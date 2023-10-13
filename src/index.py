import sys

import logging
import chromadb
import streamlit as st

from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index import ServiceContext
from llama_index.node_parser.file.markdown import MarkdownNodeParser


from MarkdownReader import MarkdownReader, dict_string_values
from sources import sources, get_file_metadata, Source

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def get_all_metadata(source):
    return lambda filename: {
        **source.get("file_metadata", get_file_metadata)(filename),
        "source": source.get("description", source.get("title"))
    }

def get_documents(source):
    """return Document for given source(path, file_metadata)"""
    reader = SimpleDirectoryReader(
        input_dir=source.get("path"),
        required_exts=[".md"],
        recursive=True,
        exclude=source.get("exclude", []),
        file_extractor={".md": MarkdownReader(source.get("include_metas", []))},
        file_metadata=get_all_metadata(source)
    )
    # use MarkdownReader
    docs = reader.load_data()
    return docs



def index_source(chroma_client, source: Source):
    """index given source in chromadb"""
    docs = get_documents(source)
    try:
        chroma_collection = chroma_client.get_collection(source.get("id"))
        logger.info("==> Collection {} already exist\n\n".format(source.get("id")))
    except ValueError:
        nodes = node_parser.get_nodes_from_documents(docs, show_progress=True)
        chroma_collection = chroma_client.create_collection(source.get("id"))
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # todo: show nodes content length
        logger.info(
            "index {} documents and {} nodes in {}".format(
                len(docs), len(nodes), source.get("id")
            )
        )
        index = VectorStoreIndex.from_documents(
            docs, storage_context=storage_context, service_context=service_context, show_progress=True
        )
        logger.info(f"==> Loaded {len(docs)} docs\n\n")
        if source.get("on_finish"):
            source.get("on_finish", lambda a, b: None)(docs, index) # lambda for typings
    finally:
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store)

    return index



def debug_source(index, source):
    query_engine = index.as_query_engine()
    for query in source.get("examples", []):
        response = query_engine.query(query)
        print("\n", source.get("id"), ":", query, "\n")
        print(str(response))
        #  print((response.get_formatted_sources()))
        # print((response.source_nodes))
        print("\n-------------")

#@st.cache_resource(show_spinner=False) 
def index_sources1(sources):
    logger.info("Indexing sources...")
    indices = []
    for source in sources:
        logger.info("Indexing {}".format(source.get("id")))
        index = index_source(chroma_client, source)
       # debug_source(index, source)
        indices.append(index)
    return list(zip(indices, sources))


def index_sources(sources):
    logger.info("Indexing sources...")
    docs=[]
    index_id = "all_docs"
    chroma_collection = None
    for source in sources:
        sourceDocs = get_documents(source)
        docs += sourceDocs
        if source.get("additional_documents"):
            docs += source.get("additional_documents")(sourceDocs)
    try:
        chroma_collection = chroma_client.get_collection(index_id)
        logger.info(f"==> Collection {index_id} already exist\n\n")
    except ValueError:
        #nodes = node_parser.get_nodes_from_documents(docs, show_progress=True)
        chroma_collection = chroma_client.create_collection(index_id)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # todo: show nodes content length
        logger.info(
            "index {} documents in {}".format(
                len(docs), index_id
            )
        )
        index = VectorStoreIndex.from_documents(
            docs, storage_context=storage_context, service_context=service_context, show_progress=True
        )
        logger.info(f"==> Loaded {len(docs)} docs\n\n")
        # if source.get("on_finish"):
        #     source.get("on_finish", lambda a, b: None)(docs, index) # lambda for typings
    finally:
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store)
    return index



node_parser = MarkdownNodeParser.from_defaults()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

# use OpenAI by default
service_context = ServiceContext.from_defaults(
    chunk_size=512,
    # embed_model=embed_model,
    node_parser=node_parser,
    # llm=llm,
)

index = index_sources(sources)

chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)

chat_engine.stream_chat("C'est quoi domifa ?").print_response_stream()

while 1:
    print("\n\n")
    user_input = input('Prompt : ')
    chat_engine.stream_chat(user_input).print_response_stream()


# chat_engine.stream_chat("Qui contacter pour des questions relatives au RGPD ?").print_response_stream()
# chat_engine.stream_chat("Quelles sont les valeurs cardinales de beta.gouv ?").print_response_stream()

