#!/bin/bash

./download.sh

streamlit run ./src/run.py --server.port=8501 --server.address=0.0.0.0