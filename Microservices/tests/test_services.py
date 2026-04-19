from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest
import requests
from fastapi import HTTPException
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]


def load_app(relative_path: str):
    file_path = ROOT / relative_path
    spec = spec_from_file_location(file_path.stem.replace('-', '_'), file_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.app


def load_module(relative_path: str):
    file_path = ROOT / relative_path
    spec = spec_from_file_location(file_path.stem.replace('-', '_'), file_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_users_service_returns_user():
    app = load_app("users-service/main.py")
    client = TestClient(app)

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "user_name": "Marcin"}



def test_orders_service_creates_order():
    module = load_module("orders-service/main.py")

    class DummyResponse:
        def __init__(self, payload):
            self._payload = payload

        def json(self):
            return self._payload

        def raise_for_status(self):
            return None

    def fake_get(url, timeout):
        assert url == "http://127.0.0.1:8002/users/1"
        assert timeout == 2
        return DummyResponse({"user_id": 1, "user_name": "Marcin"})

    module.requests.get = fake_get
    client = TestClient(module.app)

    response = client.post(
        "/orders",
        json={"user_id": 1, "product": "Laptop"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "user_name": "Marcin",
        "product": "Laptop",
    }


def test_root_script_run_orchestrates_services(monkeypatch):
    module = load_module("main.py")

    class DummyResponse:
        def __init__(self, payload):
            self._payload = payload

        def json(self):
            return self._payload

        def raise_for_status(self):
            return None

    def fake_post(url, json, timeout):
        assert url == "http://127.0.0.1:8001/orders"
        assert timeout == 5
        assert json == {"user_id": 1, "product": "Laptop"}
        return DummyResponse({"user_id": 1, "user_name": "Marcin", "product": "Laptop"})

    monkeypatch.setattr(module.requests, "post", fake_post)

    result = module.run()

    assert result == {"user_id": 1, "user_name": "Marcin", "product": "Laptop"}


def test_root_script_run_propagates_http_error(monkeypatch):
    module = load_module("main.py")

    class DummyErrorResponse:
        def raise_for_status(self):
            raise requests.HTTPError("orders-service unavailable")

    monkeypatch.setattr(module.requests, "post", lambda url, json, timeout: DummyErrorResponse())

    with pytest.raises(HTTPException) as exc_info:
        module.run()

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Users service unavailable"


