import json
import requests
from config import Config
import os
from langchain.document_loaders import PyPDFLoader
from flask import Flask, request, jsonify , render_template_string
import tiktoken
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER


def generateAnswer(messages):
    """
    Send a POST request to the OpenAI API to generate an answer based on the given messages.

    Args:
        messages (list): A list of messages to send to the OpenAI API. in the format [{"role": "system", "content": "<system prompt>"},{"role": "user", "content": "Hello!"}]

    Returns:
        dict: A dictionary containing the response from the OpenAI API, with an additional "Success" key indicating whether the request was successful.
    """
    
    url="https://api.openai.com/v1/chat/completions"
    headers={"Content-Type":"application/json","Authorization":"Bearer {}".format(Config.OPENAI_API_KEY)}   
    json_data={
        "model":"gpt-3.5-turbo",
        "messages":messages
    }
    try:
        r=requests.post(url,headers=headers,json=json_data)
        data=r.json()
        data["Success"]=True
        return data
    except Exception as e:
        return {"Success":False,"Message":"Something went wrong. Please try again later.","Error_Message":e}


def read_pdf(file_path):
    """
    Read a PDF file using LangChain's PyPDFLoader and extract text.
    
    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    pdf_text = "\n".join([doc.page_content for doc in documents])
    return pdf_text


def read_json(file_path):
    """
    Read a JSON file containing questions or prompts.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list of questions or prompts.
    """
    with open(file_path, 'r') as file:
            questions = json.load(file)
    return questions

def count_tokens(messages):
    """
    Count the number of tokens used by the OpenAI model for a given set of messages.
    Args:
        messages (list): A list of messages to be sent to the OpenAI API.
    Returns:
        int: The total number of tokens used by the messages.
    """
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = 0
    for message in messages:
        # Tokens in the role
        num_tokens += len(encoding.encode(message['role']))
        # Tokens in the content
        num_tokens += len(encoding.encode(message['content']))    
    return num_tokens




@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle POST requests to the root path, which will be used to upload a PDF and a JSON file.

    If the request is a POST request, the function will check if the request contains both a PDF and a JSON file.
    It will then save the files to the configured upload folder, and use the functions `read_pdf` and `read_json` to read the files.
    If there is an error while reading the files, it will return a JSON response with the error message.

    It will then use the `generateAnswer` function to generate answers to the questions in the JSON file, using the text from the PDF as the source.
    If the number of tokens exceeds the maximum allowed, it will return a JSON response with an error message.
    Otherwise, it will return a JSON response with the answers to the questions.

    If the request is a GET request, it will return a simple HTML form to upload a PDF and a JSON file.
    """
    if request.method == 'POST':
        if "pdf_doc" not in request.files or "json_doc" not in request.files:
            return jsonify({"Success": False, "Message": "Please upload both a PDF and a JSON file."})
        pdf_file = request.files['pdf_doc']
        json_file = request.files['json_doc']
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"Success": False, "Message": "The first file must be a PDF."})
        if not json_file.filename.lower().endswith('.json'):
            return jsonify({"Success": False, "Message": "The second file must be a JSON file."})

        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        json_path = os.path.join(app.config['UPLOAD_FOLDER'], json_file.filename)
        pdf_file.save(pdf_path)
        json_file.save(json_path)
        try:
            pdf_text=read_pdf(pdf_path)
        except:
            return jsonify({"Success":False,"Message":"Invalid PDF File"})
        try:
            questions=read_json(json_path)
        except:
            return jsonify({"Success":False,"Message":"Invalid Json File"})
        if(type(questions)=='list'):
            return jsonify({"Success":False,"Message":"Invalid Json File"})
        results=[]
        for question in questions:
            result={"question":question}
            messages=[
                {"role": "system", "content": Config.PROMPT.format(pdf_text)},
                {"role": "user", "content": question}
            ]
            tokenCount=count_tokens(messages)
            if(tokenCount>Config.MAX_TOKEN_LIMIT):
                result["answer"]="max token excceded"
            else:
                completion = generateAnswer(messages)
                if(completion["Success"] and completion.get("choices")):
                    result["answer"]=completion["choices"][0]["message"]["content"]
                else:
                    result["answer"]="Error in genrating answer"
            results.append(result)
        return jsonify(results)
    else:
        return render_template_string('''
            <!doctype html>
            <title>Upload PDF and JSON</title>
            <h1>Upload PDF and JSON Files</h1>
            <form method="post" enctype="multipart/form-data">
                <label for="pdf_doc">PDF File:</label>
                <input type="file" id="pdf_doc" name="pdf_doc" accept=".pdf"><br><br>
                <label for="json_doc">JSON File:</label>
                <input type="file" id="json_doc" name="json_doc" accept=".json"><br><br>
                <input type="submit" value="Upload">
            </form>
        ''')

if __name__ == "__main__":
    app.run()