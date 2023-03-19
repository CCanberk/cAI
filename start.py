from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key

app = Flask(__name__)


def format_output(text):
    return text.replace("-", "<br>-")

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/answer", methods=['POST'])
def get_answer():
    category = request.form['category']
    design_line = request.form['design_line']
    user_group = request.form['user_group']
    model = "gpt-3.5-turbo"
    completions = openai.ChatCompletion.create(
        model=model,
        messages=[
             {"role": "system", "content": "Web tasarım önerisi sunan bir AI'sın. Kullanıcıların verdiği site kategorisi, tasarım çizgisi ve kullanıcı grubu bilgilerine göre nasıl bir tasarım anlayışıyla ilerlemeleri gerektiği hakkında önerilerde bulun."},
            {"role": "user", "content": f"Site kategorisi: {category}, tasarım çizgisi: {design_line}, kullanıcı grubu: {user_group}. Bu bilgiler doğrultusunda nasıl bir web tasarımı anlayışı önerirsin?Maddeleri tire işaretiyle birlikte ve satır atlayarak sırala"}
        ]
    )
    message = completions.choices[0].message.content
    formatted_message = format_output(message)
    return render_template("answer.html", message=formatted_message)

if __name__ == "__main__":
    app.run(debug=True)
