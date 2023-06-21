import os
import argparse

from langchain.document_loaders import NotionDirectoryLoader
from langchain.document_loaders import PyPDFLoader

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores.faiss import FAISS

from api_key_loader import load_api_keys

DEFAULT_CHUNK_SIZE = 1024
DEFAULT_CHUNK_OVERLAP = 128

def gen_pdf_idx(source_path, chunk_size, chunk_overlap):
    print(f"generating index with pdf at {source_path}")

    loader = PyPDFLoader(source_path)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap)
    
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    index = FAISS.from_documents(texts, embeddings)
    return index

def gen_notion_idx(source_path, chunk_size, chunk_overlap):
    print(f"generating index from Notion dump at {source_path}")

    loader = NotionDirectoryLoader(source_path)

    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap)
    
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    index = FAISS.from_documents(texts, embeddings)
    return index

def gen_index(source_path, source_type, idx_path, chunk_size, chunk_overlap):
    print(f"""Generating index:
            Index path: {idx_path}
            Source path: {source_path}
            Source type: {source_type}
            Chunk size: {chunk_size}
            Chunk overlap: {chunk_overlap}
          """)

    if source_type == "pdf":
        index = gen_pdf_idx(source_path, chunk_size, chunk_overlap)
    elif source_type == "notion":
        index = gen_notion_idx(source_path, chunk_size, chunk_overlap)
    else:
        print(f"Unknown source type: {source_type}")
        return

    if os.path.exists(idx_path):
        print(f"Index {idx_path} found; updating...")
        vectorstore = FAISS.load_local(idx_path, OpenAIEmbeddings())
        vectorstore.merge_from(index)
    else:
        print(f"Index {idx_path} not found; creating...")
        vectorstore = index

    vectorstore.save_local(idx_path)
    print("Documents indexed:")
    for key in vectorstore.docstore._dict:
        print(vectorstore.docstore._dict[key].metadata['source'])



if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add required string arguments
    parser.add_argument('--source', type=str, required=True, help='Path to source')
    parser.add_argument('--type', type=str, required=True, help='Source type')
    parser.add_argument('--idx_path', type=str, required=True, help='Index file name')
    parser.add_argument('--chunk_size', type=int, required=False, help='Index chunk size')
    parser.add_argument('--chunk_overlap', type=int, required=False, help='Index chunk overlap')

    # Parse the command line arguments
    args = parser.parse_args()

    # Access the parsed arguments
    source_path = args.source
    source_type = args.type
    idx_path = args.idx_path
    
    if args.chunk_size == None:
        chunk_size = DEFAULT_CHUNK_SIZE
    else: 
        chunk_size = args.chunk_size

    if args.chunk_overlap == None:
        chunk_overlap = DEFAULT_CHUNK_OVERLAP
    else: 
        chunk_overlap = args.chunk_overlap

    load_api_keys()
    gen_index(source_path, source_type, idx_path, chunk_size, chunk_overlap)