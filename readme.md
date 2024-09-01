# Flask PDF and JSON File Processing Application

This is a Flask-based web application that allows users to upload a PDF file and a JSON file. The application extracts text from the PDF, processes the JSON file's content using the OpenAI API, and returns the results as a JSON blob.

## Features

- **PDF Text Extraction**: Extracts text from the uploaded PDF file using LangChain's `PyPDFLoader`.
- **OpenAI API Integration**: Processes questions from the JSON file using the OpenAI GPT-3.5-turbo model.
- **Token Counting**: Estimates the number of tokens used before making the API call to manage within token limits.
- **JSON Response**: Returns a JSON blob with the answers generated for each question in the JSON file.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10+
- Pip

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Ankit130/zania-assignment.git
   cd zania-assignment
   ```
2. **Create a virtual environment** (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your configuration**:

   - Add openai key in config file.

   ```python
   class Config:
       OPENAI_API_KEY = 'your-openai-api-key'  # Your OpenAI API key
       #more variables
   ```

## Running the Application

1. **Start the Flask development server**:

   ```bash
   python app.py
   ```
2. **Access the application**:

   Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1. **Upload Files**:

   - **PDF File**: Upload a PDF document that you want to extract text from.
   - **JSON File**: Upload a JSON file containing questions or prompts in the following format:

   ```json
   [
       "What is the main topic discussed in the document?",
       "Provide a summary of the document."
   ]
   ```
2. **Submit**:

   Click the "Upload" button to submit the files. The application will extract the text from the PDF, process the questions from the JSON file using the OpenAI API, and return the results as a JSON blob.

## Example Response

The response will be a JSON object containing the questions and their corresponding answers:

```json
[
    {
        "question": "What is the main topic discussed in the document?",
        "answer": "The main topic is..."
    },
    {
        "question": "Provide a summary of the document.",
        "answer": "The document discusses..."
    }
]
```
