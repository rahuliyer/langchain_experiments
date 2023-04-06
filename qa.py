import sys

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT

from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader('./scaling_people.pdf')

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

#qa = ConversationalRetrievalChain.from_llm(
#    llm=OpenAI(temperature=0), 
#    retriever=docsearch.as_retriever())
llm = OpenAI(temperature=0)
question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
doc_chain = load_qa_chain(llm, chain_type="map_reduce")

qa = ConversationalRetrievalChain(
    retriever=docsearch.as_retriever(),
    question_generator=question_generator,
    combine_docs_chain=doc_chain,
)
history = []
while True:
    query = input("Ask a question: ")
    result = qa({"question": query, "chat_history": history})
    print(result["answer"])
    history.append((query, result["answer"]))
