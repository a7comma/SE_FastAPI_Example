import pytest
from pytest_mock import MockerFixture
from fastapi import HTTPException

from services.sentiment import SentimentService

def test_analyze_success(mocker: MockerFixture):

    mock_pipeline = mocker.Mock()
    mock_pipeline.return_value = [{"label": "POSITIVE", "score": 0.91}]

    mocker.patch("services.sentiment.pipeline", return_value=mock_pipeline)

    service = SentimentService()

    result = service.analyze("Я люблю тебя, Мир!")

    assert isinstance(result, list)
    assert len(result) > 0

    item = result[0]

    assert isinstance(item, dict)
    assert "label" in item
    assert "score" in item

    assert isinstance(item["label"], str)
    assert isinstance(item["score"], float)

def test_analyze_empty_text(mocker: MockerFixture):
    mocker.patch("services.sentiment.pipeline")

    service = SentimentService()

    with pytest.raises(HTTPException) as exc:
        service.analyze("")

    assert exc.value.status_code == 400
    assert exc.value.detail == "Text cannot be empty"

def test_analyze_pipeline_error(mocker: MockerFixture):
    mock_pipeline = mocker.Mock()
    mock_pipeline.side_effect = Exception("model crash")

    mocker.patch("services.sentiment.pipeline", return_value=mock_pipeline)

    service = SentimentService()

    with pytest.raises(HTTPException) as exc:
        service.analyze("Some text")

    assert exc.value.status_code == 500
    assert exc.value.detail == "Internal Server Error"