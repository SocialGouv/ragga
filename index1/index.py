import sys

import logging
import chromadb


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



def get_documents(source):
    """return Document for given source(path, file_metadata)"""
    reader = SimpleDirectoryReader(
        input_dir=source.get("path"),
        required_exts=[".md"],
        recursive=True,
        exclude=source.get("exclude", []),
        file_extractor={".md": MarkdownReader(source.get("include_metas", []))},
        file_metadata=source.get("file_metadata", get_file_metadata),
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
        nodes = node_parser.get_nodes_from_documents(docs)
        chroma_collection = chroma_client.create_collection(source.get("id"))
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        logger.info(
            "index {} documents and {} nodes in {}".format(
                len(docs), len(nodes), source.get("id")
            )
        )
        index = VectorStoreIndex.from_documents(
            docs, storage_context=storage_context, service_context=service_context
        )
        logger.info(f"==> Loaded {len(docs)} docs\n\n")
    finally:
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store)
    return index



def debug_source(source):
    index = index_source(chroma_client, source)
    query_engine = index.as_query_engine()
    for query in source.get("examples", []):
        response = query_engine.query(query)
        print("\n", source.get("id"), ":", query, "\n")
        print(str(response))
        #  print((response.get_formatted_sources()))
        # print((response.source_nodes))
        print("\n-------------")

def debug_sources():
    for source in sources:
        debug_source(source)
        


node_parser = MarkdownNodeParser.from_defaults()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

# use OpenAI by default
service_context = ServiceContext.from_defaults(
    chunk_size=4096,
    # embed_model=embed_model,
    node_parser=node_parser,
    # llm=llm,
)

debug_sources()