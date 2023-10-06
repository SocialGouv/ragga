from llama_index import SimpleDirectoryReader
import json
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from pathlib import Path
import frontmatter

# from unstructured.partition.auto import partition
# import commonmark
# import frontmatter

# url = "https://raw.githubusercontent.com/Unstructured-IO/unstructured/main/LICENSE.md"
# elements = partition(url=url)
# elements = partition(url=url, content_type="text/markdown")

required_exts = [".md"]


def get_file_metadata(filename):
    post = frontmatter.load(filename)
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
        required_exts=required_exts,
        recursive=True,
        file_metadata=source.get("file_metadata"),
    )
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
    }
]


for source in sources:
    docs = get_documents(source)
    for doc in docs:
        print(doc.doc_id)
        print(doc.metadata)

print(f"Loaded {len(docs)} docs")
