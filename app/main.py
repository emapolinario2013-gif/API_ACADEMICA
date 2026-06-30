from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1 import content, tasks
from app.core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="API de Inteligência Artificial Acadêmica",
    description=(
        "API que disponibiliza dois serviços de IA para suporte acadêmico:\n\n"
        "- **/v1/ask** — Tire dúvidas sobre o conteúdo das aulas (consulta PDFs)\n"
        "- **/v1/tasks** — Consulte tarefas, documentos e prazos de entrega\n\n"
        "Autenticação: envie sua chave no header `X-API-Key`."
    ),
    version="1.0.0",
    contact={"name": "Trabalho Final — Construção de APIs para IA"},
)

app.include_router(content.router, prefix="/v1", tags=["Conteúdo das Aulas"])
app.include_router(tasks.router, prefix="/v1", tags=["Tarefas e Prazos"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Exceção não tratada em %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno inesperado no servidor."},
    )


@app.get("/", tags=["Status"])
async def health_check():
    """Verifica se a API está no ar."""
    return {"status": "ok", "version": "1.0.0"}
