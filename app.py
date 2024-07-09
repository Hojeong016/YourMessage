from flask import Flask, render_template
import threading
import os

app = Flask(__name__)

@app.route('/naver1c9a3278fb62fa5ab61d951fb51c72f1.html')
def serve_file(filename):
    return render_template('',filename)  # 템플릿 폴더에서 파일 서빙

def run_flask():
    app.run(port=8000)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    os.system('streamlit run main.py')
