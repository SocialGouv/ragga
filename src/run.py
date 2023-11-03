import random
import streamlit as st
import chromadb
import logging
import sys

from llama_index.vector_stores import ChromaVectorStore
from llama_index import VectorStoreIndex
from llama_index.chat_engine.types import ChatMode
from sources import sources
from index import index

logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# stream_handler = logging.StreamHandler(stream=sys.stdout)
# stream_handler.setLevel(logging.DEBUG)

# file_handler = logging.FileHandler("logs.log")
# file_handler.setLevel(logging.DEBUG)

# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

# chroma_client = chromadb.PersistentClient(path="./chroma_db")
# chroma_collection = chroma_client.get_collection("standup-fabrique")
# vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# index = VectorStoreIndex.from_vector_store(vector_store)

# #index = load_data()

sources_list = map(
    lambda source: " - [{}]({})".format(source.get("title"), source.get("url")), sources
)

st.set_page_config(
    page_title="LlamaIndex + OpenAI + Markdown",
    page_icon="🐫",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.header("LlamaIndex + OpenAI + Markdown")
st.title(
    "Interrogez la doc de la fabrique des ministères sociaux",
)
st.info(
    "Détail des sources utilisées : \n\n{}\n\n:warning: Bot expérimental, retours bienvenus sur [sur GitHub](https://github.com/SocialGouv/ragga/issues/new)\n\nVoir des [exemples de réponses](https://pad.numerique.gouv.fr/751pO3ShQU-cZ3o-gQiYpA)".format(
        "\n".join(sources_list)
    ),
    icon="💡",
)

if "messages" not in st.session_state.keys():  # Initialize the chat message history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bonjour, je suis l'assistant de la fabrique, posez-moi vos questions!",
        }
    ]

if "chat_engine" not in st.session_state:
    # set the initial default value of the slider widget
    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT, verbose=True, similarity_top_k=5
    )
    st.session_state["chat_engine"] = chat_engine

waiters = [
    "Je refléchis...",
    "Hummmm laissez moi chercher...",
    "Je cherche des réponses...",
]

input = st.chat_input("A votre écoute :)")

if prompt := input:
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3.6. Pass query to chat engine and display response
# If last message is not from assistant, generate a new response
# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Je refléchis..."):
#             response = chat_engine.stream_chat(prompt)
#             for token in response.response_gen:
#                 #print(token, end="")
#                 st.write(token, end="")
#             message = {"role": "assistant", "content": response.response}
#             st.session_state.messages.append(message)  # Add response to message history


#
# query_engine = index.as_query_engine(streaming=True)
# response = query_engine.query("What did the author do growing up?")
# response.print_response_stream()
#


waiters = [
    "Je refléchis...",
    "Hummmm laissez moi chercher...",
    "Je cherche des réponses...",
]


def get_source_link(description: str, filename):
    source = [src for src in sources if src.get("description") == description]
    if source:
        if source[0].get("get_url"):
            return source[0].get("get_url", lambda a: a)(filename)
        return source[0].get("url")
    return None


def get_source_links(source_nodes):
    sources = filter(
        lambda a: True,
        set(
            map(
                lambda node: get_source_link(
                    filename=node.metadata.get("filename"),
                    description=node.metadata.get("source"),
                ),
                source_nodes,
            )
        ),
    )
    return "\n".join(map(lambda row: f" - {row}", sources))


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        message = str(random.choice(waiters))
        with st.spinner(message):
            message_placeholder = st.empty()
            source_nodes = []

            streaming_response = st.session_state["chat_engine"].stream_chat(prompt)

            # streaming_response.print_response_stream()

            full_response = ""
            source_nodes += streaming_response.source_nodes

            for text in streaming_response.response_gen:
                full_response += text
                message_placeholder.markdown(full_response)

            str_sources = get_source_links(source_nodes)
            if str_sources:
                full_response += "\n\nSources utilisées : \n\n" + str_sources
                message_placeholder.markdown(full_response)
            # print("str_sources", str_sources)
            #   full_response += f"\n\n{str_sources}"
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
