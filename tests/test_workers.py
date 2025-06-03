import pytest
from prometheus_test.workers import WorkerConfig

def test_worker_config_parsing():
    # Test worker configuration parsing
    worker_config = {
        "worker1": {
            "port": 5001,
            "env": {
                "WORKER_ID": "worker1"
            }
        }
    }
    
    config = WorkerConfig(worker_config)
    
    assert len(config.workers) == 1
    assert config.workers[0].name == "worker1"
    assert config.workers[0].port == 5001
    assert config.workers[0].env.get("WORKER_ID") == "worker1"