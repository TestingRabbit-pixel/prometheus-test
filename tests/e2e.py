from pathlib import Path
from prometheus_test import TestRunner
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Import test steps
from .steps import steps

def post_load_callback(db):
    """Modify database after initial load"""
    # Example: Add a timestamp to all documents
    for doc in db.test_collection.find():
        db.test_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"loaded_at": "2024-01-01T00:00:00Z"}}
        )

def main():
    # Create test runner with config from YAML
    base_dir = Path(__file__).parent
    runner = TestRunner(
        steps=steps,
        config_file=base_dir / "config.yaml",
        config_overrides={
            "post_load_callback": post_load_callback
        }
    )

    # Run test sequence
    runner.run(force_reset=False)

if __name__ == "__main__":
    main() 