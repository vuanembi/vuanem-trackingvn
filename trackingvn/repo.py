import os
from datetime import datetime
import json

import httpx

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
API_COUNT = 500
LISTING_API_REQ_PER_SEC = 6
DETAILS_API_REQ_PER_SEC = 12
DETAILS_LIMIT = 2500


def _get_client() -> httpx.Client:
    return httpx.Client(
        base_url="https://vuanem.coffeehr.vn/API/CustomAPI/GetCustomAPI",
        headers={"Token": os.getenv("COFFEEHR_TOKEN", "")},
        timeout=None,
    )


def parse_timeframe(timeframe: tuple[datetime, datetime]):
    start, end = timeframe
    return {
        k: v.strftime("%d/%m/%Y")
        for k, v in [
            ("fromtime", start),
            ("totime", end),
        ]
    }


def get(get_options: tuple[str, str]):
    def _get(timeframe: tuple[datetime, datetime]):
        method, api_code = get_options

        with _get_client() as client:
            r = client.request(
                method,
                "/",
                data={
                    "APICode": api_code,
                    **parse_timeframe(timeframe),
                },
            )
            res = r.json()
            data = res["Data"]
            return json.loads(data)

    return _get
