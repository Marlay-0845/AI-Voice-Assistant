from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

import AI_Assistant.config as cf



llm = ChatOpenAI(
    api_key='ollama',
    base_url=cf.OLLAMA_BASE_URL_V1,
    model=cf.LLM_MODEL,
    temperature=0.2,
    max_completion_tokens=512,
    top_p=0.9
)


store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


answer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are the personal assistant.\n"
        "\n"
        "Your task:\n"
        "1. Answer questions .\n"
        "2. Follow a person's instructions.\n"
        "3. Respond in Russian only. \n"
        "4. Do not use special characters. \n"
        "5. Don't repeat the same phrase twice. \n"
        "6. Keep your response to 2-3 sentences. \n"
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    (
        "human", "{text}"
    )
])


answer_chain = (
    answer_prompt
    | llm
    | StrOutputParser()
)


chain_with_history = RunnableWithMessageHistory(
    answer_chain,
    get_session_history,
    input_messages_key="text",
    history_messages_key="chat_history"
)


def answer_to_text(text: str) -> str:
    config = {"configurable": {"session_id": "Daniil"}}
    return chain_with_history.invoke({"text": text}, config=config)