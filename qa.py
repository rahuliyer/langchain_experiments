import sys

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader('./scaling_people.pdf')

documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0), 
    chain_type="stuff", 
    retriever=docsearch.as_retriever())

while True:
    query = input("Ask a question: ")
    result = qa.run(query)
    print(result)
