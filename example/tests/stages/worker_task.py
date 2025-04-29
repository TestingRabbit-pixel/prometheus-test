"""Stage for executing worker tasks."""

import requests


def prepare(runner, worker):
    """Prepare data for worker task"""
    return {
        "taskId": runner.get("task_id"),
        "round_number": str(runner.get("current_round")),
        "repo_url": runner.get("repo_url"),
    }


def execute(runner, worker, data):
    """Execute worker task step"""
    if not data:
        return {"success": True, "message": "No repo url found"}
    url = f"{worker.url}/worker-task/{runner.state['current_round']}"
    response = requests.post(url, json=data)
    result = response.json()

    # Handle 409 gracefully - no eligible todos is an expected case
    if response.status_code == 409:
        print(
            f"✓ {result.get('message', 'No eligible todos')} for {worker.name} - continuing"
        )
        return {"success": True, "message": result.get("message")}

    if result.get("success") and "pr_url" in result["result"]["data"]:
        # Store PR URL in state
        runner.set(f"pr_urls.{worker.name}", result["result"]["data"]["pr_url"])

    return result
