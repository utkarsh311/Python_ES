###### TRAVERSING THROUGH AN IMAGES FOLDER AND UPLOAD IMAGE EMBEDDING TO ES INDEX##################

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import os #import os module that provides a way to interact with operating system like working with files and directories, executing system commands
from PIL import Image #import the Image module from the Python Imaging Library (PIL). 
                       #PIL is a library in Python used for opening, manipulating, and saving many different image file formats.

client=Elasticsearch("http://localhost:9200")
model = SentenceTransformer('clip-ViT-B-32')
folder_path="/Users/utkarshsinha/Desktop/PYTHON_ES_LOCAL_SEMANTIC/Python_Semantic/uploaded_images/"
index_name="image_index"


#Function to return embedding for image object passed as parameter while calling this function
def returnembedding(img):
    token_vector=model.encode(img)
    return token_vector

#VVIMPPPP
image_name = [f for f in os.listdir(folder_path)] 
## create a list of image names in the given folder path USING LIST COMPREHENSION
'''
List comprehension is a concise way to create lists in Python. It allows you to construct a new list by applying an expression 
to each item in an iterable (such as a list, tuple, or range) and optionally filtering the items based on a condition. 
[expression for item in iterable if condition]
numbers = [1, 2, 3, 4, 5]
squared_numbers = [x ** 2 for x in numbers]
print(squared_numbers)  # Output: [1, 4, 9, 16, 25]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Using list comprehension with if condition to filter even numbers
even_numbers = [x for x in numbers if x % 2 == 0]
print(even_numbers)  # Output: [2, 4, 6, 8, 10]
'''
#print(len(files))
'''
PUT image_index
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
      "image_embedding": {
        "type": "dense_vector",
        "dims": 512,
        "index": true,
        "similarity": "cosine"
      },
      "image_name": {
        "type": "keyword",
        "index": false
      },
      "image_path": {
        "type": "keyword",
        "index": false
      }
    }
  }
}
'''


##get the image name one by one , open it using image.open, generate vector for that image and then index it to ES index
for img in image_name:
    try:
        image_path=str(folder_path+img)
        #print(image_path)
        im=Image.open(image_path)
        vector=returnembedding(im) #passing image object to returnembedding function
        index_dict={ #creating the dictionary with key and vlaue to ingest to es index
            "image_name":img,
            "image_embedding":vector,
            "image_path":image_path
        }
        client.index(index=index_name,body=index_dict,request_timeout=100000) #ingestig to es index
    except Exception as e:
        print(e)
##all images under the given folder indexed to ES index with image vector and other fields.