# import pandas as pd
# import chromadb
# import uuid


# class Portfolio:
#     def __init__(self, file_path="D:/project-genai-cold-email-generator/app/resource/my_portfolio.csv"):
#         self.file_path = file_path
#         self.data = pd.read_csv(file_path)
#         self.chroma_client = chromadb.PersistentClient('vectorstore')
#         self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

#     def load_portfolio(self):
#         if not self.collection.count():
#             for _, row in self.data.iterrows():
#                 self.collection.add(documents=row["Techstack"],
#                                     metadatas={"links": row["Links"]},
#                                     ids=[str(uuid.uuid4())])

#     def query_links(self, skills):
#         return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])


import pandas as pd
import chromadb
import uuid
from chromadb.config import Settings


class Portfolio:
    def __init__(self, file_path="D:/project-genai-cold-email-generator/app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # ✅ Persistent client with correct path argument
        self.chroma_client = chromadb.PersistentClient(
            path="./vectorstore",
            settings=Settings(anonymized_telemetry=False)  # avoids telemetry issues
        )

        # ✅ Auto-create collection
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        """Load portfolio CSV into ChromaDB (only once)."""
        if self.collection.count() == 0:  # load only if empty
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[str(row["Techstack"])],  # must be list
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        """Query ChromaDB for portfolio entries matching skills."""
        if not skills:
            return []

        results = self.collection.query(
            query_texts=[" ".join(skills)],  # single joined query
            n_results=2
        )
        return results.get("metadatas", [[]])[0]  # safe return
