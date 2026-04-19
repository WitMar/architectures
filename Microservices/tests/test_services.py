from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest
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
    app = load_app("orders-service/main.py")
    client = TestClient(app)

    response = client.post(
        "/orders",
        json={"user_id": 1, "user_name": "Marcin", "product": "Laptop"},
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

    def fake_get(url, timeout):
        assert url == "http://127.0.0.1:8001/users/1"
        assert timeout == 5
        return DummyResponse({"user_id": 1, "user_name": "Marcin"})

    def fake_post(url, json, timeout):
        assert url == "http://127.0.0.1:8002/orders"
        assert timeout == 5
        assert json == {"user_id": 1, "user_name": "Marcin", "product": "Laptop"}
        return DummyResponse(json)

    monkeypatch.setattr(module.requests, "get", fake_get)
    monkeypatch.setattr(module.requests, "post", fake_post)

    result = module.run()

    assert result == {"user_id": 1, "user_name": "Marcin", "product": "Laptop"}


def test_root_script_run_propagates_http_error(monkeypatch):
    module = load_module("main.py")

    class DummyErrorResponse:
        def raise_for_status(self):
            raise requests.HTTPError("users-service unavailable")

    import requests

    monkeypatch.setattr(module.requests, "get", lambda url, timeout: DummyErrorResponse())

    with pytest.raises(requests.HTTPError):
        module.run()


