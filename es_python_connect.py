################################# BASIC PYTHON CONNECTION TO ELASTICSEARCH ################################
#Reference Link -> https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/connecting.html#connecting

from elasticsearch import Elasticsearch 
#is a statement used to import the Elasticsearch class from the elasticsearch module/library. This statement allows you to use functionalities provided by Elasticsearch within your Python code.

#1) Connection to local Elasticsearch without AUTH Enabled

client = Elasticsearch("http://localhost:9200")
#Client  here is an instance/object of Elasticsearch class which we can use to perform operations on our ES cluster, using the methods provided by Elasticsearch class

client.info()
#if succesfull conection happens, returns cluster info, else returns ERROR.

#2) Conecting with AUTH enabled (HTTPS & CA Certificates)
# have the path to cert files generated while Elasticsearch Auth(/etc/elasticsearch/certs in Pearson)and username (mostly 'elastic') and pass(csgFeb2024 in Pearson)
ELASTIC_PASSWORD = 'csgFeb2024' #variable storing the ES password

#create the client instance
client=Elasticsearch(
    "https://localhost:9200",
    ca_certs="/path/to/certfile", #ca_cert -> parameter to provide path to cert file
    basic_auth=('elastic',ELASTIC_PASSWORD) #baisc_auth is a parameter to provide basic auth details
)

client.info() #instance details or ERROR msg if above line fails to connect to ES
# {'name': 'instance-0000000000', 'cluster_name': ...}

#3) Connecting to multiple host
#The Python Elasticsearch client supports sending API requests to multiple nodes in the cluster. This means that work will be more evenly spread across the cluster instead of hammering the same node over and over with requests. 

#Note-> Even if we give IP and port of only one node(mostly master) it will work but for better performance we should give all node deatils in cluster.
#Like in Pearson PROD we give IP and port of all 19 nodes in spring boot configuration.

# List of nodes to connect
NODES = [
    "https://192.158.220.37:9200",
    "https://192.160.220.12:9200"
]

client = Elasticsearch(
    NODES, #passing the node list to connect to
    ca_certs="/path/to/http_ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

#By default nodes are selected using round-robin, but alternate node selection strategies can be configured with node_selector_class parameter.
#If your Elasticsearch cluster is behind a load balancer like when using Elastic Cloud you won’t need to configure multiple nodes. Instead use the load balancer host and port.

#4)Connecting to Elastic cloud
#When connecting to Elastic Cloud with the Python Elasticsearch client you should always use the cloud_id parameter to connect. You can find this value within the "Manage Deployment" page after you’ve created a cluster (look in the top-left if you’re in Kibana).

# Found in the 'Manage Deployment' page
CLOUD_ID = "deployment-name:dXMtZWFzdDQuZ2Nw..."

# Create the client instance
client = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

client.info()

# Note -> To connect to AZURE, GCP or AWS see documentation page.
# https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/connecting.html#connecting
