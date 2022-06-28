from typing import Any

from coffeehr import coffeehr_controller
from tasks.tasks_service import create_tasks_service


def main(request):
    data: dict[str, Any] = request.get_json()
    print(data)

    if "tasks" in data:
        response = create_tasks_service()
    elif "table" in data:
        response = coffeehr_controller.controller(data)
    else:
        raise ValueError(data)

    print(response)
    return response
