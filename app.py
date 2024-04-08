# streamlit_app.py (Streamlit app)
import streamlit as st  ##Streamlit is an open-source Python library that allows you to create interactive web applications directly from Python scripts. 
import requests#This library is commonly used for making HTTP requests, including GET, POST, PUT, DELETE, etc.
import json #The json module provides functions for encoding and decoding JSON data.
from PIL import Image
#import aspose.slides as slides

st.set_page_config(layout="wide") #you're configuring the layout of the Streamlit app to be wide, which means that the app will use more horizontal space. 

###################################################################
image = Image.open('cognizant.jpeg')# open the image as an object
st.image(image,width=200)#st.image() function in Streamlit is used to display images in your Streamlit application.passing image object as an parameter to display the image on UI

st.markdown("<h1 style='text-align: center; color: purple; height: 120px; font-size: 55px ; '>Elasticsearch (Semantic-GenAI) </h1>", unsafe_allow_html=True)
#st.markdown() function in Streamlit is used to display Markdown-formatted text in your Streamlit application. 
#widely used for formatting text on the web.


# Input field for search query
search_query = st.text_input("Enter your search query")
#function in Streamlit is used to create a text input box in your Streamlit application, where users can enter text.

####################################  BUTTTONS ############################################################
#The st.button() function in Streamlit is used to create a button in your Streamlit application. 
# #When the button is clicked by the user, it returns True; otherwise, it returns False.
# # This allows you to trigger actions in your application based on whether the button is clicked or not.
semantic = st.button("Semantic Search")
traditional = st.button("Traditional Search")
image_search=st.button("Image Search")
#################################### SEMANTIC SEARCH ######################################################
# Search button

if semantic: #check if semantic button in clicked or not, if yes will be TRUE else FALSE
    if search_query:
        # Make a POST request to the Flask API
        api_url = "http://127.0.0.1:5001/semanticsearch" #Defining the Flask API URL
        data = {"query_string": search_query} #Passing the input from UI in json format
        response = requests.post(api_url, json=data) #requests.post() function in Python's requests library 
                                    #is used to send an HTTP POST request to a specified URL with JSON data in the request body.
                                    # This is commonly used to interact with APIs by sending data to a server. 
        print(response)

        if response.status_code == 200:
        #In Python's requests library, you can use the status_code attribute of the response object to check the HTTP status code returned by the server.
            global result
            result = response.json()["Results"]
            #it returns the JSON data from the response body. This data is then assigned to the variable result, 
            st.table(result)
            #To display a table using Streamlit's st.table() function, you need to pass the data you want to display as an argument to the function. 
            #Streamlit supports various data types for tables, including Pandas DataFrames, lists of dictionaries, and lists of lists.
        else:
            st.error("Error fetching data from the API")#The st.error() function in Streamlit is used to display an error message in the Streamlit app.


    else:
        st.warning("Please enter a search query")#The st.warning() function in Streamlit is used to display a warning message in the Streamlit app.

#################################  TRADITIONAL SEARCH ###################################
if traditional:
    if search_query:
        # Make a POST request to the Flask API
        api_url = "http://127.0.0.1:5001/traditionalsearch"
        data = {"query_string": search_query}
        response = requests.post(api_url, json=data)
        #print(response)

        if response.status_code == 200:
            global result_traditional
            result_traditional = response.json()["Results"]
            #st.write("Result:", result)
            st.table(result_traditional)
        else:
            st.error("Error fetching data from the API")
    else:
        st.warning("Please enter a search query")

############################ IMAGE SEARCH #################################

if image_search:
    if search_query:
        # Make a POST request to the Flask API
        api_url = "http://127.0.0.1:5001/imagesearch"
        data = {"query_string": search_query}
        response = requests.post(api_url, json=data)
        print(response)

        if response.status_code == 200:
            global result_image
            result_image = response.json()["Results"]
            leng_result_image=len(result_image)#finding the len of result_image list to iterate over it 
        try:
            for i in range(0,leng_result_image): #iterating over all images returned one by one to find out it's image path so that we can display that in UI
                photo_location=result_image[i]['relative_path'] #finding the photo location to open and display it in UI
                st.title("Similar imgae is:")#The st.title() function in Streamlit is used to display a title at the top of the Streamlit app. It is typically used to provide a heading or title for the entire app or for a specific section of the app.
                image = Image.open(photo_location)
                # Display the image
                st.image(image, caption='Similar image', use_column_width=True)##st.image() function in Streamlit is used to display images in your Streamlit application.passing image object as an parameter to display the image on UI

        except:
            st.warning("No Similar image found")