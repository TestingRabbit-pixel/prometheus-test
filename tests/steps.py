from prometheus_test import TestStep
from functools import partial

def prepare_step1(runner, worker):
    """Setup for step 1"""
    task_id = runner.config.task_id
    return {
        "task_id": task_id,
        "test_value": 100
    }

def execute_step1(runner, worker, prepare_data):
    """Execute step 1"""
    task_id = prepare_data["task_id"]
    test_value = prepare_data["test_value"]
    
    # Make a request using the provided worker
    print(f"\nMaking request to {worker.url}/test-endpoint")
    response = worker.get("/test-endpoint")
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response body: {response.text}")
    
    if not response.ok:
        return {
            "success": False,
            "error": f"Request failed with status {response.status_code}: {response.text}"
        }
    
    try:
        data = response.json()
        if data.get("status") != "success":
            return {
                "success": False,
                "error": data.get("message", "Unknown error")
            }
        return {
            "success": True,
            "data": data
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Invalid JSON response - {response.text}"
        }

def prepare_step2(runner, worker):
    """Setup for step 2"""
    return {
        "message": "Testing step 2"
    }

def execute_step2(runner, worker, prepare_data):
    """Execute step 2"""
    message = prepare_data["message"]
    
    # Make a request using the provided worker
    print(f"\nMaking request to {worker.url}/process")
    response = worker.post("/process", json={"message": message})
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response body: {response.text}")
    
    if not response.ok:
        return {
            "success": False,
            "error": f"Request failed with status {response.status_code}: {response.text}"
        }
    
    try:
        data = response.json()
        if data.get("status") != "success":
            return {
                "success": False,
                "error": data.get("message", "Unknown error")
            }
        return {
            "success": True,
            "data": data
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Invalid JSON response - {response.text}"
        }

# Define test steps
steps = [
    TestStep(
        name="step1",
        description="First test step",
        prepare=prepare_step1,
        execute=execute_step1,
        worker="worker1"
    ),
    TestStep(
        name="step2",
        description="Second test step",
        prepare=prepare_step2,
        execute=execute_step2,
        worker="worker2"
    )
] 