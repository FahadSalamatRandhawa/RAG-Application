from langchain.llms import OpenAI
from langchain.chains import RetrievalQA


class OpenAi_Model():
    def __init__(self,api_key:str,temperature:int=0):
        try:
            self.openai = OpenAI(api_key=api_key,temperature=temperature)
            self.temperature=temperature
        except Exception as e:
            print("Error in creating OpenAi_Model")
            print(e)
            return False

    def query_output(self,query:str,retriever):
        """
        query:query for the document
        retriever:a vector reterival object to retrieve similar documents

        returns the llm_output 
        """
        try:
            qa=RetrievalQA.from_chain_type(llm=self.openai, chain_type="stuff", retriever=retriever)
            llm_output=qa.run(query)
            return llm_output
        except Exception as e:
            print("Error in OpenAi_Model for query_output")
            print(e)
            return False
