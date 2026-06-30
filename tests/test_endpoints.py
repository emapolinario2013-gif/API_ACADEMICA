"""
Testes básicos dos endpoints da API.
Execute com: pytest tests/ -v
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)
VALID_KEY = "chave-de-teste"


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setattr("app.core.security.API_SECRET_KEY", VALID_KEY)


# --- Testes de autenticação ---

def test_ask_sem_chave_retorna_401():
    resp = client.post("/v1/ask", json={"question": "O que é REST?"})
    assert resp.status_code == 401


def test_tasks_sem_chave_retorna_401():
    resp = client.post("/v1/tasks", json={"question": "Quais tarefas vencem essa semana?"})
    assert resp.status_code == 401


def test_ask_chave_invalida_retorna_401():
    resp = client.post(
        "/v1/ask",
        json={"question": "O que é REST?"},
        headers={"X-API-Key": "chave-errada"},
    )
    assert resp.status_code == 401


# --- Testes de validação de dados ---

def test_ask_pergunta_muito_curta_retorna_422():
    resp = client.post(
        "/v1/ask",
        json={"question": "Oi"},
        headers={"X-API-Key": VALID_KEY},
    )
    assert resp.status_code == 422


def test_tasks_pergunta_muito_curta_retorna_422():
    resp = client.post(
        "/v1/tasks",
        json={"question": "Ok"},
        headers={"X-API-Key": VALID_KEY},
    )
    assert resp.status_code == 422


def test_ask_sem_body_retorna_422():
    resp = client.post("/v1/ask", headers={"X-API-Key": VALID_KEY})
    assert resp.status_code == 422


# --- Testes funcionais (com mock do agente) ---

def test_ask_retorna_resposta_valida():
    with patch("app.api.v1.content.ask_content_agent", return_value="REST é um estilo arquitetural."), \
         patch("app.api.v1.content.list_available_pdfs", return_value=["aula1.pdf"]):
        resp = client.post(
            "/v1/ask",
            json={"question": "O que é uma API REST?"},
            headers={"X-API-Key": VALID_KEY},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "sources_available" in data
    assert data["answer"] == "REST é um estilo arquitetural."


def test_tasks_retorna_resposta_valida():
    with patch("app.api.v1.tasks.ask_tasks_agent", return_value="A tarefa X vence dia 30/06."), \
         patch("app.api.v1.tasks.list_task_files", return_value=["tarefas.docx"]):
        resp = client.post(
            "/v1/tasks",
            json={"question": "Quais tarefas vencem essa semana?"},
            headers={"X-API-Key": VALID_KEY},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "files_consulted" in data


def test_ask_sem_pdfs_retorna_404():
    with patch("app.api.v1.content.ask_content_agent", side_effect=FileNotFoundError("Sem PDFs")):
        resp = client.post(
            "/v1/ask",
            json={"question": "O que é autenticação JWT?"},
            headers={"X-API-Key": VALID_KEY},
        )
    assert resp.status_code == 404


def test_tasks_sem_arquivo_retorna_404():
    with patch("app.api.v1.tasks.ask_tasks_agent", side_effect=FileNotFoundError("Sem tarefas")):
        resp = client.post(
            "/v1/tasks",
            json={"question": "Quais tarefas vencem essa semana?"},
            headers={"X-API-Key": VALID_KEY},
        )
    assert resp.status_code == 404


# --- Health check ---

def test_health_check():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
