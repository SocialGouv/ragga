import streamlit as st
import chromadb

from llama_index.vector_stores import ChromaVectorStore
from llama_index import VectorStoreIndex


chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_collection("startups-beta")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store)

#index = load_data()


st.set_page_config(page_title="LlamaIndex + OpenAI + Markdown = ❤️", page_icon="🐫", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.header("LlamaIndex + OpenAI + Markdown = ❤️")
st.title("Interrogez la doc de la fabrique, powered by LlamaIndex 💬🦙")
st.info("Détail des sources utilisées\n - documentation SRE\n - documentation beta.gouv\n - startups beta.gouv\n - standup fabrique\n - notion fabrique", icon="💡")


if "messages" not in st.session_state.keys():  # Initialize the chat message history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bonjour, je suis l'assistant de la fabrique, posez-moi vos questions!",
        }
    ]
# 3.4. Create the chat engine
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

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




# React to user input
if st.session_state.messages[-1]["role"] != "assistant":

    # Display user message in chat message container
  #  with st.chat_message("user"):
   #     st.markdown(user_prompt)

    # Add user message to chat history
    #st.session_state.messages.append({"role": "user", "content": user_prompt})

    #with st.spinner("Finding context..."):
    #    subquery_response, md_outputs = generative_search_engine_iter(user_prompt, index, df, K)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        streaming_response = chat_engine.stream_chat(prompt)
        full_response = ""
        for text in streaming_response.response_gen:
            full_response += text
            message_placeholder.markdown(full_response)

        #for line in md_outputs:
         #   st.markdown(line)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

if st.button("Reset chat engine's memory"):
    chat_engine.reset()