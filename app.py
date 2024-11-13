import os
from dotenv import load_dotenv
import google.generativeai as genai
import mysql.connector as mysql
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

app.config["STATIC_URL"] = '/static/'

#GEMINI API
load_dotenv()
#Note: Provide the GEMINI API key in .env file in root folder.
API_KEY = os.getenv('API_KEY') #Load the API key from the environment
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

#Global Variable for Schema
schema = ""

#Global Variable for Database
db = None

#Global Variable for Database Type
db_format = 'sql'


#Fuction to Generate Database QUERY based on Given Prompt.
def generate_query(request):
    prompt = f'''Generate me a database query taking these table attributes
    {schema} and take this: {request} as reference for the query need to be generated and now return the {db_format} query in a following json format ''' + ''' 
    {"query": [query is here]}
'''
    result = model.generate_content([prompt])
    return result


#Fuction to parse the response from API to get the DB QUERY and Executing the Query to get the Required Information.
def get_response(message):
    #Generating the QUERY for given prompt.
    result = generate_query(message)
    try:
        #Parsing the response from API to get QUERY.
        res = result.text
        start_ind, end_ind = -1, -1
        for i in range(len(res)):
            if res[i] == '{':
                start_ind = i
                break
        for i in range(len(res)-1, start_ind, -1):
            if res[i] == '}':
                end_ind = i
                break
        
        print(start_ind, end_ind, res[start_ind], res[end_ind])

        if start_ind == -1 or end_ind == -1:
            raise Exception #if response is not in the form required format rasing Exception

        response = eval(res[start_ind:end_ind+1])

        print(response["query"]) #To Check whether the query exists or not.

    except Exception as e:
        response = f"!! Error Retrieving Data from API Response: {e}" #For debubbing purpose.
        print(response)
        return 0, response #Returning 0 if the request is Failed or Response is unable to parse.
    
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    print("---", result)

    try:
        #Executing the QUERY in Provided Database.
        cursor = db.cursor()
        query = response["query"]
        cursor.execute(query)
        result = cursor.fetchall()
        result.insert(0, [col[0] for col in cursor.description])
        print(">> Data Retrieved Successfully.")
        cursor.close()
    except Exception as e:
        result = f"!! Error Retrieving Data from Database: {e}" #For debubbing purpose.
        print(result)
        return 0, result #Returning 0 if any error occur while executing the QUERY.

    return 1, result[:20] #Returning 1 if execution successful and returning only max 20 entries from the result.


# Basic Chat Responses.
chatbot_responses = {
    "hi": "Hii, How can I help you.",
    "hii": "Hii, How can I help you.",
    "hello": "Hello there!, How can i help you.",
    "how are you": "I'm doing well, thanks for asking!",
    "help": "How can I help you today?",
    "what can you do": "I will help you with analysing your database."
}


# This is the API for CHAT Responses.
@app.route('/chat', methods=['POST'])
def chat():
    print(request.json)
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    print(result)
    user_message = request.json['message']
    response = chatbot_responses.get(user_message.lower(), 0)
    res_type = 0
    if not response:
        success, response = get_response(user_message)
        if not success or not response:
            response = "I didn't understand that."
        elif len(response)<2:
            response = "No Data Found."
        else:
            res_type = 1

    return jsonify({'response': response, 'res_type': res_type})


#This is Page to connect the given DATABASE and to store the SCHEMA in global variables.
@app.route('/bot', methods=['POST'])
def bot():
    global db, schema
    if request.method == 'POST':
        req = request.form
        # print(req)
        db = mysql.connect(
            host=req["host"],
            user=req["user"],
            password=req["password"],
            database=req["database"],
        )
        print(db)
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        result = cursor.fetchall()
        print(result)
        cursor.close()
        schema = req["schema"]
        return render_template('chat.html')
    return render_template('index.html')


##This is Home Page to get the DATABASE Details and SCHEMA with Detailed Description.
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)