import yaml
from io import StringIO

def load_yaml_config(config_str):
    """
    Load configuration from a YAML string.
    
    Args:
        config_str (str): YAML configuration string
    
    Returns:
        dict: Parsed configuration
    """
    try:
        return yaml.safe_load(StringIO(config_str))
    except yaml.YAMLError as e:
        raise ValueError(f"Failed to parse YAML configuration: {e}")