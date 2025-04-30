import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from typing import Dict, Optional, Any
from dotenv import load_dotenv
import threading
from .utils import load_keypair

load_dotenv()


class Worker:
    """Represents a worker in the test environment"""

    def __init__(
        self,
        name: str,
        base_dir: Path,
        port: int,
        env_vars: Dict[str, str],
        keypairs: Dict[str, str],
        server_entrypoint: Optional[Path] = None,
        **config,
    ):
        self.name = name
        self.base_dir = base_dir
        self.port = port

        # Initialize data storage with any additional config fields
        self._data = {
            k: v
            for k, v in config.items()
            if k not in ["env_vars", "keypairs", "server_entrypoint"]
        }

        base_env = base_dir / ".env"  # Test framework base .env
        if base_env.exists():
            load_dotenv(base_env, override=True)  # Override any existing values

        # Load keypairs using provided paths or environment variables
        staking_keypair_path = os.getenv(
            keypairs.get("staking"), f"{name.upper()}_STAKING_KEYPAIR"
        )
        public_keypair_path = os.getenv(
            keypairs.get("public"), f"{name.upper()}_PUBLIC_KEYPAIR"
        )

        # Load keypairs
        self.staking_signing_key, self.staking_public_key = load_keypair(
            staking_keypair_path
        )
        self.public_signing_key, self.public_key = load_keypair(public_keypair_path)

        # Server configuration
        self.url = f"http://localhost:{port}"
        self.process = None
        self.server_entrypoint = server_entrypoint
        self.database_path = base_dir / f"database_{name}.db"

        # Environment setup
        self.env = os.environ.copy()
        # For each environment variable in env_vars, get its value from the environment
        for key, env_var_name in env_vars.items():
            self.env[key] = os.getenv(env_var_name)
        self.env["DATABASE_PATH"] = str(self.database_path)
        self.env["PYTHONUNBUFFERED"] = "1"  # Always ensure unbuffered output
        self.env["PORT"] = str(self.port)  # Set the port for the server

    def _print_output(self, stream, prefix):
        """Print output from a stream with a prefix"""
        for line in stream:
            print(f"{prefix} {line.strip()}")
            sys.stdout.flush()

    def start(self):
        """Start the worker's server"""
        print(f"\nStarting {self.name} server on port {self.port}...")
        sys.stdout.flush()

        # Start the process with unbuffered output
        self.process = subprocess.Popen(
            [sys.executable, str(self.server_entrypoint)],
            env=self.env,
            cwd=self.base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )

        # Wait for server to start
        time.sleep(3)  # Default timeout

        # Check if server started successfully
        if self.process.poll() is not None:
            _, stderr = self.process.communicate()
            error_msg = stderr.strip() if stderr else "No error output available"
            raise RuntimeError(f"Failed to start {self.name} server:\n{error_msg}")

        stdout_thread = threading.Thread(
            target=self._print_output,
            args=(self.process.stdout, f"[{self.name}]"),
            daemon=True,
        )
        stderr_thread = threading.Thread(
            target=self._print_output,
            args=(self.process.stderr, f"[{self.name} ERR]"),
            daemon=True,
        )
        stdout_thread.start()
        stderr_thread.start()

    def stop(self):
        """Stop the worker's server"""
        if self.process:
            print(f"\nStopping {self.name} server...")
            sys.stdout.flush()

            # Send SIGTERM first to allow graceful shutdown
            os.kill(self.process.pid, signal.SIGTERM)
            time.sleep(1)

            # If still running, send SIGKILL
            if self.process.poll() is None:
                os.kill(self.process.pid, signal.SIGKILL)

            # Wait for process to fully terminate
            self.process.wait()
            self.process = None

    def get_env(self, key: str) -> Optional[str]:
        """Get an environment variable value.

        Args:
            key: The environment variable name to look up

        Returns:
            The environment variable value if found, None otherwise
        """
        return self.env.get(key)

    def get_key(self, key_type: str = "public") -> str:
        """Get a key value (public or signing key).

        Args:
            key_type: Type of key to return, either "public" or "staking"

        Returns:
            The requested public key

        Raises:
            ValueError: If key_type is not "public" or "staking"
        """
        if key_type == "public":
            return self.public_key
        elif key_type == "staking":
            return self.staking_public_key
        else:
            raise ValueError('key_type must be either "public" or "staking"')

    def get(self, key: str, default: Any = None) -> Any:
        """Get an arbitrary stored value.

        Args:
            key: The key to look up
            default: Value to return if key is not found

        Returns:
            The stored value if found, default otherwise
        """
        return self._data.get(key, default)


class TestEnvironment:
    """Manages multiple workers for testing"""

    def __init__(
        self,
        worker_configs: Dict[str, dict],
        base_dir: Path,
        base_port: int = 5000,
        server_entrypoint: Optional[Path] = None,
    ):
        self.base_dir = base_dir

        # Set default startup script if not provided
        if server_entrypoint is None:
            server_entrypoint = base_dir.parent / "main.py"
            if not server_entrypoint.exists():
                raise FileNotFoundError(
                    f"Server entrypoint not found: {server_entrypoint}"
                )

        # Create workers
        self.workers: Dict[str, Worker] = {}
        for i, (name, config) in enumerate(worker_configs.items()):
            # Extract special config fields
            env_vars = config.get("env_vars", {})
            keypairs = config.get("keypairs", {})

            # Use port from config if specified, otherwise use base_port + index
            port = config.get("port", base_port + i)

            # Create worker with all config fields
            worker = Worker(
                name=name,
                base_dir=base_dir,
                port=port,
                env_vars=env_vars,
                keypairs=keypairs,
                server_entrypoint=server_entrypoint,
                **config,  # Pass through all config fields
            )
            self.workers[name] = worker

    def __enter__(self):
        """Start all worker servers"""
        print("Starting worker servers...")
        try:
            for worker in self.workers.values():
                worker.start()
            return self
        except Exception as e:
            print(f"Failed to start servers: {str(e)}")
            self._cleanup()
            raise

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        """Stop all worker servers"""
        print("Stopping worker servers...")
        self._cleanup()

    def _cleanup(self):
        """Clean up all worker processes"""
        for worker in self.workers.values():
            if worker.process:
                try:
                    os.kill(worker.process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass  # Process already gone
                worker.process = None

    def get_worker(self, name: str) -> Worker:
        """Get a worker by name"""
        if name not in self.workers:
            raise KeyError(f"No worker found with name: {name}")
        return self.workers[name]
