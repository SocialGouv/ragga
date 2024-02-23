# ragga

⚠️ experimental

Expose a [llama-index](https://llamaindex.ai) chat with a [streamlit](https://streamlit.io/) UI.

The service download and index files based on [./download.sh](./download.sh)

## Dev

```sh
poetry install
poetry shell


export OPENAI_API_KEY=xxx

# run CLI example
python src/index.py

# run streamlit GUI
streamlit run src/run.py
```

## Todo

- gestion CSV/pandas
- add evaluation pipeline
- données : matomo, github...
