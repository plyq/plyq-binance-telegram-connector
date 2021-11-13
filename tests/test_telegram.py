"""Tests main app behaviour"""
import json
from typing import Generator

import pytest
from flask.testing import FlaskClient  # type: ignore
from pytest import MonkeyPatch

from app import create_app
from app.telegram import telegram_bot
from app.thirdparty.proxy import MirrorProxy


@pytest.fixture
def client(monkeypatch: MonkeyPatch) -> Generator[FlaskClient, None, None]:
    """Monkeypatch app client."""
    monkeypatch.setenv("FLASK_ENV", "TEST")
    app = create_app()

    with app.test_client() as client:
        yield client


@pytest.fixture
def mocked_client(
    monkeypatch: MonkeyPatch, client: FlaskClient
) -> Generator[FlaskClient, None, None]:
    """Monkeypatch app client with proxy (not internet connection needed)."""
    monkeypatch.setattr(telegram_bot, "_proxy", MirrorProxy())
    yield client


class TestEndToEnd:
    """Test real Telegram calls."""

    def test_check0(self, client: FlaskClient) -> None:
        """Test real chat status check."""
        response = client.get("/check")
        actual_data = json.loads(response.data)
        assert actual_data["ok"]
        assert actual_data["result"]["is_bot"]


class TestIntegration:
    """Test correctness of requests w/o real Telegram calls."""

    def test_check0(self, mocked_client: FlaskClient) -> None:
        """Test mocked chat status check."""
        response = mocked_client.get("/check")
        actual_data = json.loads(response.data)
        assert actual_data["method"] == "GET"
        assert actual_data["request"] == "getMe"

    def test_send0(self, mocked_client: FlaskClient) -> None:
        """Test mocked chat status check with wrong data."""
        response = mocked_client.post(
            "/send", data='{"a": 10}', headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 404

    def test_send1(self, mocked_client: FlaskClient) -> None:
        """Test mocked chat status check with OK data."""
        response = mocked_client.post(
            "/send",
            data='{"message": "Hi", "chat": "abc"}',
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 1
        actual_data = json.loads(response.data)
        print(actual_data)
        assert actual_data["method"] == "POST"
        assert actual_data["request"] == "sendMessage"
        assert actual_data["kwargs"]["data"] == {"chat_id": "abc", "text": "Hi"}
