from langchain.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient

#mongodb+srv://dreamtwister61814:5Mi3VbL7JHXb47FI@cluster0.9guwb86.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
class Database():
    def __init__(self,connection_string:str) -> None:
        self.client=MongoClient(connection_string)

    def get_collection(self,database:str,collection_name:str):
        """
        databasename,collectionname
        """
        collection=self.client[database][collection_name]
        return collection
    
    def insert_data(self,data,embedding_model,database:str,collection:str):
        try:
            collection=self.get_collection(database,collection)
            print("Inserting data to MongoDB")
            vectorStore=MongoDBAtlasVectorSearch.from_texts(data, embedding=embedding_model, collection=collection)
            print(" Successfully Inserted data")
            return vectorStore
        except Exception as e:
            print("Error in inserting data to MongoAtlasDB")
            print(e)
            return False
        
    def query_database(self,query:str,database:str,collection:str,embedding_model):
        """
        returns 
        top_documents (most similar document)\n
        retriever (a retriever instance of the vectoreStore [to pass to the llm model])
        """

        vectoreStore=MongoDBAtlasVectorSearch(self.client[database][collection],embedding_model)
        docs=vectoreStore.similarity_search(query,K=10)
        retriever=vectoreStore.as_retriever()
        return docs,retriever
    
    
    def get_vectoreStore(self):
        return self.vectoreStore
    
    def Create_Collection(self,databsae:str,collection:str):
        collection=self.client[databsae][collection]
        return collection


