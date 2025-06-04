import pytest
from prometheus_test import TestStep, TestRunner
from pathlib import Path

def test_test_step_creation():
    """Test basic TestStep creation."""
    def dummy_prepare(context):
        return {"prepared": True}
    
    def dummy_execute(context, prepare_data):
        assert prepare_data.get("prepared") == True
        return {"success": True}
    
    step = TestStep(
        name="test_step",
        description="A test step",
        prepare=dummy_prepare,
        execute=dummy_execute,
        worker="test_worker"
    )
    
    assert step.name == "test_step"
    assert step.description == "A test step"
    assert step.worker == "test_worker"

def test_test_runner_initialization():
    """Test basic TestRunner initialization."""
    base_dir = Path(__file__).parent
    steps = [
        TestStep(
            name="step1",
            description="First step",
            prepare=lambda context: {},
            execute=lambda context, prepare_data: {},
            worker="worker1"
        )
    ]
    
    # Mock config file creation
    config_file = base_dir / "test_config.yaml"
    config_file.write_text("""
    task_id: test_task
    base_port: 5000
    max_rounds: 3
    """)
    
    try:
        runner = TestRunner(
            steps=steps,
            config_file=config_file
        )
        
        assert runner is not None
        assert runner.config is not None
        assert runner.config.task_id == "test_task"
    finally:
        # Clean up test config file
        config_file.unlink()