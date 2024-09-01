class Config:
    OPENAI_API_KEY = '<api key>'
    UPLOAD_FOLDER = '.\\pdfs\\'
    ALLOWED_EXTENSIONS = {'pdf','json'}
    MAX_TOKEN_LIMIT=14000
    PROMPT="""You are an AI assistant who help user to answer user question from below source. 
    You answer should be concise and to the point. Do not generate answer if you can not find it in from below source.
    If you are unable to find answer from source below reply with 'I dont Know'. 
    <source>
    {}
    </source>
    """
