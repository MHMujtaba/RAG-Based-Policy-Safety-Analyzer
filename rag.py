import os

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import glob

class RAG:
    def __init__(self, docs_folder, top_k=2):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.docs, self.embeds = [], []
        for f in glob.glob(f"{docs_folder}/*.md"):
            with open(f) as fp:
                txt = fp.read()
                self.docs.append(txt)
                self.embeds.append(self.model.encode(txt))
        self.index = faiss.IndexFlatL2(len(self.embeds[0]))
        self.index.add(np.array(self.embeds))
        self.top_k = top_k

    def retrieve(self, query):
        q_emb = self.model.encode(query)
        _, idxs = self.index.search(q_emb.reshape(1, -1), self.top_k)
        top_docs = [self.docs[i] for i in idxs[0]]
        return top_docs, idxs[0].tolist()
