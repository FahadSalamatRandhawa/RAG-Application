from fastapi import FastAPI, Depends,Body,UploadFile,File,HTTPException
from api._Database__Model import Database
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from api._OpenAI__Model import OpenAi_Model
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv,find_dotenv
import os

from typing import List

_:bool=load_dotenv(find_dotenv())
app = FastAPI()

# load files
def Load_File(path:str,glob:str):
    loader=DirectoryLoader(path,glob,show_progress=True)
    data=loader.load()
    print(data)
    return data

@app.on_event("startup")
async def startup():
    try:
        global database, llm_model, embeddings
        llm_model=OpenAi_Model(api_key=os.environ.get('OPENAI_API_KEY'))
        embeddings=OpenAIEmbeddings(api_key=os.environ.get('OPENAI_API_KEY'),disallowed_special=())
        database=Database(connection_string=os.environ.get('MONGODBATLAS_CONNECTIONSTRING'))
    except Exception as e:
        print("Error in database startup")
        print(e)
        raise HTTPException(status_code=500, detail="Error in loading models")

@app.get("/api/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/upload")
async def upload_To_Database(files:List[UploadFile] = File(...)):
    # print(files)
    # for file in files:
    #     contents = await file.read()
    #     print(f"Contents of {file.filename}:")
    #     print(contents)
    try:
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)

        # loop and split each document text 1 by 1, store chunks in new array
        docs = [];filenames=[]
        for file in files:
            print(vars(file))
            contents = await file.read()
            contents = contents.decode("utf-8")  # decode bytes to string
            docs.extend(text_splitter.split_text(contents))
            filenames.extend([file.filename])
        
        # documents = [{"page_content": text} for text in docs]
        # print("Splitted docs", len(documents))
        # for document in documents:
        #     print(document)
            
        print(docs)
        database.insert_data(docs,embeddings,"rag_application","training_docs")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error in uploading to database")

@app.post("/api/getresponse")
def chat(query:str=Body()):
    print(query)
    collection=database.get_collection("rag_demo","training_documents")
    try:
        top_doc,retriever=database.query_database(query,"rag_application","training_docs",embedding_model=embeddings)
        doc_contents=[doc.page_content for doc in top_doc]
        print("Question : ",query)
        query=f""" Question = ```{query}```, instruction = ```The answer must be provided according to the context, otherwise respond with "I don't know"``` , context = ```{doc_contents}``` """
        if(retriever):
            llm_output=llm_model.query_output(query,retriever)
            print(llm_output)
            return llm_output
    except Exception as e:
        print("Error in chat ")
        print(e)
        raise HTTPException(status_code=500, detail="Error in chat")
    
@app.post("/api/vectorsearch")
async def vector_search(query:str=Body()):
    try:
        top_doc,retriever=database.query_database(query,"rag_application","training_docs",embedding_model=embeddings)
        doc_contents=[doc.page_content for doc in top_doc]
        print(len(doc_contents))
        return doc_contents
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in vector search")