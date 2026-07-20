"""Error-envelope convention tests (AC-003 contract groundwork).

Traceability: AC-003; Phase 4 Increment 4.1.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.correlation import CorrelationIdMiddleware
from app.errors import register_error_handlers


def make_test_app() -> TestClient:
    """A throwaway app with one validated route to exercise 422 shape."""
    app = FastAPI()
    app.add_middleware(CorrelationIdMiddleware)
    register_error_handlers(app)

    class Payload(BaseModel):
        name: str = Field(min_length=1, max_length=5)

    @app.post("/echo")
    def echo(payload: Payload) -> dict:
        return {"name": payload.name}

    return TestClient(app)


def test_404_uses_error_envelope(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "not_found"
    assert error["correlation_id"] == response.headers["X-Correlation-ID"]
    assert error["details"] == []


def test_422_names_field_and_rule():
    test_client = make_test_app()
    response = test_client.post("/echo", json={"name": "too-long-value"})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "validation_error"
    detail = error["details"][0]
    assert detail["field"] == "body.name"
    assert detail["rule"] == "string_too_long"
    assert detail["message"]


def test_422_missing_field():
    test_client = make_test_app()
    response = test_client.post("/echo", json={})
    assert response.status_code == 422
    detail = response.json()["error"]["details"][0]
    assert detail["field"] == "body.name"
    assert detail["rule"] == "missing"
