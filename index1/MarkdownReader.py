"""Markdown reader."""
from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.schema import Document

import frontmatter


class MarkdownReader(BaseReader):
    """Markdown reader

    Extract raw markdown and front matter
    """

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)

    def load_data(
        input_file,
        extra_info,
        # self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        # print(input_file, extra_info)
        """Parse file into string."""
        # print("extra_info", extra_info)
        with open(input_file, encoding="utf-8") as f:
            content = f.read()
        markdown = frontmatter.loads(content)
        metadata = {
            "filename": input_file.name,
            "metadata": {**markdown.metadata, **extra_info},
        }

        # print(post)
        # if not post.metadata:
        #     post.metadata["title"] = "xxx"
        # return {"filename": filename} | post.metadata

        # if extra_info:
        #     metadata = {**metadata, **extra_info}

        return [Document(text=content, metadata=metadata)]
