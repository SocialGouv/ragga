"""Markdown reader."""
from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.schema import Document

import frontmatter


def dict_string_values(dct):
    return dict(
        map(
            lambda x: (x, str(dct.get(x))),
            dct,
        )
    )


class MarkdownReader(BaseReader):
    """Markdown reader

    Extract raw markdown and front matter
    """

    def __init__(
        self,
        include_metas=[],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self.include_metas = include_metas

    def load_data(
        self,
        input_file,
        extra_info,
        # self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file into string."""
        with open(input_file, encoding="utf-8") as f:
            content = f.read()
        markdown = frontmatter.loads(content)

        def should_include_key(pair):
            key, value = pair
            return not self.include_metas or key in self.include_metas

        metas = dict(
            filter(
                should_include_key,
                markdown.metadata.items(),
            )
        )
        metadata = dict_string_values(
            {
                "filename": input_file.name,
                **metas,
                **extra_info,
            }
        )
        return [Document(text=content, metadata=metadata)]
