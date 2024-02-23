import re
import logging
import sys
import os.path
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast
import frontmatter

from llama_index.core import PromptTemplate
from llama_index.core.schema import Document
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

from llama_index.readers.file.markdown import MarkdownReader

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


class StartupMarkdownReader(MarkdownReader):
    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        results = super().load_data(file, extra_info)
        with open(file, encoding="utf-8") as f:
            content = f.read()
        header = [item for item in filter(lambda a: a != "", content.split("---"))][0]
        value = header
        results.append(Document(text=value, extra_info=extra_info or {}))
        return results


PERSIST_DIR = "./storage"


def get_doc_metadata(filename):
    url = "https://doc.incubateur.net/communaute/{}".format(
        re.sub(".md$", "", re.sub("^content/documentation-beta/", "", filename))
    )
    return {"url": url}


def get_startup_metadata(filename):
    print("get_startup_metadata", filename)
    url = "https://beta.gouv.fr/startups/{}.html".format(
        re.sub(".md$", "", re.sub("^content/startups-beta/", "", filename))
    )
    return {"url": url}


# check if storage already exists
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    docs = SimpleDirectoryReader(
        "./content/documentation-beta/",
        file_metadata=get_doc_metadata,
        recursive=True,
        exclude=["SUMMARY.md", "README.md"],
    ).load_data()
    startups = SimpleDirectoryReader(
        "./content/startups-beta",
        required_exts=[".md"],
        file_extractor={".md": StartupMarkdownReader()},
        file_metadata=get_startup_metadata,
    ).load_data()
    index = VectorStoreIndex.from_documents([*docs, *startups], show_progress=True)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    print("Loading existing database")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    print("✔ Loaded")


qa_prompt_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query in french only and invite the user to visit the URL provided in context if any.\n"
    "Query: {query_str}\n"
    "Answer: "
)


def format_context_fn(**kwargs):
    print("format_context_fn", kwargs)
    # format context with bullet points
    context_list = kwargs["context_str"].split("\n\n")
    fmtted_context = "\n\n".join([f"- {c}" for c in context_list])
    return fmtted_context


qa_prompt_tmpl = PromptTemplate(
    qa_prompt_tmpl_str  # , function_mappings={"context_str": format_context_fn}
)

query_engine = index.as_query_engine(similarity_top_k=5)
query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})


if __name__ == "__main__":
    queries = [
        "Que faire quand j'arrête ma mission ?",
        "Quelles sont les règles sur mattermost ?",
        "Comment contacter la startup Aigle ?",
        "Quel est la valeur de accessibility_status pour la startup datagir ?",
        "Quelle startups permettent d'aider à la domiciliation des personnes ?",
        "Quelles sont les nouvelles de démarches simplifiées ?",
    ]

    for query in queries:
        print()
        print()
        print(query)
        print()
        response = query_engine.query(query)
        print(response)
