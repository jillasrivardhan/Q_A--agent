import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

search = GoogleSerperAPIWrapper()

@tool
def web_search(query: str) -> str:
    """Search the web for information related to the user's query."""
    return search.run(query)

if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

agent = create_agent(
    model=model,
    tools=[web_search],
    checkpointer=st.session_state.memory,
    system_prompt=(
        "You are a helpful assistant that remembers previous messages "
        "and answers questions based on the information provided by the user. "
        "If you don't know the answer, say you don't know. "
        "Do not make up answers. You can also search the web using web_search "
        "when external or current information is needed."
    ),
)

st.subheader("AI CHATBOT WITH MEMORY")
st.markdown("AI agent chatbot with memory and tools")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask anything...")

if query:
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    with st.chat_message("user"):
        st.markdown(query)

    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": st.session_state.thread_id}}
    )

    answer = response["messages"][-1].content

    if isinstance(answer, list):
        answer = "\n".join(
            item.get("text", str(item)) if isinstance(item, dict)
            else str(item)
            for item in answer
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

