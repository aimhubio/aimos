import os
from pathlib import Path

import requests
from aimstack.llamaindex_observer.callback_handlers import GenericCallbackHandler
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.callbacks.base import CallbackManager

paul_graham_essay_url = "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt"
response = requests.get(paul_graham_essay_url)
output_dir = Path("aimos/examples/paul_graham_essay/data/")

if response.status_code == 200:
    os.system(f"mkdir -p {output_dir}")
    with open(output_dir.joinpath("Paul_Graham_Essay.txt"), "wb") as file:
        file.write(response.content)
else:
    print("Failed to download the file.")

documents = SimpleDirectoryReader(output_dir).load_data()


aim_callback = GenericCallbackHandler(repo="aim://0.0.0.0:53800")
callback_manager = CallbackManager([aim_callback])


service_context = ServiceContext.from_defaults(callback_manager=callback_manager)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
query_engine = index.as_query_engine()
aim_callback.flush()

query_engine.query("How does Graham address the topic of competition and the importance (or lack thereof) of being the first mover in a market?")
aim_callback.flush()

query_engine.query("What are Paul Graham's notable projects or companies?")
aim_callback.flush()

query_engine.query("What problems did the author encounter with the early AI programs?")
aim_callback.flush()
