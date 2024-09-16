import sqlite3, os, json
from datetime import datetime
import google.generativeai as genai
from table_info import table_definitions
from flask import Flask, render_template, request
from sql import main
# import webview


genai.configure(api_key="YOUR_API_KEY")

def get_gemini_model(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([question])
    return response.text

def insert_data(cursor,text,response):
    insert_queries = [
        f'''INSERT INTO metadata VALUES
            ('{text}', '{response}')
        '''
    ]

    for query in insert_queries:
        try:
            cursor.execute(query)
        except Exception as e:
            print(f"Error executing query: {str(e)}")

    print("The values were successfully inserted!!!")

def run_sql_query(db,text,response):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    insert_data(cur,text,response)
    conn.commit()

app = Flask(__name__)
main()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    OUTPUT_DIR = "Output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if request.method == 'POST':
        user_text = request.form['userInput'].strip()

        prompt = "Analyze and tell me whether the news is FAKE,REAL or NOT SURE without any explanations, etc."

        input_text = f"Statement:{user_text}. {prompt}\n\n"

        response = get_gemini_model(input_text)
        data = run_sql_query(db='Data.db',text=user_text,response=response)

    return render_template('results.html', user_input_text=user_text, output=response)

# webview.create_window('News Analyzer', app)

if __name__=='__main__':
    app.run(host='0.0.0.0' ,port=4000, debug=True)
    # webview.start()