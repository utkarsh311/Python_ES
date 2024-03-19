############################## Create index structure with mappings and settings with Python script ##########################################
from elasticsearch import Elasticsearch

client= Elasticsearch("http://localhost:9200")
print(client.info())

index_name="create-index-from-python" #Define the index name

#Define the mappings and settings for your index.

#mappings is a dictionary containing the mappings for different fields in the index.
mappings={
    "properties": {
      "course_title": {
        "type": "text",
        "analyzer": "whitespace_stop_analyzer", 
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "course_id": {
        "type": "keyword"
      },
      "url": {
        "type": "keyword"
      },
      "num_lectures": {
        "type": "keyword"
      },
      "price": {
        "type": "keyword"
      },
      "published_timestamp":
      {
        "type": "date"
      }
    }   
}

#settings is a dictionary containing various settings such as the number of shards and replicas.
settings ={   
    "number_of_shards": 1,
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
}

#Use the indices.create() method of the Elasticsearch client to create the index with the specified mappings and settings:
#This is a method provided by the Elasticsearch Python client library to create an index in the Elasticsearch cluster.
client.indices.create(index=index_name, body={"mappings": mappings, "settings": settings})
#body={"mappings": mappings, "settings": settings}: This parameter specifies the body of the request sent to Elasticsearch to create the index. It's a dictionary containing two keys: "mappings" and "settings".
