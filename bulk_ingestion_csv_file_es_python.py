############ CONVERTING A CSV TO BULK REQUEST FORM AND THEN INGESTING TO ES INDEX USING BULK INDEXING#############
from elasticsearch import Elasticsearch 
import pandas as pd
from elasticsearch.helpers import bulk
#elasticsearch.helpers.bulk function is a convenient method provided by the Elasticsearch Python client library (elasticsearch-py) 
# for performing bulk operations, such as bulk indexing or bulk deleting, 
client=Elasticsearch("http://localhost:9200")
csv_file="udemy_courses.csv"
index_one="python_csv_bulk_mehtod_one"
index_two="python_csv_bulk_mehtod_two"

##################### TWO METHOD TO DO BULK INGESTION #############################

######## METHOD 1############
def bulk_mehtod_one(csv_file,index_one):
    df=pd.read_csv(csv_file)
    elk_data=df.to_dict(orient='records') #converting df to list of dictionary to index
    #print(elk_data[0])
    bulk_data=[]
    for val in elk_data:
        #indexing records using bulk should be in a list of dicitonary and each dict should be in the format below,
        #{"_index":"my_bulk","_id":"1","_source":{"name": "utkarsh","age": 28}}
        #so converting our records in the desired format to index in ES index using bulk
        index_details={"_index":index_one,"_id":val['course_id'],"_source":val}
        #_id we are giving value of the course_id  for every document
        #val is a dictionary  which we want to index at the nth pos of the elk_data list
        bulk_data.append(index_details) #creating the list of dictionary to index using bulk

        #In bulk only diff is that we add _index key and _source key , under _source key we give our dictionary which we want to
        #index, in normal we directly give our dictionary(val here) to index using es.index()
    return bulk_data

bulk_data_one=bulk_mehtod_one(csv_file,index_one) #final list of dictionary to be indexed
response_one=bulk(client,bulk_data_one) #givin the es object and body to index, since we have _index in all documents present,
                                        #we are not giving index parameter explicitly
#This will execute the bulk generator function  and return a generator that yields responses for each action in the bulk request.
print("Response one is:")
print(response_one) #we can also iterate response and print response for each item/document

#When you call a generator function, it returns a generator object,and values are generated only when you iterate over the generator object.
#here response_one is a generator object  and we can iterate over it using loops like below
'''
for item in response_one:
    print(item)
'''

########################################################

############ METHOD 2##################
def bulk_method_two(csv_file,index_two):
    df=pd.read_csv(csv_file)
    elk_data=df.to_dict(orient='records') #elk data is the list of dictionary
    bulk_data=[]
    for val in elk_data:
        # to bulk index the data using the es.bulk method the data needs to be in the below format
        '''
        {"index": {"_index": "bulk_python_test", "_id": "1"}},
        {"name": "Utkarsh","age":20},
        {"index": {"_index": "bulk_python_test", "_id": "2"}},
        {"name": "Rahul","age":29}
        '''
        #Thus converting the list of dict(elk_data) in the fomart which can be ingested using bulk
        index_details={"_index":index_two,"_id":val['course_id']} #creating the first level dict {"_index": "bulk_python_test", "_id": "1"}
        operation={"index":index_details} #adding the first level dict to "index" key in another dict {"index": {"_index": "bulk_python_test", "_id": "1"}}
        bulk_data.append(operation) #adding the first level dict to bulk_data list 
        bulk_data.append(val) #adding the value dict(which contains actual values from csv) from elk_data to the bulk_list

    return bulk_data

bulk_data_two=bulk_method_two(csv_file,index_two)
response_two=client.bulk(index=index_two,body=bulk_data_two) #Using the ES client bulk function to index all data in one go
print("Response two is :")
print(response_two)