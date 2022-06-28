from typing import Any
import os
from datetime import datetime

import httpx

BASE_URL = "http://api.tracking.vn"
DEVICE_ID = "BI"

TIME_FORMAT = "%d/%m/%Y %H:%M:%S"


def get_auth_session() -> httpx.Client:
    res = httpx.post(
        f"{BASE_URL}/users/login",
        headers={
            "UserName": os.getenv("USERNAME", ""),
            "PassWord": os.getenv("PASSWORD", ""),
            "DeviceID": DEVICE_ID,
        },
    )
    res.raise_for_status()

    data = res.json()

    return httpx.Client(
        base_url=BASE_URL,
        headers={"DeviceID": DEVICE_ID, "token": data["Result"]["Token"]["UserToken"]},
        timeout=None,
    )


def get_vehicles(client: httpx.Client):
    def _get() -> list[str]:
        res = client.post("/users/getstatus/1")
        res.raise_for_status()

        data = res.json()

        return [i["N"] for i in data["Result"]]

    return _get


def get_report_summary(client: httpx.Client, start: datetime, end: datetime):
    def _get(vehicles: list[str]) -> list[dict[str, Any]]:
        res = client.post(
            "/reports/totalsumary",
            params={
                "vehiclesName": ",".join(vehicles),
                "From": start.strftime(TIME_FORMAT),
                "To": end.strftime(TIME_FORMAT),
                "Rebuilt": 1,
            },
        )
        res.raise_for_status()
        data = res.json()

        return data["Result"]["items"]

    return _get
