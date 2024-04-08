############# flask api to return images using search query string matching with image embeddings######################
from elasticsearch import Elasticsearch
import pandas as pd
from sentence_transformers import SentenceTransformer
from flask import Flask, jsonify, request

client=Elasticsearch("http://localhost:9200")
index_name="image_index"
model = SentenceTransformer('clip-ViT-B-32')

def return_embedding(query):
    vector=model.encode(query)
    return vector

app=Flask(__name__)

@app.route('/image_search',methods=["GET","POST"])
def image_search():
    query=request.json['query_string']
    query_vector=return_embedding(query)
    query  ={
    "_source": ["image_name","image_path"], #only these 2 fields will be returned for all records
       "knn":{
           "field":"image_embedding",
           "query_vector":query_vector,
           "k":4, #number of records(nearest neighbours) to be returned
           "num_candidates":10 #This parameter represents the number of candidate documents to evaluate during the search process.
        }
    }
    res=client.search(index=index_name,body=query,min_score=0.62,request_timeout=100000)
    ####IMP->MIN_SCORE- is the relevency score, minimun should be >=0.62, then only return results, 
    #play around with this to filter irrelevent results
    result_list=[]
    for val in res['hits']['hits']:
        result_list.append(val['_source'])
    result_dict={"result":result_list}
    return result_dict


if __name__=='__main__':
    app.run(host='localhost', port="5001")