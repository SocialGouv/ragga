import streamlit as st
import chromadb

from llama_index.vector_stores import ChromaVectorStore
from llama_index import VectorStoreIndex

from sources import sources
from index import index


# chroma_client = chromadb.PersistentClient(path="./chroma_db")
# chroma_collection = chroma_client.get_collection("standup-fabrique")
# vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# index = VectorStoreIndex.from_vector_store(vector_store)

# #index = load_data()

sources_list = map(lambda source: " - [{}]({})".format(source.get("title"), source.get("url")),sources)

st.set_page_config(page_title="LlamaIndex + OpenAI + Markdown = ❤️", page_icon="🐫", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.header("LlamaIndex + OpenAI + Markdown = ❤️")
st.title("Interrogez la doc de la fabrique, powered by LlamaIndex 💬🦙")
st.info("Détail des sources utilisées : \n\n{}\n\n:warning: Pensez à préciser le nom de l'incubateur si la question lui est spécifique".format("\n".join(sources_list)), icon="💡")

if "messages" not in st.session_state.keys():  # Initialize the chat message history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bonjour, je suis l'assistant de la fabrique, posez-moi vos questions!",
        }
    ]
# 3.4. Create the chat engine
chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)

# 3.5. Prompt for user input and display message history
if prompt := st.chat_input("A votre écoute :)"):
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

if st.session_state.messages[-1]["role"] != "assistant":

    with st.chat_message("assistant"):
        with st.spinner("Je refléchis..."):
            message_placeholder = st.empty()

            streaming_response = chat_engine.stream_chat(prompt)

            # streaming_response.print_response_stream()

            full_response = ""
            for text in streaming_response.response_gen:
                full_response += text
                message_placeholder.markdown(full_response)


            st.session_state.messages.append({"role": "assistant", "content": full_response})

if st.button("Recommencer"):
    chat_engine.reset()
    del st.session_state["messages"]
