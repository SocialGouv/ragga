import sys

import logging
import chromadb
import streamlit as st

from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index import ServiceContext
from llama_index.node_parser.file.markdown import MarkdownNodeParser
from llama_index.chat_engine.types import ChatMode

from MarkdownReader import MarkdownReader
from sources import sources, get_file_metadata, Source

logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# stream_handler = logging.StreamHandler(stream=sys.stdout)
# stream_handler.setLevel(logging.DEBUG)

# file_handler = logging.FileHandler("logs.log")
# file_handler.setLevel(logging.DEBUG)

# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)


def get_filename_metadata(source, filename):
    metadata = {
        "source": source.get("description", source.get("title")),
        **source.get("file_metadata", get_file_metadata)(filename),
    }
    # print(filename, metadata)
    return metadata


def get_all_metadata(source):
    return lambda filename: get_filename_metadata(source, filename)


def get_documents(source):
    """return Document for given source(path, file_metadata)"""
    reader = SimpleDirectoryReader(
        input_dir=source.get("path"),
        required_exts=[".md"],
        recursive=True,
        exclude=source.get("exclude", []),
        file_extractor={".md": MarkdownReader(source.get("include_metas", []))},
        file_metadata=get_all_metadata(source),
    )
    # use MarkdownReader
    docs = reader.load_data()
    return docs


def index_source(chroma_client, source: Source):
    """index given source in chromadb"""
    docs = get_documents(source)
    chroma_collection = None
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
            docs,
            storage_context=storage_context,
            service_context=service_context,
            show_progress=True,
        )
        logger.info(f"==> Loaded {len(docs)} docs\n\n")
        if source.get("on_finish"):
            source.get("on_finish", lambda a, b: None)(
                docs, index
            )  # lambda for typings
    finally:
        if chroma_collection:
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


# @st.cache_resource(show_spinner=False)
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
    docs = []
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
        # nodes = node_parser.get_nodes_from_documents(docs, show_progress=True)
        chroma_collection = chroma_client.create_collection(index_id)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # todo: show nodes content length
        logger.info("index {} documents in {}".format(len(docs), index_id))
        index = VectorStoreIndex.from_documents(
            docs,
            storage_context=storage_context,
            service_context=service_context,
            show_progress=True,
        )
        logger.info(f"==> Loaded {len(docs)} docs\n\n")
        # if source.get("on_finish"):
        #     source.get("on_finish", lambda a, b: None)(docs, index) # lambda for typings
    finally:
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(
            vector_store, service_context=service_context
        )
    return index


node_parser = MarkdownNodeParser.from_defaults()

chroma_client = chromadb.PersistentClient(path="./chroma_db")


# llm = OpenAI(
#     model="gpt-3.5-turbo",
#     temperature=0.0,
# )

# use OpenAI by default
service_context = ServiceContext.from_defaults(
    chunk_size=512,
    # embed_model=embed_model,
    node_parser=node_parser,
    #   llm=llm,
    # prompt_helper=
)

index = index_sources(sources)


if __name__ == "__main__":
    # query
    chat = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT,
        verbose=True,
        similarity_top_k=5,
    )
    chat.chat_repl()
