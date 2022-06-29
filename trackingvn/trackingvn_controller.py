from typing import Any

from trackingvn.trackingvn_service import pipeline_service


def controller(body: dict[str, Any]):
    res = pipeline_service(
        body.get("start"),
        body.get("end"),
    )
    return {"results": res}
