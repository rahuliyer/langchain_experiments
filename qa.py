import sys
import os
import argparse

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

from langchain.chains import RetrievalQA

from langchain.vectorstores.faiss import FAISS

def qa(index_path):
    vectorstore = None
    if os.path.exists(index_path):
        print("Index found. Loading index...")        
        vectorstore = FAISS.load_local(index_path, OpenAIEmbeddings())
    else:
        print(f"Index {index_path} doesn't exist")
        sys.exit(-1)

    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k"), 
        chain_type="stuff", 
        retriever=vectorstore.as_retriever())

    while True:
        query = input("Ask a question: ")
        result = qa.run(query)
        print(f"{result}\n")

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add required string arguments
    parser.add_argument('--idx_path', type=str, required=True, help='Index file name')

    # Parse the command line arguments
    args = parser.parse_args()
    idx_path = args.idx_path

    qa(idx_path)

