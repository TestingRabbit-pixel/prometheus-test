import pytest
from prometheus_test.data import load_yaml_config

def test_load_yaml_config():
    # Test basic YAML config loading
    sample_config = '''
    task_id: test_task
    base_port: 5000
    max_rounds: 3
    '''
    config = load_yaml_config(sample_config)
    
    assert config['task_id'] == 'test_task'
    assert config['base_port'] == 5000
    assert config['max_rounds'] == 3