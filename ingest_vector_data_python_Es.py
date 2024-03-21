#################### READ CSV FILE CONVERT TEXT  TO VECTOR FORM AND INGEST TO ELASTICSEARCH INDEX ############################ 

from elasticsearch import Elasticsearch
import pandas as pd
from sentence_transformers import SentenceTransformer
'''
import the SentenceTransformer class from the sentence_transformers library in Python. 
This library provides a simple interface for using pre-trained sentence embeddings models, such as BERT-based models, 
for generating vector representations of sentences.
'''

client= Elasticsearch("http://localhost:9200")
index_name="semantic_courseera"


df= pd.read_csv("udemy_courses.csv")
print(df.head(1))
########## THIS IS ONE WAY TO VECTORIZE THE course_title, which we have been using till date, it works well####################
'''

### Python class named Tokenizer that uses the SentenceTransformer to encode documents into embeddings.########

class Tokenizer(object):
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_token(self, documents):
        sentences  = [documents]
        sentence_embeddings = self.model.encode(sentences)
        encod_np_array = np.array(sentence_embeddings)
        encod_list = encod_np_array.tolist()
        return encod_list[0]

token_instance = Tokenizer() #OBJECT of Tokenizer Class

df["vector"] = df['course_title'].progress_apply(token_instance.get_token) #we are calling the get_token fucntion of Tokenizer class from the token_instance object
#progress_apply is used in Jupyter to show the progress,in VS code just use apply

print(df.head()) #Now we have the vector coloumn as well with vector embedding for each row on top of the course_title field
'''

######################### THIS IS THE SECOND AND EASY METHOD#############################
model = SentenceTransformer('all-MiniLM-L6-v2') 
#imports the SentenceTransformer class from the sentence_transformers library and initializes a SentenceTransformer model using the 'all-MiniLM-L6-v2' pre-trained model.
# This model is trained to generate fixed-size dense embeddings (vectors) for input sentences.

'''
We define a custom function vector(row) that takes a row of the DataFrame as input and returns the vector form of couloumn course_title.
We use the .apply() method along with the custom function to apply the function to each row of the DataFrame (axis=1 specifies that the function should be applied row-wise).
The result of the .apply() operation is assigned to a new column named 'vector'.

'''
def vector(row):
    return model.encode(row['course_title'])

df["vector"] = df.apply(vector,axis=1)
print(df.head())#Now we have the vector coloumn as well with vector embedding for each row on top of the course_title field

'''
Next is to create a index with mappins and settings with dense vector
PUT udemy_courses
{
  "settings": {
    "number_of_shards": 5,
    "number_of_replicas": 1,
    "analysis": {
      "filter": {
        "stop_filter": {
          "type": "stop",
          "stopwords": "_english_"
        }
      },
      "analyzer": {
        "whitespace_stop_analyzer": {
          "filter": [
            "lowercase",
            "stop_filter"
          ],
          "type": "custom",
          "stopwords": "_english_",
          "tokenizer": "whitespace"
        }
      },
      "tokenizer": {
        "split_tokenizer": {
          "pattern": "([^|/]+)",
          "type": "pattern",
          "group": "1"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "vector": {
        "type": "dense_vector",
        "index": true,
        "similarity": "dot_product",
        "dims": 384
      },
      "course_title": {
        "type": "text",
        "analyzer": "whitespace_stop_analyzer", 
        "fields": {
          "keyword": {
            "type": "keyword",
            "index": false
          }
        }
      },
      "course_id": {
        "type": "keyword",
        "index": false
      },
      "url": {
        "type": "keyword",
        "index": false
      },
      "num_lectures": {
        "type": "keyword",
        "index": false
      },
      "price": {
        "type": "keyword",
        "index": false
      },
      "published_timestamp":
      {
        "type": "date"
      }
    }
  }
}
'''
#Now we will ingest records to the elasticsearch index

es_data=df.to_dict(orient='records') #Already described in detail in index_multiple_records_es_python.py
#in short creates a list of dictionaries , es_data is a list

for value in es_data:
    document=value
    try:
        client.index(index=index_name,body=document,request_timeout=1000000)
    except Exception as e:
        print(e)

#### Records ingested along with vectors.