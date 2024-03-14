from transformers import pipeline #type: ignore
#import pymongo as pym #type: ignore

class Embedding_Model():
    def __init__(self,task:str,model:str)->None:
        self.model=model
        self.pipeline=pipeline(task, model=model)
        self.task=task

    def toVector(self, text:str)->list[float]:
        embedding=self.pipeline(text)
        return embedding