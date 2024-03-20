################################ SEARCHING FROM AN ELASTICSEARCH INDEX ###################################


from elasticsearch import Elasticsearch
client=Elasticsearch("http://localhost:9200")

index_name="multiple_record"

## The query you want to give 
query={
    "query":
    {
        "match_all":{}
    }
}

res=client.search(index=index_name,body=query)

print(type(res)) #Res is an Object, <class 'elastic_transport.ObjectApiResponse'>

'''
VVVVIMP ->  We have response now , the sturcture of respons is as follows,
{
  "took": 10,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3678,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "multiple_record",
        "_id": "KtERWI4BWKwUUuhoycHQ",
        "_score": 1,
        "_source": {
          "course_id": 499504,
          "course_title": "Disminuye deudas en tu hogar en menos de 30 días"
        }
      },
      {
        "_index": "multiple_record",
        "_id": "K9ERWI4BWKwUUuhoycHh",
        "_score": 1,
        "_source": {
          "course_id": 903326,
          "course_title": "CPA 10 COMPLETO"
        }
      }
    ]
  }
}

The outermost dictionary has 4 keys
1)took -> value is number
2)timed_out -> value is true or false
3)_shards -> value is again a dictionary
4)hits ->  value is again a dictionary

Now the data is in dictioanry present under  'hits' key

Let us see 'hits' dictionary now
"hits": {
    "total": {
      "value": 3678,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "multiple_record",
        "_id": "KtERWI4BWKwUUuhoycHQ",
        "_score": 1,
        "_source": {
          "course_id": 499504,
          "course_title": "Disminuye deudas en tu hogar en menos de 30 días"
        }
      },
      {
        "_index": "multiple_record",
        "_id": "K9ERWI4BWKwUUuhoycHh",
        "_score": 1,
        "_source": {
          "course_id": 903326,
          "course_title": "CPA 10 COMPLETO"
        }
      }
    ]
}

Now the hits dictionary again has 3 keys,
1) total -> value is a dictionary
2) max_score -> value is an int value
3)"hits" -> value is a list of dictionaries

######Now 'hits' is a list of dictionaries which we need to iterate over to get our searched results.
so to access this list of dictionaries we need
for value in res['hits']['hits']: -> the above hit key and under that again the hit key with list of dictionaries
    value is the nth element of the list of dictionaries

Now again since ['hits'] ['hits'] is a list of dictionary
so ['hits'] ['hits'] looks like
"hits": [
      {
        "_index": "multiple_record",
        "_id": "KtERWI4BWKwUUuhoycHQ",
        "_score": 1,
        "_source": {
          "course_id": 499504,
          "course_title": "Disminuye deudas en tu hogar en menos de 30 días"
        }
      },
      {
        "_index": "multiple_record",
        "_id": "K9ERWI4BWKwUUuhoycHh",
        "_score": 1,
        "_source": {
          "course_id": 903326,
          "course_title": "CPA 10 COMPLETO"
        }
      }
]
so at each element of this list we have a dictionary , and under each dictionary , under _source key we have our values,
_source which again is a dictionary and keys and values of this dictionary is our fields and values indexed.

so to access each record which the query returned use the following code
'''

for value in res['hits']['hits']:
    print(value['_source'])  #will print nth '_source' key value(which is a dictioanry) 
    print(type(value['_source'])) #type is dicitonary, i.e the entire dictioanry with keys and it's values which we indexed

## Now suppose we have to fetch only one value say course_id form the returned results then
for value in res['hits']['hits']:
    print(value['_source']['course_id']) #Since _source is a also a dictionary with key and values, 
                                #course_id is a key in _source dict and we are fetching the value of course_id keys
    print(type(value['_source']['course_id'])) #int , since course_id value is int