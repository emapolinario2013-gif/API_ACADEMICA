import os
from run_agent import AIAgent
from app.core.config import AI_MODEL, AULAS_DIR
from app.core.logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """Você é um assistente acadêmico especializado no conteúdo das aulas.
Responda dúvidas com base nos materiais de estudo disponíveis na pasta de aulas.
Seja claro, didático e objetivo. Se a dúvida não estiver coberta pelo material,
diga isso honestamente em vez de inventar uma resposta."""


def list_available_pdfs() -> list[str]:
    """Retorna os nomes dos PDFs disponíveis na pasta de aulas."""
    if not os.path.isdir(AULAS_DIR):
        return []
    return [f for f in os.listdir(AULAS_DIR) if f.lower().endswith(".pdf")]


def ask_content_agent(question: str) -> str:
    """
    Envia uma dúvida ao agente de conteúdo.
    O agente tem acesso à pasta de aulas para consultar os PDFs.
    """
    pdfs = list_available_pdfs()
    if not pdfs:
        logger.warning("Nenhum PDF encontrado em: %s", AULAS_DIR)
        raise FileNotFoundError("Nenhum material de aula encontrado na pasta 'data/aulas'.")

    files_list = "\n".join(f"- {f}" for f in pdfs)
    enriched_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Materiais disponíveis em '{AULAS_DIR}':\n{files_list}\n\n"
        f"Use a ferramenta de leitura de arquivos para acessar os PDFs antes de responder."
    )

    logger.info("Consultando agente de conteúdo | pergunta: %.80s...", question)

    agent = AIAgent(
        model=AI_MODEL,
        ephemeral_system_prompt=enriched_prompt,
        quiet_mode=True,
        skip_context_files=True,
        skip_memory=True,
        max_iterations=15,
    )

    response = agent.chat(question)
    logger.info("Agente de conteúdo respondeu com sucesso.")
    return response
