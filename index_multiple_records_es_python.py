#################################### INDEX MULTIPLE RECORDS FROM A CSV FILE TO ELASTICSEARCH INDEX############################
from elasticsearch import Elasticsearch
import pandas as pd

client=Elasticsearch("http://localhost:9200")
print(client.info())

single_index_name="single_record"
multiple_index_name="multiple_record"

#read_csv is a function of pandas library(lot many paramertes for this function, see as and when req)
df=pd.read_csv("/Users/utkarshsinha/Desktop/PYTHON_ES_LOCAL_SEMANTIC/Python_ES/udemy_courses.csv") #path of csv file
print(df.head(5))

## Note-> to index records in an elasticsearch index we need the data to be in a dictionary format, then only we can index.

######################## INDEXING ONE RECORD ####################
#document is a dictionay with key and value
document = {
    "title": "Sample Document",
    "content": "This is a sample document for indexing in Elasticsearch.",
    "tags": ["sample", "elasticsearch", "python"]
}

client.index(index=single_index_name, body=document) #Use the index() method of the Elasticsearch client to index the document

############################## INDEX MULTIPLE RECORDS ############################################
#Note -> To index multiple records we need a LIST OF DICTIONARY, where we will iterate through the list and index one dictionary in one iteration

record_list=df.to_dict(orient='records') #here we are converting the csv(dataframe) data to a list of dictionaries to be indexed to elasticsearch

'''
VVVIMP-> df.to_dict(orient='records') is a method in pandas that converts a DataFrame into a list of dictionaries.
orient='records': This parameter specifies the format of the resulting dictionary.
When set to 'records', the method will return a list of dictionaries, where each dictionary represents a single row in the DataFrame.
The keys of each dictionary are the column names, and the values are the corresponding values in that row.
eg:A  B
0  1  4
1  2  5
2  3  6

is converted to 
[
    {'A': 1, 'B': 4},
    {'A': 2, 'B': 5},
    {'A': 3, 'B': 6}
]
‘records’ : list like [{column -> value}, … , {column -> value}]
That is how we want, we want each row to be one dictionary within the list with key value of it as it's coloumn name
'''

print(type(record_list))
print(record_list[0])# Now we have the list of dictionaries required.

'''
VVVVIMP -> Now we have the  list of dictionary now we need to iterate through the list and index one dictionary as one record in es index.
for x in record_list:
    in first iteration it will pick the dictionary at 0th index of the list
    index_data is a dictionary  we are creating with keys(which will be the key for value in es index, like under mapping we have keys)
    courseId,courseTitle, url etc are the key values, the keys we want to see in es index
    and  x['course_id] , str(x['course_title']) are the values we want to give for that key
    so, for first iteration it will create a dictionary 'index_data' with key(manual) and values from record_list[0]th element
    after that it will index the 0th element records using the client.index
    and carry on for the next iterations i.e recordlist[1], recordlist[2] and so on...........
    Thus in one iteration one record is being ingested
'''
for x in record_list:
    #Note-> since index structure is not defined from before, it will take the type(long,text) as per the value(x['course_id']) type,
    #if suppose multiple_records was defined from before and every key was of type text it will not take int,long values.
    #so be careful of the type of data and corresponding type of that key in es index.

    '''
     VVVIMPPP-> both index_data={'courseId': x['course_id'],....} and index_data=x works,
     since x is already a dictionary at the nth element of the record_list,
     we can directly give x as body to index in each iteration
    '''

    '''
    index_data={
        'courseId': x['course_id'],
        'courseTitle': str(x['course_title']),
        'url':str(x['url']),
        'price':x['price'],
        'subject':str(x['subject'])
    }
    '''
    #OR 
    index_data=x
    try:
        client.index(index=multiple_index_name,body=index_data,request_timeout=1000000) 
        '''
        The client.index() method in Elasticsearch Python client library is used to index a document into an Elasticsearch index.
        body: This parameter specifies the document data you want to index. It should be a dictionary where the keys are field names and the values are the corresponding values you want to store.
        This method creates a new document or updates an existing document in the specified index. 
        If you don't specify an id for the document, Elasticsearch will automatically generate one. 
        If you want to specify your own id, you can pass it as another parameter to the index() method:
        client.index(index='your_index_name', id='your_document_id', body=index_data)
        '''
    except Exception as e:
        print(e)
