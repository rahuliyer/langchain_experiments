import sys
import os
import argparse

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

from langchain import PromptTemplate, LLMChain

from langchain.chains import RetrievalQA

from langchain.vectorstores.faiss import FAISS

MAX_MEMORY_LEN = 4096

def search(index_path):
    vectorstore = None
    if os.path.exists(index_path):
        print("Index found. Loading index...")        
        vectorstore = FAISS.load_local(index_path, OpenAIEmbeddings())
    else:
        print(f"Index {index_path} doesn't exist")
        sys.exit(-1)

    llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
    prompt_template = """You are a helpful AI assistant
        Given the context and input text please respond to the question
        as succinctly as possible:
        Context: {context}
        Input text: {input_text}
        Question: {question}
    """
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt_template)
    )

    memory = ""
    while True:
        query = input("Ask a question: ")
        result = vectorstore.similarity_search_with_score(query, k=5)
        text = ""
        sources = set()
        for doc, score in result:
            text += doc.page_content + "\n"
            sources.add(doc.metadata['source'])

        result = llm_chain({
            'context': memory, 
            'input_text': text,
            'question': query
            })

        print(f"{result['text']}")
        print("Sources:")
        for source in sources:
            print(source)

        memory += result['text'] + "\n"
        if len(memory) > MAX_MEMORY_LEN:
            memory = memory[:-MAX_MEMORY_LEN]

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add required string arguments
    parser.add_argument('--idx_path', type=str, required=True, help='Index file name')

    # Parse the command line arguments
    args = parser.parse_args()
    idx_path = args.idx_path

    search(idx_path)

