from typing import Dict, List, Optional

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