import sys

import logging
import chromadb
import streamlit as st

from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index import ServiceContext
from llama_index.node_parser.file.markdown import MarkdownNodeParser
from llama_index.query_engine.router_query_engine import RouterQueryEngine
from llama_index.tools.query_engine import QueryEngineTool
from llama_index.selectors.pydantic_selectors import (
    PydanticMultiSelector,
    PydanticSingleSelector,
)

from MarkdownReader import MarkdownReader, dict_string_values
from sources import sources, get_file_metadata, Source

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(logging.DEBUG)

#logger.addHandler(file_handler)
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
def index_sources(sources):
    logger.info("Indexing sources...")
    indices = []
    for source in sources:
        logger.info("Indexing {}".format(source.get("id")))
        index = index_source(chroma_client, source)
       # debug_source(index, source)
        indices.append(index)
    return zip(indices, sources)

node_parser = MarkdownNodeParser.from_defaults()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

# use OpenAI by default
service_context = ServiceContext.from_defaults(
    chunk_size=512,
    # embed_model=embed_model,
    node_parser=node_parser,
    # llm=llm,
)

results = index_sources(sources)




# for (index, source) in results:


def to_query_engine_tool(index, result):
    index = result[0]
    source = result[1]
    if index == 0: # not sure why only first has tree_summarize
        query_engine = index.as_query_engine(
            response_mode="compact",
            use_async=True,
        )
    else:
        query_engine = index.as_query_engine()
    query_engine_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=source.get("query_engine_description", source.get("title"))
    )
    return query_engine_tool


query_engine_tools = map(lambda x: to_query_engine_tool(x[0], x[1]), enumerate(results))

query_engine = RouterQueryEngine(
    selector=PydanticMultiSelector.from_defaults(),
    query_engine_tools=query_engine_tools
)

res = query_engine.query(
    "Comment améliorer les performances de ma base de données ?"
)
print(res)

res = query_engine.query(
    "A la fabrique des ministères sociaux, qui contacter pour des questions juridiques ?"
)
print(res)

res = query_engine.query(
    "A la fabrique des ministères sociaux, qui contacter pour des questions techniques ?"
)
print(res)

res = query_engine.query(
    "A la fabrique des ministères sociaux, comment facturer mes prestations ?"
)
print(res)


res = query_engine.query(
    "Quelles sont les premières étapes de l'homologation RGS ?"
)
print(res)

res = query_engine.query(
    "Quels sont les points forts de la methode beta.gouv ?"
)
print(res)

# query_engines = map(to_query_engine, indices)

# query_engine_tools = map(to_query_engine_tools, indices)

# list_tool = QueryEngineTool.from_defaults(
#     query_engine=list_query_engine,
#     description="Useful for summarization questions related to Paul Graham eassy on What I Worked On.",
# )

# vector_tool = QueryEngineTool.from_defaults(
#     query_engine=vector_query_engine,
#     description="Useful for retrieving specific context from Paul Graham essay on What I Worked On.",
# )

# query_engine = RouterQueryEngine(
#     selector=PydanticMultiSelector.from_defaults(),
#     query_engine_tools=[
#         list_tool,
#         vector_tool,
#     ],
# )