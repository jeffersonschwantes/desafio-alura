# Etapa 0: Instalar as bibliotecas necessárias
# Descomente as linhas abaixo se estiver executando em um ambiente que não seja o Colab
# ou se as bibliotecas não estiverem instaladas.
# !pip install -q google-genai
# !pip install -q google-adk

import os
from google.colab import userdata # Para Colab
from google import genai
from google.genai import types as genai_types
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
# from google.adk.tools import Google Search # Descomente se quiser adicionar a ferramenta de busca
import textwrap
from IPython.display import display, Markdown
import warnings

warnings.filterwarnings("ignore")

# Etapa 1: Configurar a API Key do Google Gemini
# Certifique-se de ter sua GOOGLE_API_KEY configurada no ambiente ou no Colab Userdata
try:
    os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')
except Exception as e:
    print(f"Erro ao obter GOOGLE_API_KEY do userdata do Colab: {e}")
    print("Por favor, configure sua GOOGLE_API_KEY manualmente se não estiver usando o Colab.")
    # Exemplo: os.environ["GOOGLE_API_KEY"] = "SUA_API_KEY_AQUI"

if not os.environ.get("GOOGLE_API_KEY"):
    print("A GOOGLE_API_KEY não foi encontrada. O programa não poderá funcionar.")
    exit()

# Etapa 2: Configurar o cliente da SDK do Gemini
try:
    client = genai.Client()
    MODEL_ID = "gemini-1.5-flash-latest" # Usando um modelo mais recente e capaz
except Exception as e:
    print(f"Erro ao inicializar o cliente GenAI: {e}")
    print("Verifique sua API Key e configurações de rede.")
    exit()

# Etapa 3: Funções Auxiliares (do arquivo agentes.py)
def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user_interview_sim", session_id="session_interview")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = genai_types.Content(role="user", parts=[genai_types.Part(text=message_text)])

    final_response = ""
    for event in runner.run(user_id="user_interview_sim", session_id="session_interview", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response.strip()

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# --- AGENTES DO SIMULADOR DE ENTREVISTA ---

######################################
# --- Agente 1: Entrevistador --- #
######################################
def agente_entrevistador(topic: str, difficulty: str) -> str:
    entrevistador = Agent(
        name="agente_entrevistador",
        model=MODEL_ID,
        # tools=[Google Search], # Opcional: para buscar perguntas atuais
        instruction="""Você é um experiente entrevistador técnico.
        Sua tarefa é, com base no TÓPICO e NÍVEL fornecidos, formular UMA ÚNICA pergunta de entrevista clara e concisa.
        A pergunta deve ser específica e testar conhecimento prático ou teórico relevante.
        Retorne APENAS a pergunta, sem saudações, introduções ou qualquer texto adicional.
        Seja criativo e evite perguntas genéricas demais.
        Exemplo de entrada:
        TÓPICO: Python
        NÍVEL: Intermediário
        Exemplo de saída:
        Explique o que são Decorators em Python e forneça um exemplo prático de seu uso.
        """,
        description="Agente que formula perguntas para entrevistas técnicas."
    )
    entrada_agente = f"TÓPICO: {topic}\nNÍVEL: {difficulty}"
    pergunta = call_agent(entrevistador, entrada_agente)
    return pergunta

################################################
# --- Agente 2: Avaliador de Respostas --- #
################################################
def agente_avaliador(topic: str, question: str, user_answer: str) -> str:
    avaliador = Agent(
        name="agente_avaliador",
        model=MODEL_ID,
        # tools=[Google Search], # Opcional: para verificar fatos ou aprofundar na avaliação
        instruction="""Você é um avaliador técnico sênior e justo.
        Com base na PERGUNTA, RESPOSTA DO USUÁRIO e TÓPICO fornecidos, sua tarefa é analisar a resposta do usuário.
        Avalie a correção técnica, clareza, profundidade do conhecimento e a relevância da resposta para a pergunta.
        Identifique os pontos fortes e fracos de forma objetiva.
        Forneça um resumo conciso da sua avaliação em no máximo 3-4 frases curtas.
        Não adicione introduções ou despedidas. Foque na essência da avaliação.
        Exemplo de entrada:
        TÓPICO: Python
        PERGUNTA: O que é o GIL em Python e quais suas implicações?
        RESPOSTA DO USUÁRIO: É um bloqueio que não deixa as threads rodarem em paralelo.
        Exemplo de saída:
        A resposta identifica corretamente o GIL como um bloqueio, mas carece de profundidade sobre suas implicações no paralelismo real e em tarefas CPU-bound vs I/O-bound. A clareza é razoável, mas a completude é baixa.
        """,
        description="Agente que avalia respostas de entrevistas técnicas."
    )
    entrada_agente = f"TÓPICO: {topic}\nPERGUNTA: {question}\nRESPOSTA DO USUÁRIO: {user_answer}"
    avaliacao = call_agent(avaliador, entrada_agente)
    return avaliacao

####################################################
# --- Agente 3: Fornecedor de Feedback Construtivo --- #
####################################################
def agente_feedback(question: str, user_answer: str, evaluation_summary: str) -> str:
    feedback_provider = Agent(
        name="agente_feedback_construtivo",
        model=MODEL_ID,
        instruction="""Você é um coach de carreira e especialista em entrevistas técnicas, com um tom amigável e encorajador.
        Seu objetivo é ajudar o candidato a melhorar. Com base na PERGUNTA, RESPOSTA DO USUÁRIO e no RESUMO DA AVALIAÇÃO fornecidos:
        1. Comece com uma frase positiva, reconhecendo o esforço do candidato.
        2. Destaque os pontos positivos da resposta, conectando-os com o resumo da avaliação se pertinente.
        3. Para cada ponto fraco ou área de melhoria identificada na avaliação, explique claramente o porquê é importante e ofereça sugestões específicas, exemplos de como a resposta poderia ser aprimorada, ou o que estudar. Use bullet points para clareza nas sugestões.
        4. Mantenha um tom positivo e educativo. O objetivo é construir confiança e guiar o aprendizado.
        5. Se a resposta foi excelente, explique o que a tornou assim e como manter esse nível em outras perguntas.
        Evite repetir integralmente a pergunta ou a resposta do usuário. Foque no conselho prático e acionável.
        Finalize com uma nota de encorajamento.
        """,
        description="Agente que fornece feedback construtivo sobre o desempenho em entrevistas."
    )
    entrada_agente = f"PERGUNTA: {question}\nRESPOSTA DO USUÁRIO: {user_answer}\nRESUMO DA AVALIAÇÃO: {evaluation_summary}"
    feedback_detalhado = call_agent(feedback_provider, entrada_agente)
    return feedback_detalhado

# --- LÓGICA PRINCIPAL DO SIMULADOR DE ENTREVISTA ---
def iniciar_simulador_entrevista():
    display(Markdown("---"))
    display(Markdown("## 🎙️ Bem-vindo ao Simulador de Entrevistas Técnicas com IA! 🎙️"))
    display(Markdown("---"))

    topic = input("📚 Sobre qual TÓPICO de tecnologia você gostaria de ser entrevistado? (ex: Python, JavaScript, SQL, Machine Learning): ")
    difficulty = input("🏋️ Qual nível de dificuldade você prefere? (ex: Iniciante, Intermediário, Avançado): ")

    if not topic or not difficulty:
        display(Markdown("> ❌ Tópico e dificuldade são obrigatórios para iniciar. Encerrando simulador."))
        return

    # MODIFICAÇÃO AQUI: Permitir que o usuário defina o número de perguntas
    while True:
        try:
            num_questions_str = input("🔢 Quantas perguntas você gostaria de responder nesta simulação? (ex: 3, 5): ")
            num_questions = int(num_questions_str)
            if num_questions > 0 and num_questions <= 10: # Limite razoável para não sobrecarregar
                break
            else:
                display(Markdown("> ⚠️ Por favor, insira um número entre 1 e 10."))
        except ValueError:
            display(Markdown("> ❌ Entrada inválida. Por favor, insira um número inteiro."))

    display(Markdown(f"\nOk! Preparando uma entrevista sobre **{topic}** (Nível: **{difficulty}**) com **{num_questions}** pergunta(s)."))
    display(Markdown("---"))

    for i in range(num_questions):
        display(Markdown(f"### 📝 Pergunta {i+1} de {num_questions}"))

        # 1. Gerar Pergunta
        display(Markdown("> Gerando pergunta... Aguarde um momento."))
        question = agente_entrevistador(topic, difficulty)
        if not question:
            display(Markdown("> ❌ Não foi possível gerar uma pergunta. Tente novamente mais tarde."))
            continue
        display(Markdown(f"**🎤 Entrevistador IA:**\n>{question}"))

        # 2. Obter Resposta do Usuário
        user_answer = input("\n✍️ Sua resposta: ")
        if not user_answer:
            user_answer = "(Nenhuma resposta fornecida)"
        display(Markdown("---"))

        # 3. Avaliar Resposta
        display(Markdown("> Avaliando sua resposta... Aguarde um momento."))
        evaluation_summary = agente_avaliador(topic, question, user_answer)
        if not evaluation_summary:
            display(Markdown("> ❌ Não foi possível obter uma avaliação da resposta."))
        else:
            display(Markdown(f"**🧐 Avaliador IA (Resumo):**"))
            display(to_markdown(evaluation_summary))
        display(Markdown("---"))

        # 4. Fornecer Feedback Construtivo
        display(Markdown("> Gerando feedback detalhado... Aguarde um momento."))
        detailed_feedback = agente_feedback(question, user_answer, evaluation_summary if evaluation_summary else "Avaliação não disponível.")
        if not detailed_feedback:
            display(Markdown("> ❌ Não foi possível gerar o feedback detalhado."))
        else:
            display(Markdown(f"**💡 Coach de Carreira IA (Feedback):**"))
            display(to_markdown(detailed_feedback))
        display(Markdown("---"))

        if i < num_questions - 1:
            input("Pressione Enter para a próxima pergunta...")
            display(Markdown("\n---\n"))

    display(Markdown("## 🎉 Simulação de Entrevista Concluída! 🎉"))
    display(Markdown("Continue praticando e boa sorte em suas entrevistas reais!"))
    display(Markdown("---"))

if __name__ == "__main__":
    # Este bloco permite executar o script diretamente.
    # Se estiver no Colab, você pode chamar a função iniciar_simulador_entrevista() em uma célula.
    try:
        iniciar_simulador_entrevista()
    except Exception as e:
        display(Markdown(f"> ❌ Ocorreu um erro inesperado durante a simulação: {e}"))
