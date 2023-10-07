import sys
import re
import json
import logging
import frontmatter
import chromadb

from datetime import date
from pathlib import Path

from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index import ServiceContext
from llama_index.node_parser.file.markdown import MarkdownNodeParser

from MarkdownReader import MarkdownReader, dict_string_values

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def get_file_metadata(filename):
    post = frontmatter.load(filename)
    return {"filename": filename, **post.metadata}


sre_files_mapping = {
    "content/support-sre/init/.*": {
        "description": [
            "Présentation générale de la plateforme et des services technique de la fabrique"
        ],
    },
    "content/support-sre/infrastructure/.*": {
        "description": ["Questions sur l'infrastructure technique de la fabrique"],
    },
    "content/support-sre/standards/.*": {
        "description": [
            "Questions sur les standards techniques et conventions de la fabrique"
        ],
    },
    "content/support-sre/workshops/.*": {
        "description": ["Workshops proposés aux développeurs(ses) de la fabrique"],
    },
}


def get_sre_metadata(filename):
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
        file_extractor={".md": MarkdownReader(source.get("include_metas", []))},
        file_metadata=source.get("file_metadata"),
    )
    # use MarkdownReader
    docs = reader.load_data()
    return docs


sources = [
    # {
    #     "id": "startups-beta-gouv-sample",
    #     "topics": [
    #         "Questions concernant les startups beta.gouv",
    #         "Questions concernant les startups de la fabrique numérique",
    #     ],
    #     "path": "./content/sample",
    #     "file_metadata": get_se_metadata,
    # },
    {
        "id": "startups-beta-gouv",
        # "topics": [
        #     "Questions concernant les startups beta.gouv",
        # ],
        "path": "./content/startups",
        "file_metadata": get_se_metadata,
        "include_metas": ["contact"],
        "examples": [
            # "Aide dans mon parcours administratif",
            # "Reconnaissance d'image",
            # "Formation continue",
            # "c'est quoi MonAideCyber ?",
            # "cybersécurité",
            # "liste des startups de l'incubateur de l'écologie",
            # "liste des startups de l'incubateur de la DINUM",
            "Liste des startups en phase de transfert",
            "Liste des startups en phase d'investigation",
            "Liste des startups en phase d'acceleration",
        ],
    },
    {
        "id": "support-techique-sre-socialgouv",
        # "topics": [
        #     "Questions techniques sur le fonctionnent de l'hebergement",
        #     "Questions sur kubernetes et la plateforme de la fabrique",
        # ],
        "path": "./content/support-sre",
        "file_metadata": get_sre_metadata,
        "examples": [
            "Me connecter à ma base de données",
            "Configurer mes ressources",
            "Demander de l'aide",
        ],
    },
]


def index_source(chroma_client, source):
    """index given source in chromadb"""
    docs = get_documents(source)
    try:
        chroma_collection = chroma_client.get_collection(source.get("id"))
        logging.info("==> Collection {} already exist\n\n".format(source.get("id")))
    except ValueError:
        nodes = node_parser.get_nodes_from_documents(docs)
        chroma_collection = chroma_client.create_collection(source.get("id"))
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        logging.info(
            "index {} documents and {} nodes in {}".format(
                len(docs), len(nodes), source.get("id")
            )
        )
        index = VectorStoreIndex.from_documents(
            docs, storage_context=storage_context, service_context=service_context
        )
        logging.info(f"==> Loaded {len(docs)} docs\n\n")
        print("\n\n")
    finally:
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store)
    return index


node_parser = MarkdownNodeParser.from_defaults()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

service_context = ServiceContext.from_defaults(
    # chunk_size=512,
    # embed_model=embed_model,
    node_parser=node_parser,
    # llm=llm,
)

for source in sources:
    index = index_source(chroma_client, source)
    query_engine = index.as_query_engine()
    for query in source.get("examples"):
        response = query_engine.query(query)
        print("\n", source.get("id"), ":", query)
        print(str(response))
        print((response.get_formatted_sources()))
        # print((response.source_nodes))
        print("\n-------------\n")
