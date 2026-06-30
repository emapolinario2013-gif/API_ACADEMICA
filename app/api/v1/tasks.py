from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.agents.tasks_agent import ask_tasks_agent, list_task_files
from app.core.security import require_api_key
from app.core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class TaskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Pergunta sobre tarefas, documentos ou prazos.",
        examples=["Quais tarefas vencem essa semana?"],
    )


class TaskResponse(BaseModel):
    answer: str
    files_consulted: list[str]


@router.post(
    "/tasks",
    response_model=TaskResponse,
    summary="Consulte tarefas e prazos de entrega",
    description=(
        "Envia uma pergunta ao agente de IA, que consulta o documento de tarefas "
        "e responde com informações sobre entregas, documentos e datas limite."
    ),
)
async def ask_tasks(
    body: TaskRequest,
    _: str = Depends(require_api_key),
):
    try:
        answer = ask_tasks_agent(body.question)
        files = list_task_files()
        return TaskResponse(answer=answer, files_consulted=files)

    except FileNotFoundError as exc:
        logger.error("Arquivo de tarefas não encontrado: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except Exception as exc:
        logger.exception("Erro inesperado no endpoint /tasks: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a consulta. Tente novamente.",
        )
