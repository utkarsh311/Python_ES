############ FLASK REST API for kNN and Traditional search ################
from elasticsearch import Elasticsearch
import pandas as pd
from sentence_transformers import SentenceTransformer
from flask import Flask, jsonify, request
'''
Flask is a lightweight web application framework for Python. 
Flask: This is the main Flask module. 
        By importing Flask, you create a Flask application instance, which will be used to define routes and run the web server.
jsonify: jsonify is a function provided by Flask that converts a Python dictionary into a JSON response. 
        It is commonly used to return JSON data from Flask routes.
request: request is a global object provided by Flask that represents the incoming HTTP request. 
    It contains information about the request such as headers, form data, and query parameters. 
    You can use it to access data sent by the client in the request.
'''
client=Elasticsearch("http://localhost:9200")
print(client.info())

index_name="semantic_courseera"
model=SentenceTransformer('all-MiniLM-L6-v2')
#Initializing pretrained all-MiniLM-L6-v2 with model instance/object

app=Flask(__name__) #creates a Flask application instance named app, using the name of the current module as the parameter.
'''
#name: This is a special variable in Python that represents the name of the current module. When you run a Python script directly, 
# Python sets the __name__ variable of that script to '__main__'. 
# When you import a module, Python sets the __name__ variable of that module to the module's name. 
# By passing __name__ as an argument to Flask, you are telling Flask the name of the current module,
#  which Flask uses to locate resources such as templates and static files.
'''

'''
@app.route: This is a decorator provided by Flask to define routes in a Flask application. 
            It tells Flask to associate the decorated function with a specific URL route.
"/semanticsearch": This is the URL route that the decorated function will be associated with. 
            In this case, the function will handle requests to the "/semanticsearch" route.
methods=['POST', 'GET']: This specifies the HTTP methods that the route will respond to. 
            In this case, the route will respond to both POST and GET requests. 
'''

@app.route("/semanticsearch",methods=['POST','GET'])
def semanticsearch():
    if request.method == "POST":
        input=request.json['query_string']
        #request.json contains a JSON/dict object and you want to retrieve the value associated with the key 'query_string'
        #in POSTMAN or UI if I give {"query_string":"courses on python"}, input variable will have value courses on python

    token_vector=model.encode(input)
    #we are giving the user input(input->say courses on python) to model to return vector form of query string
    
    #we are running knn query and giving our input token_vector to coampre with existing records
    query  ={
    "_source": ["course_id","course_title"], #only these 2 fields will be returned for all records
       "knn":{
           "field":"vector",
           "query_vector":token_vector,
           "k":10, #number of records(nearest neighbours) to be returned
           "num_candidates":10 #This parameter represents the number of candidate documents to evaluate during the search process.
        }
    }
    res=client.search(index=index_name,body=query,request_timeout=100) 

    #The results returned is a list of dictionaries so to store it we need a list of dictionaries
    result_list=[] #creating an empty list to store all dictionaries
    for val in res['hits']['hits']: #iterating through the hits list under hits dictionary
        result_list.append(val['_source']) #Append all the _source dictionary value to this list as nth element
                                            #Since only course_id and course_title is in response
                                            #result_list=[{"course_id":01,"course_title":python},{},{}...]
        #print(val['_source']['course_id'])
    #print(result_list)
    #We can return result_list as well BUT in flask only string, dict and tuple can be returned as response
    #return result_list #TypeError: The view function did not return a valid response. 
                        #The return type must be a string, dict, tuple, Response instance, or WSGI callable, but it was a list.

    response_dict={"response":result_list} #Creating a dictionary with key 'response' and value for this key is result_list
                                            #This is done just to return response as a dict and not list
    return response_dict #List of dictionary with our returned results under keyname 'response'


'''
"/traditional": This is the URL route that the decorated function will be associated with. 
            In this case, the function will handle requests to the "/traditional" route.
'''
@app.route("/traditionalsearch",methods=["GET","POST"])
def traditionalsearch():
    input=request.json['query_string']

    query={
        "_source": ["course_id","course_title"],
        "query":
        {
            "match":{
                "course_title":input
            }
        }
    }
    res=client.search(index=index_name,body=query,request_timeout=100)
    result_list=[]
    for value in res['hits']['hits']:
        result_list.append(value['_source'])

    response_dict={"response":result_list}
    return response_dict

'''
This condition (if __name__ == '__main__':) ensures that the following code block will only run if the script is executed directly,
 not if it's imported as a module into another script.
 In this particular case, the code block app.run(host='localhost', port=5001) starts the Flask application. 
 It tells Flask to listen for incoming HTTP requests on the localhost (127.0.0.1) 
 Flask will start the development server, and your Flask application will be accessible at http://localhost:5001/ 
 in a web browser or through HTTP requests.
'''
if __name__=='__main__':
    app.run(host='localhost', port="5001")