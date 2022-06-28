import pytest

from trackingvn.trackingvn_service import pipeline_service

TIME_FRAME = [
    ("auto", (None, None)),
    ("manual", ("2022-06-01", "2022-06-26")),
]


@pytest.mark.parametrize(
    ["start", "end"],
    [i[1] for i in TIME_FRAME],
    ids=[i[0] for i in TIME_FRAME],
)
def test_service(start, end):
    res = pipeline_service(start, end)
    assert res["output_rows"] >= 0
