from typing import Any

from trackingvn import trackingvn_controller


def main(request):
    data: dict[str, Any] = request.get_json()
    print(data)

    response = trackingvn_controller.controller(data)

    print(response)
    return response
