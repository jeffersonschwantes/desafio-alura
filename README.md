# 🎙️ Simulador de Entrevistas Técnicas com IA 🎙️

Este projeto foi desenvolvido como parte do desafio da **Imersão IA 2025 da Alura, FIAP, PM3 e Google**.

## 🎯 Objetivo Principal

O objetivo deste projeto é fornecer uma ferramenta interativa para que desenvolvedores, estudantes de tecnologia e qualquer pessoa que esteja se preparando para processos seletivos na área de TI possam praticar para entrevistas técnicas. A ideia é simular um cenário de entrevista, onde o usuário pode responder a perguntas específicas de uma tecnologia ou conceito e receber feedback instantâneo e construtivo gerado por Inteligência Artificial.

## 🚀 Para que serve?

Este simulador serve como um ambiente de treinamento seguro e eficaz, ajudando os usuários a:

* **Praticar Respostas:** Articular e refinar suas respostas para perguntas técnicas comuns em diversas áreas da tecnologia.
* **Receber Feedback Imediato:** Obter uma análise da sua resposta, destacando pontos fortes e áreas que necessitam de melhoria, algo que raramente é disponibilizado após uma entrevista real.
* **Identificar Lacunas de Conhecimento:** Perceber quais tópicos precisam de mais estudo ou aprofundamento.
* **Aumentar a Confiança:** Familiarizar-se com a dinâmica de uma entrevista técnica e ganhar mais segurança para enfrentar os desafios reais.
* **Aprender de Forma Personalizada:** O feedback é gerado com base na sua resposta específica, tornando o aprendizado mais direcionado.

## ✨ Como Funciona?

O simulador utiliza um sistema multiagente construído com o **Google Agent Development Kit (ADK)** e o poder do modelo de linguagem **Google Gemini (`gemini-1.5-flash-latest`)**. O fluxo é o seguinte:

1.  **Definição do Cenário:** O usuário escolhe o **TÓPICO** da entrevista (ex: Python, JavaScript, SQL, Machine Learning) e o **NÍVEL** de dificuldade (ex: Iniciante, Intermediário, Avançado).
2.  **Agente Entrevistador (IA):** Um agente de IA especializado formula uma pergunta técnica relevante com base no tópico e nível definidos.
3.  **Resposta do Usuário:** O usuário digita sua resposta à pergunta.
4.  **Agente Avaliador (IA):** Outro agente de IA analisa a resposta do usuário, avaliando critérios como correção técnica, clareza, profundidade e relevância. Ele fornece um resumo conciso da avaliação.
5.  **Agente de Feedback Construtivo (IA):** Um terceiro agente, atuando como um "coach de carreira", utiliza a pergunta, a resposta do usuário e a avaliação para gerar um feedback detalhado, encorajador e com sugestões práticas para melhoria.
6.  **Ciclo Interativo:** O processo se repete para um número configurado de perguntas, permitindo uma sessão de prática completa.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Google Gemini API** (especificamente o modelo `gemini-1.5-flash-latest`)
* **Google Agent Development Kit (ADK)**
* Bibliotecas Python: `google-genai`, `google-adk`, `ipython` (para `display` e `Markdown` no Colab).

## ⚙️ Configuração e Uso

1.  **Pré-requisitos:**
    * Python 3.7 ou superior.
    * Uma Chave de API do Google Gemini.

2.  **Instalação de Dependências:**
    ```bash
    pip install google-genai google-adk ipython
    ```

3.  **Configuração da API Key:**
    * **Google Colab:** Configure sua `GOOGLE_API_KEY` nos "Secrets" do Colab.
    * **Ambiente Local:** Exporte sua chave como uma variável de ambiente:
        ```bash
        export GOOGLE_API_KEY="SUA_API_KEY_AQUI"
        ```
        (Ou modifique o código para inserir a chave diretamente, o que é menos recomendado por segurança).

4.  **Execução:**
    * Se estiver usando o Google Colab, cole o código em uma célula e execute-a.
    * Se estiver em um ambiente local, salve o código como um arquivo `.py` (ex: `simulador_entrevista.py`) e execute:
        ```bash
        python simulador_entrevista.py
        ```
    * Siga as instruções no console para iniciar a simulação.

## 🔮 Próximos Passos e Melhorias (Sugestões)

* Implementar a ferramenta `Google Search` para que os agentes possam buscar informações mais recentes ou validar respostas complexas.
* Adicionar um "Agente de Simulação de Comportamento" para variar o estilo do entrevistador (ex: mais amigável, mais desafiador).
* Salvar o histórico da entrevista para revisão posterior.
* Criar uma interface gráfica simples (ex: com Streamlit ou Flask).

---

Sinta-se à vontade para usar, modificar e contribuir com este projeto!
