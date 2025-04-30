"""Stage for worker audits."""

import requests


def prepare(runner, worker, target_name):
    """Prepare data for worker audit"""
    # Check if we have a PR URL for the target
    pr_url = runner.get(f"pr_urls.{target_name}")
    if pr_url is None:
        print(
            f"✓ No PR URL found for {target_name}, skipping {worker.get('name')} audit - continuing"
        )
        return None

    # Get submission data from state
    submission_data = runner.get(f"submission_data.{target_name}")
    if submission_data is None:
        print(
            f"✓ No submission data found for {target_name}, skipping {worker.get('name')} audit - continuing"
        )
        return None

    return {"submission": submission_data}


def execute(runner, worker, data):
    """Execute worker audit step"""
    # If prepare returned None, skip this step
    if data is None:
        return {
            "success": True,
            "message": "Skipped due to missing PR URL or submission data",
        }

    url = f"{worker.get('url')}/worker-audit/{runner.get('current_round')}"
    response = requests.post(url, json=data)
    result = response.json()

    return result
