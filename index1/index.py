import sys
import re
import json
import logging
import frontmatter
import chromadb

from datetime import date
from pathlib import Path
from typing import TypedDict, List, Callable, NotRequired

from llama_index.node_parser.simple_file import SimpleFileNodeParser
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index import ServiceContext
#from llama_index.node_parser.file.markdown import MarkdownNodeParser
from llama_index.node_parser.simple import SimpleNodeParser

from MarkdownReader import MarkdownReader, dict_string_values
from MarkdownNodeParser import MarkdownNodeParser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def get_file_metadata(filename):
    logger.debug("get_file_metadata: {}".format(filename))
    post = frontmatter.load(filename)
    return {"filename": filename, **post.metadata}


sre_files_mapping = {
    "content/support-sre-fabrique/init/.*": {
        "description": [
            "Présentation générale de la plateforme et des services technique de la fabrique"
        ],
    },
    "content/support-sre-fabrique/infrastructure/.*": {
        "description": ["Questions sur l'infrastructure technique de la fabrique"],
    },
    "content/support-sre-fabrique/standards/.*": {
        "description": [
            "Questions sur les standards techniques et conventions de la fabrique"
        ],
    },
    "content/support-sre-fabrique/workshops/.*": {
        "description": ["Workshops proposés aux développeurs(ses) de la fabrique"],
    },
}


def get_sre_metadata(filename):
    logger.debug("get_sre_metadata: {}".format(filename))
    metadata = get_file_metadata(filename)
    for path in sre_files_mapping.keys():
        if bool(re.match(path, filename)):
            return {
                **dict_string_values(sre_files_mapping[path]),
                **metadata,
            }
    return metadata


def get_last_phase(metadata):
    if metadata.get("phases"):
        metadata.get("phases").sort(key=lambda x: x.get("start", date(1970, 1, 1)))
        latest = metadata.get("phases")[-1]
        return latest.get("name")
    return None


incubators = json.loads(Path("./index1/incubators.json").read_text())


def get_se_metadata(filename):
    logger.debug("get_se_metadata: {}".format(filename))
    metadata = get_file_metadata(filename)
    result = {
        "title": metadata.get("title"),
        "description": metadata.get("mission"),
        "incubateur": incubators.get(metadata.get("incubator"), {}).get("title"),
        "phase": get_last_phase(metadata)
        # "sponsors": metadata.get("sponsors"),
    }
    return result


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


Source = TypedDict(
    "Source",
    {
        "id": str,
        "path": str,
        "file_metadata": NotRequired[Callable],
        "include_metas": NotRequired[List[str]],
        "examples": NotRequired[List[str]],
        "exclude": NotRequired[List[str]]
    },
)



sources: List[Source] = [
    # {
    #     "id": "startups-beta-gouv-sample",
    #     "topics": [
    #         "Questions concernant les startups beta.gouv",
    #         "Questions concernant les startups de la fabrique numérique",
    #     ],
    #     "path": "./content/sample",
    #     "file_metadata": get_se_metadata,
    # },
    # {
    #     "id": "startups-beta",
    #     # "topics": [
    #     #     "Questions concernant les startups beta.gouv",
    #     # ],
    #     "path": "./content/startups-beta",
    #     "file_metadata": get_se_metadata,
    #     "include_metas": ["contact"],
    #     "examples": [
    #         # "Aide dans mon parcours administratif",
    #         # "Reconnaissance d'image",
    #         # "Formation continue",
    #         # "c'est quoi MonAideCyber ?",
    #         # "cybersécurité",
    #         # "liste des startups de l'incubateur de l'écologie",
    #         # "liste des startups de l'incubateur de la DINUM",
    #         "Donnes moi une liste des startups en phase de transfert",
    #         "Donnes moi une liste des startups en phase d'investigation",
    #         "Donnes moi une liste des startups en phase d'acceleration",
    #     ],
    # },
    # {
    #     "id": "support-sre-fabrique",
    #     # "topics": [
    #     #     "Questions techniques sur le fonctionnent de l'hebergement",
    #     #     "Questions sur kubernetes et la plateforme de la fabrique",
    #     # ],
    #     "path": "./content/support-sre-fabrique",
    #     "file_metadata": get_sre_metadata,
    #     "examples": [
    #         "Comment me connecter à ma base de données",
    #         "Comment configurer mes ressources",
    #         "Demander de l'aide",
    #     ],
    # },
    {
        "id": "documentation-beta",
        # "topics": [
        #     "Questions sur la méthodologie startups d'état",
        #     "Questions sur le fonctionnement, les outils pour gérer sa startup",
        #     "Questions sur la communauté beta",
        # ],
        "path": "./content/documentation-beta",
        "exclude": ["*SUMMARY.md",".*README.md"], # bug with long content
        # "file_metadata": get_file_metadata,
        "examples": [
            "comment lancer un openlab ?",
            "comment accéder à mattermost ?",
        ],
    },
    {
        "id": "notion-fabrique",
        # "topics": [
        #     "Questions sur la méthodologie startups d'état",
        #     "Questions sur le fonctionnement, les outils pour gérer sa startup",
        #     "Questions sur la communauté beta",
        # ],
        "path": "./content/notion-fabrique",
        # "file_metadata": get_file_metadata,
        "examples": [
            "que fait la fabrique ?",
            "comment est organisée la fabrique ?",
            "quelles sont les valeurs de la fabrique ?",
        ],
    },
]


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


node_parser = MarkdownNodeParser.from_defaults()
#node_parser = SimpleFileNodeParser.from_defaults()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

# use OpenAI by default
service_context = ServiceContext.from_defaults(
    chunk_size=4096,
    # embed_model=embed_model,
    node_parser=node_parser,
    # llm=llm,
)

for source in sources:
    index = index_source(chroma_client, source)
    query_engine = index.as_query_engine()
    for query in source.get("examples", []):
        response = query_engine.query(query)
        print("\n", source.get("id"), ":", query, "\n")
        print(str(response))
        #  print((response.get_formatted_sources()))
        # print((response.source_nodes))
        print("\n-------------")
