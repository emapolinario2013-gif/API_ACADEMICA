import os
from run_agent import AIAgent
from app.core.config import AI_MODEL, TAREFAS_DIR
from app.core.logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """Você é um assistente acadêmico especializado em gerenciamento de tarefas e prazos.
Consulte o documento de tarefas disponível e responda perguntas sobre:
- Quais tarefas precisam ser entregues
- Documentos que devem ser preenchidos
- Datas limite de entrega
- Tarefas próximas do prazo ou já vencidas (considere a data de hoje)

Seja preciso com datas e nomes de documentos. Priorize clareza e organização nas respostas."""


def list_task_files() -> list[str]:
    """Retorna os arquivos de tarefas disponíveis (docx, pdf, txt)."""
    if not os.path.isdir(TAREFAS_DIR):
        return []
    extensions = (".docx", ".pdf", ".txt")
    return [f for f in os.listdir(TAREFAS_DIR) if f.lower().endswith(extensions)]


def ask_tasks_agent(question: str) -> str:
    """
    Envia uma pergunta ao agente de tarefas.
    O agente consulta o documento de tarefas para responder.
    """
    files = list_task_files()
    if not files:
        logger.warning("Nenhum arquivo de tarefas encontrado em: %s", TAREFAS_DIR)
        raise FileNotFoundError("Nenhum arquivo de tarefas encontrado na pasta 'data/tarefas'.")

    files_list = "\n".join(f"- {f}" for f in files)
    enriched_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Arquivo(s) de tarefas em '{TAREFAS_DIR}':\n{files_list}\n\n"
        f"Leia o(s) arquivo(s) usando a ferramenta de leitura antes de responder."
    )

    logger.info("Consultando agente de tarefas | pergunta: %.80s...", question)

    agent = AIAgent(
        model=AI_MODEL,
        ephemeral_system_prompt=enriched_prompt,
        quiet_mode=True,
        skip_context_files=True,
        skip_memory=True,
        max_iterations=15,
    )

    response = agent.chat(question)
    logger.info("Agente de tarefas respondeu com sucesso.")
    return response
