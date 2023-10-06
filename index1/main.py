from llama_index import SimpleDirectoryReader
import json
from pathlib import Path
import frontmatter

from llama_index.node_parser.extractors import (
    MetadataExtractor,
    TitleExtractor,
    QuestionsAnsweredExtractor,
)


def get_file_metadata(filename):
    post = frontmatter.load(filename)
    print(post)
    if not post.metadata:
        post.metadata["title"] = "xxx"
    return {"filename": filename} | post.metadata


def get_se_metadata(filename):
    metadata = get_file_metadata(filename)
    return {
        "title": metadata.get("title"),
        "description": metadata.get("mission"),
        "incubateur": metadata.get("incubator"),
        "sponsors": metadata.get("sponsors"),
        "topics": [
            "startups beta gouv",
            "liste des projets, services et produits de l'écosystème beta.gouv",
        ],
    }


def get_documents(source):
    reader = SimpleDirectoryReader(
        input_dir=source.get("path"),
        required_exts=[".md"],
        recursive=True,
        file_metadata=source.get("file_metadata"),
    )
    # use MarkdownReader and split top-level paragraphs into documents
    docs = reader.load_data()
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
        "file_metadata": get_file_metadata,
    },
]


metadata_extractor = MetadataExtractor(
    extractors=[
        TitleExtractor(nodes=5),
        # QuestionsAnsweredExtractor(questions=3),
    ],
)

text_splitter = TokenTextSplitter(separator=" ", chunk_size=512, chunk_overlap=128)

node_parser = SimpleNodeParser.from_defaults(
    text_splitter=text_splitter,
    metadata_extractor=metadata_extractor,
)
# assume documents are defined -> extract nodes


for source in sources:
    docs = get_documents(source)
    for doc in docs:
        print("\n\n")
        print(doc.doc_id)
        print(doc.metadata)
        print(dir(doc))
        print(doc.json())
        nodes = node_parser.get_nodes_from_documents(documents)
        print(nodes)

print(f"Loaded {len(docs)} docs")
