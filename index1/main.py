import frontmatter
from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index.readers.base import BaseReader

from llama_index.node_parser.file.markdown import MarkdownNodeParser
from MarkdownReader import MarkdownReader
from llama_index.node_parser import SentenceWindowNodeParser
import re

from llama_index.node_parser.extractors import (
    MetadataExtractor,
    TitleExtractor,
    QuestionsAnsweredExtractor,
)


def get_file_metadata(filename):
    post = frontmatter.load(filename)
    # print(post)
    # if not post.metadata:
    #   post.metadata["title"] = "xxx"
    return {"filename": filename, **post.metadata}


SreFilesMapping = {
    "content/support-sre/init/.*": {
        "topics": [
            "Présentation générale de la plateforme et des services technique de la fabrique"
        ],
    },
    "content/support-sre/infrastructure/.*": {
        "topics": ["Questions sur l'infrastructure technique de la fabrique"],
    },
    "content/support-sre/standards/.*": {
        "topics": [
            "Questions sur les standards techniques et conventions de la fabrique"
        ],
    },
    "content/support-sre/workshops/.*": {
        "topics": ["Workshops proposés aux développeurs(ses) de la fabrique"],
    },
}


def get_sre_metadata(filename):
    # print(filename)
    metadata = get_file_metadata(filename)
    for path in SreFilesMapping.keys():
        if bool(re.match(path, filename)):
            return {
                **SreFilesMapping[path],
                **metadata,
            }
    return metadata


def get_se_metadata(filename):
    metadata = get_file_metadata(filename)
    return {
        "title": metadata.get("title"),
        "description": metadata.get("mission"),
        "incubateur": metadata.get("incubator"),
        # "sponsors": metadata.get("sponsors"),
    }


def get_documents(source):
    reader = SimpleDirectoryReader(
        input_dir=source.get("path"),
        required_exts=[".md"],
        recursive=True,
        file_extractor={".md": MarkdownReader},
        file_metadata=source.get("file_metadata"),
    )
    # use MarkdownReader and split top-level paragraphs into documents
    docs = reader.load_data()
    # for doc in docs:
    #     doc.metadata = source.get("file_metadata")(doc.filename)
    return docs


sources = [
    {
        "topics": [
            "Questions concernant les startups beta.gouv",
            "Questions concernant les startups de la fabrique numérique",
        ],
        "path": "./content/startups",
        "file_metadata": get_se_metadata,
    },
    {
        "topics": [
            "Questions techniques sur le fonctionnent de l'hebergement",
            "Questions sur kubernetes et la plateforme de la fabrique",
            "Questions de support technique",
        ],
        "path": "./content/support-sre",
        "file_metadata": get_sre_metadata,
    },
]


# metadata_extractor = MetadataExtractor(
#     extractors=[
#         # TitleExtractor(nodes=5),
#         # QuestionsAnsweredExtractor(questions=3),
#     ],
# )

# text_splitter = SentenceWindowNodeParser(
#     window_size=3,
# )


# node_parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)

node_parser = MarkdownNodeParser.from_defaults()

# node_parser = SentenceWindowNodeParser.from_defaults(
#     # text_splitter=text_splitter,
#     window_size=0,
#     metadata_extractor=metadata_extractor,
# )
# assume documents are defined -> extract nodes


for source in sources:
    docs = get_documents(source)
    for doc in docs:
        nodes = node_parser.get_nodes_from_documents([doc])
        print(doc.metadata.get("filename"), len(nodes))
        # for node in nodes:
        #     print(node.metadata)
        #     print(node.relationships)
        # print(doc.metadata)
        # print(dir(doc))
        # print(doc.json())
        # print(len(nodes))
        # for node in nodes:
        # print("\n")
        # print(node)
        # print(node.metadata)

    print(f"==> Loaded {len(docs)} docs\n\n")
