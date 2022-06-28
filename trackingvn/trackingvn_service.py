from typing import Optional, Any
from datetime import datetime, timedelta
import re

from compose import compose
from trackingvn import trackingvn_repository, trackingvn_entity
import pytz

from db.bigquery import load

TZ = pytz.timezone("Asia/Ho_Chi_Minh")


def parse_timestamp(value: str) -> Optional[str]:
    match = re.search("\d{5,}", value)

    if not match:
        return None

    match_str = match.group(0)

    return (
        datetime.fromtimestamp(int(match_str) / 1000)
        .astimezone(TZ)
        .isoformat(timespec="seconds")
    )


def transform(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "tn": row.get("tn"),
            "t": parse_timestamp(row.get("t", "")),
            "k": row.get("k"),
            "r": row.get("r"),
            "rs": parse_timestamp(row.get("rs", "")),
            "re": parse_timestamp(row.get("re", "")),
            "sc": row.get("sc"),
            "kme": row.get("kme"),
            "dre": row.get("dre"),
            "_batched_at": datetime.utcnow().isoformat(timespec="seconds"),
        }
        for row in rows
    ]


def pipeline_service(start: Optional[str], end: Optional[str]) -> int:
    _start = (
        datetime.strptime(start, "%Y-%m-%d")
        if start
        else datetime.utcnow() - timedelta(days=10)
    )
    _end = datetime.strptime(end, "%Y-%m-%d") if end else datetime.utcnow()

    with trackingvn_repository.get_auth_session() as client:
        return compose(
            lambda x: {
                "output_rows": x,
            },
            load("p_ReportSummary", 't', trackingvn_entity.schema),
            transform,
            trackingvn_repository.get_report_summary(client, _start, _end),
            trackingvn_repository.get_vehicles(client),
        )()
