from flask import Flask, render_template_string, request
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load .env file
load_dotenv()

# Replace 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = os.getenv("CHATGPT_API_KEY")

HTML = '''
<!doctype html>
<title>AI Calculator</title>
<h2>AI Calculator</h2>
<form method=post>
  <input name=expression placeholder="Enter math expression" style="width:300px;">
  <input type=submit value=Calculate>
</form>
{% if result is not none %}
  <h3>Result: {{ result }}</h3>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        expr = request.form['expression']
        prompt = f"Calculate the result of: {expr}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=32,
                temperature=0
            )
            result = response.choices[0].message['content'].strip()
        except Exception as e:
            result = f"Error: {e}"
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(debug=True) 