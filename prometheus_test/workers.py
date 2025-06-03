from typing import Dict, List, Optional, Any

class Worker:
    def __init__(self, name: str, port: int, env: Optional[Dict[str, str]] = None):
        """
        Represents a single worker configuration.
        
        Args:
            name (str): Worker name
            port (int): Port number for the worker
            env (dict, optional): Environment variables for the worker
        """
        self.name = name
        self.port = port
        self.env = env or {}

class WorkerConfig:
    def __init__(self, config: Dict[str, Dict]):
        """
        Parse worker configuration from a dictionary.
        
        Args:
            config (dict): Worker configuration dictionary
        """
        self.workers: List[Worker] = []
        
        for name, worker_info in config.items():
            worker = Worker(
                name=name,
                port=worker_info.get('port', 0),
                env=worker_info.get('env', {})
            )
            self.workers.append(worker)

class TestEnvironment:
    """
    Manages the test environment configuration and state.
    """
    def __init__(self, workers: List[Worker], config: Optional[Dict[str, Any]] = None):
        """
        Initialize test environment.
        
        Args:
            workers (List[Worker]): List of configured workers
            config (dict, optional): Additional configuration parameters
        """
        self.workers = workers
        self.config = config or {}
        self.state: Dict[str, Any] = {}
    
    def get_worker(self, name: str) -> Optional[Worker]:
        """
        Retrieve a worker by name.
        
        Args:
            name (str): Name of the worker
        
        Returns:
            Worker or None if not found
        """
        return next((worker for worker in self.workers if worker.name == name), None)
    
    def set_state(self, key: str, value: Any):
        """
        Set a state value.
        
        Args:
            key (str): State key
            value (Any): State value
        """
        self.state[key] = value
    
    def get_state(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a state value.
        
        Args:
            key (str): State key
            default (Any, optional): Default value if key not found
        
        Returns:
            State value or default
        """
        return self.state.get(key, default)