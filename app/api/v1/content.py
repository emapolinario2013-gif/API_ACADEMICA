from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.agents.content_agent import ask_content_agent, list_available_pdfs
from app.core.security import require_api_key
from app.core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class ContentRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Dúvida sobre o conteúdo das aulas.",
        examples=["O que é uma API REST?"],
    )


class ContentResponse(BaseModel):
    answer: str
    sources_available: list[str]


@router.post(
    "/ask",
    response_model=ContentResponse,
    summary="Tire dúvidas sobre o conteúdo das aulas",
    description=(
        "Envia uma pergunta ao agente de IA, que consulta os PDFs de aula "
        "e retorna uma resposta baseada no material disponível."
    ),
)
async def ask_content(
    body: ContentRequest,
    _: str = Depends(require_api_key),
):
    try:
        answer = ask_content_agent(body.question)
        pdfs = list_available_pdfs()
        return ContentResponse(answer=answer, sources_available=pdfs)

    except FileNotFoundError as exc:
        logger.error("Material não encontrado: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except Exception as exc:
        logger.exception("Erro inesperado no endpoint /ask: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a pergunta. Tente novamente.",
        )
