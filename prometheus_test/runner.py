from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypedDict
import json
from contextlib import contextmanager
from pymongo import MongoClient
from .workers import TestEnvironment
import yaml
import os


class MongoCollectionConfig(TypedDict, total=False):
    data_file: str  # Optional, not all collections need data files
    required_count: int


class MongoConfig(TypedDict, total=False):
    database: str
    collections: Dict[str, MongoCollectionConfig]


@dataclass
class TestConfig:
    """Configuration for the test runner"""

    base_dir: Path = Path.cwd()
    data_dir: Optional[Path] = None
    workers_config: str = "workers.json"
    task_id: str = "test-task-123"
    base_port: int = 5000
    middle_server_url: Optional[str] = None
    server_entrypoint: Optional[Path] = None
    max_rounds: Optional[int] = (
        None  # Will be calculated from collection if not specified
    )
    rounds_collection: Optional[str] = (
        "todos"  # Collection to use for calculating max_rounds
    )
    post_load_callback: Optional[Callable[[Any], None]] = (
        None  # Callback for post-JSON data processing
    )
    mongodb: MongoConfig = field(
        default_factory=lambda: {
            "database": "builder247",
            "collections": {
                "issues": {"required_count": 1},
                "todos": {"required_count": 1},
                "systemprompts": {"required_count": 0},
                "audits": {"required_count": 0},
            },
        }
    )

    @classmethod
    def from_yaml(
        cls, yaml_path: Path, base_dir: Optional[Path] = None
    ) -> "TestConfig":
        """Create TestConfig from a YAML file"""
        # Load YAML config
        with open(yaml_path) as f:
            config = yaml.safe_load(f) or {}

        # Use base_dir from argument or yaml_path's parent
        base_dir = base_dir or yaml_path.parent
        config["base_dir"] = base_dir

        # Convert relative paths to absolute
        if "data_dir" in config and not config["data_dir"].startswith("/"):
            config["data_dir"] = base_dir / config["data_dir"]
        if "server_entrypoint" in config and not config["server_entrypoint"].startswith(
            "/"
        ):
            config["server_entrypoint"] = base_dir / config["server_entrypoint"]

        # Merge MongoDB config with defaults
        if "mongodb" in config:
            default_mongodb = cls().mongodb
            mongodb_config = config["mongodb"]

            # Use default database if not specified
            if "database" not in mongodb_config:
                mongodb_config["database"] = default_mongodb["database"]

            # Merge collection configs with defaults
            if "collections" in mongodb_config:
                for coll_name, default_coll in default_mongodb["collections"].items():
                    if coll_name not in mongodb_config["collections"]:
                        mongodb_config["collections"][coll_name] = default_coll
                    else:
                        # Merge with default collection config
                        mongodb_config["collections"][coll_name] = {
                            **default_coll,
                            **mongodb_config["collections"][coll_name],
                        }

        # Extract known fields for the config class
        known_fields = {k: v for k, v in config.items() if k in cls.__dataclass_fields__}

        return cls(**known_fields)

    def __post_init__(self):
        # Convert string paths to Path objects
        self.base_dir = Path(self.base_dir)
        if self.data_dir:
            self.data_dir = Path(self.data_dir)
        else:
            self.data_dir = self.base_dir / "data"

        if self.server_entrypoint:
            self.server_entrypoint = Path(self.server_entrypoint)


@dataclass
class TestStep:
    """Represents a single step in a task test sequence"""

    name: str
    description: str
    worker: str
    prepare: Callable[[], Dict[str, Any]]  # Returns data needed for the step
    execute: Callable[Dict[str, Any], Any]  # Takes prepared data and executes step
    validate: Optional[Callable[[Any, Any], None]] = (
        None  # Optional validation function
    )


class TestRunner:
    """Main test runner that executes a sequence of test steps"""

    def __init__(
        self,
        steps: List[TestStep],
        config_file: Optional[Path] = None,
        config_overrides: Optional[Dict[str, Any]] = None,
    ):
        """Initialize test runner with steps and optional config"""
        self.steps = steps
        self._config = TestConfig.from_yaml(config_file) if config_file else TestConfig()

        # Initialize state
        self.state = {
            "rounds": {},  # Round-specific state
            "global": {},  # Global state (includes config)
            "current_round": 1,
        }

        if config_file:
            # Load all values from config file into global state
            with open(config_file) as f:
                yaml_config = yaml.safe_load(f) or {}
                self.state["global"].update(yaml_config)

        # Ensure core config values are set correctly
        for field in self._config.__dataclass_fields__:
            self.state["global"][field] = getattr(self._config, field)

        # Apply any config overrides to global state
        if config_overrides:
            self.state["global"].update(config_overrides)

        # Initialize other state
        self.last_completed_step = None

        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Initialize test environment and MongoDB client
        self._test_env = None
        self._mongo_client = None
        self._max_rounds = None

    @property
    def data_dir(self) -> Path:
        """Convenience property for data_dir access"""
        return self.state["global"]["data_dir"]

    @property
    def mongo_client(self) -> MongoClient:
        """Get MongoDB client, initializing if needed"""
        if self._mongo_client is None:
            # Get MongoDB URI from environment variable
            mongodb_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
            self._mongo_client = MongoClient(mongodb_uri)
        return self._mongo_client

    @property
    def max_rounds(self) -> int:
        """Get maximum number of rounds, calculating from the specified collection if not set explicitly"""
        if self._max_rounds is None:
            if self._config.max_rounds is not None:
                self._max_rounds = self._config.max_rounds
            else:
                # Count documents in the specified collection and add 1
                if not self._config.rounds_collection:
                    raise ValueError(
                        "No collection specified for calculating max_rounds"
                    )

                db = self.mongo_client[self._config.mongodb["database"]]
                if self._config.rounds_collection not in db.list_collection_names():
                    raise ValueError(
                        f"Collection {self._config.rounds_collection} does not exist"
                    )

                self._max_rounds = (
                    db[self._config.rounds_collection].count_documents(
                        {"taskId": self._config.task_id}
                    )
                    + 1
                )
                print(
                    f"\nCalculated {self._max_rounds} rounds from {self._config.rounds_collection} collection"
                )
        return self._max_rounds

    def check_mongodb_state(self) -> bool:
        """Check if MongoDB is in the expected state

        Returns:
            bool: True if all collections exist and have required document counts
        """
        db = self.mongo_client[self._config.mongodb["database"]]

        for coll_name, coll_config in self._config.mongodb["collections"].items():
            # Skip if collection doesn't exist and no documents required
            if coll_config.get("required_count", 0) == 0:
                continue

            # Check if collection exists and has required documents
            if coll_name not in db.list_collection_names():
                print(f"Collection {coll_name} does not exist")
                return False

            count = db[coll_name].count_documents({"taskId": self._config.task_id})
            if count < coll_config["required_count"]:
                print(
                    f"Collection {coll_name} has {count} documents, requires {coll_config['required_count']}"
                )
                return False

        return True

    def reset_local_databases(self):
        """Reset all local database files"""
        print("\nResetting local databases...")
        for worker in self.test_env.workers.values():
            if worker.database_path.exists():
                print(f"Deleting database file: {worker.database_path}")
                worker.database_path.unlink()

    def reset_mongodb(self):
        """Reset MongoDB database and import data files from config"""
        print("\nResetting MongoDB database...")

        # Connect to MongoDB
        db = self.mongo_client[self._config.mongodb["database"]]

        # Clear collections
        print("\nClearing collections...")
        for collection in self._config.mongodb["collections"]:
            db[collection].delete_many({})

        # Import data files
        for coll_name, coll_config in self._config.mongodb["collections"].items():
            if "data_file" not in coll_config:
                continue

            data_file = self.data_dir / coll_config["data_file"]
            if not data_file.exists():
                if coll_config.get("required_count", 0) > 0:
                    raise FileNotFoundError(
                        f"Required data file not found: {data_file}"
                    )
                continue

            print(f"Importing data for {coll_name} from {data_file}")
            with open(data_file) as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]

                # Add task_id to all documents
                for item in data:
                    item["taskId"] = self._config.task_id

                # Insert data into collection
                db[coll_name].insert_many(data)

        # Run post-load callback if provided
        if self._config.post_load_callback:
            print("\nRunning post-load data processing...")
            self._config.post_load_callback(db)

        # Reset max_rounds cache after data import
        self._max_rounds = None

    def ensure_clean_state(self, force_reset: bool = False):
        """Ensure databases are in a clean state

        Args:
            force_reset: If True, always reset databases regardless of current state
        """
        needs_reset = force_reset or not self.check_mongodb_state()

        if needs_reset:
            print("\nResetting databases...")
            self.reset_local_databases()
            self.reset_mongodb()
            self.reset_state()

    @property
    def test_env(self) -> TestEnvironment:
        """Get the test environment, initializing if needed"""
        if self._test_env is None:
            workers_config = Path(self._config.workers_config)
            if not workers_config.is_absolute():
                workers_config = self._config.base_dir / workers_config

            self._test_env = TestEnvironment(
                config_file=workers_config,
                base_dir=self._config.base_dir,
                base_port=self._config.base_port,
                server_entrypoint=self._config.server_entrypoint,
            )
        return self._test_env

    def get_worker(self, name: str):
        """Get a worker by name"""
        return self.test_env.get_worker(name)

    def save_state(self):
        """Save current test state to file"""
        state_file = self.data_dir / "test_state.json"
        # Add current round and step to state before saving
        self.state["current_round"] = self.state["current_round"]
        if self.last_completed_step:
            self.state["last_completed_step"] = self.last_completed_step
        with open(state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def load_state(self):
        """Load test state from file if it exists"""
        state_file = self.data_dir / "test_state.json"
        if state_file.exists():
            with open(state_file, "r") as f:
                self.state = json.load(f)
                # Restore current round and step from state
                self.set("current_round", self.state.get("current_round", 1), scope="execution")
                self.set("last_completed_step", self.state.get("last_completed_step"), scope="execution")
            return True
        return False

    def reset_state(self):
        """Clear the current state"""
        self.state = {
            "rounds": {},
            "current_round": 1,
        }
        self.set("last_completed_step", None, scope="execution")
        state_file = self.data_dir / "test_state.json"
        if state_file.exists():
            state_file.unlink()

    def log_step(self, step: TestStep):
        """Log test step execution"""
        print("\n" + "#" * 80)
        print(f"STEP {step.name}: {step.description}")
        print("#" * 80)

    @contextmanager
    def run_environment(self):
        """Context manager for running the test environment"""
        with self.test_env:
            try:
                self.load_state()
                yield
            finally:
                self.save_state()

    def next_round(self):
        """Move to next round"""
        self.set("current_round", self.state["current_round"] + 1, scope="execution")
        self.set("last_completed_step", None, scope="execution")

    def get_round_state(self):
        """Get the state for the current round"""
        return self.state["rounds"].get(str(self.state["current_round"]), {})

    def get(self, key: str) -> Any:
        """
        Unified data access method. Automatically checks all data stores in priority order:
        1. Current round state
        2. Global state (includes config)
        3. Execution state (current_round, last_completed_step)

        Args:
            key: The key to look up

        Returns:
            The value if found

        Raises:
            KeyError: If the key is not found in any scope
        """
        # Support nested key access with dot notation
        parts = key.split('.')

        # Check current round state first
        round_state = self.get_round_state()
        try:
            value = round_state
            for part in parts:
                value = value[part]
            return value
        except (KeyError, TypeError):
            pass

        # Check global state (includes config)
        try:
            value = self.state["global"]
            for part in parts:
                value = value[part]
            return value
        except (KeyError, TypeError):
            pass

        # Check execution state
        if key == "current_round":
            return self.state["current_round"]
        if key == "last_completed_step":
            return self.last_completed_step

        raise KeyError(f"Key '{key}' not found in any scope")

    def set(self, key: str, value: Any, scope: str = "round") -> None:
        """
        Unified data setter. Stores data in the appropriate location based on scope.
        Automatically creates any necessary nested dictionary structures.

        Args:
            key: The key to store. Can use dot notation for nested access (e.g. "pr_urls.worker1")
            value: The value to store
            scope: Where to store the data. Options:
                - "round": Store in current round state (default)
                - "global": Store in global state
                - "execution": Store in execution state (only for specific variables)
        """
        # Handle nested keys with dot notation
        parts = key.split('.')

        if scope == "round":
            # Ensure round state exists
            round_key = str(self.state["current_round"])
            if round_key not in self.state["rounds"]:
                self.state["rounds"][round_key] = {}

            # Navigate to the correct nested location
            current = self.state["rounds"][round_key]
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value

        elif scope == "global":
            # Navigate to the correct nested location
            current = self.state["global"]
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value

        elif scope == "execution":
            if key == "current_round":
                self.state["current_round"] = value
            elif key == "last_completed_step":
                self.last_completed_step = value
            else:
                raise ValueError(f"Cannot set execution variable: {key}")
        else:
            raise ValueError(f"Invalid scope: {scope}")

        # Save state after any modification
        self.save_state()

    def run(self, force_reset=False):
        """Run the test sequence."""
        # Try to load existing state
        has_state = self.load_state()

        # Reset if:
        # 1. --reset flag is used (force_reset)
        # 2. No existing state file
        # 3. State file exists but no steps completed yet
        if force_reset or not has_state or not self.get("last_completed_step"):
            print("\nStarting fresh test run...")
            self.ensure_clean_state(force_reset)
        else:
            print(
                f"\nResuming from step {self.get('last_completed_step')} in round {self.get('current_round')}..."
            )

        try:
            with self.run_environment():
                while self.get("current_round") <= self.max_rounds:
                    round_steps = [s for s in self.steps]

                    # Find the index to start from based on last completed step
                    start_index = 0
                    last_step = self.get("last_completed_step")
                    if last_step:
                        for i, step in enumerate(round_steps):
                            if step.name == last_step:
                                start_index = i + 1
                                break

                    # Skip already completed steps
                    for step in round_steps[start_index:]:
                        self.log_step(step)

                        worker = self.get_worker(step.worker)
                        # Prepare step data
                        data = step.prepare(self, worker)

                        # Execute step
                        result = step.execute(self, worker, data)

                        # Check for errors
                        if not result.get("success"):
                            error_msg = result.get("error", "Unknown error")
                            raise RuntimeError(f"Step {step.name} failed: {error_msg}")
                        # Save state after successful step
                        self.set("last_completed_step", step.name, scope="execution")

                    # Move to next round after completing all steps
                    if self.get("current_round") < self.max_rounds:
                        self.next_round()
                    else:
                        print("\nAll rounds completed successfully!")
                        break

        except Exception as e:
            print(f"\nTest run failed: {str(e)}")
            raise
        finally:
            # Ensure we always clean up, even if there's an error
            if hasattr(self, "_test_env") and self._test_env:
                print("\nCleaning up test environment...")
                self._test_env._cleanup()

        print("\nTest run completed.")
