from flask import Flask, request, render_template_string
from langchain_ollama import ChatOllama

app = Flask(__name__)
llm = ChatOllama(model="qwen2.5-coder:3b")

HTML_TEMPLATE = """
<!doctype html>
<title>Ollama Chat</title>
<h2>Chat with Qwen2.5-Coder</h2>
<form method=post>
  <input name=prompt style="width: 300px;">
  <input type=submit value=Send>
</form>
{% if response %}
  <p><strong>Response:</strong> {{ response.content }}</p>
{% endif %}
"""


conversation = []

@app.route("/", methods=["GET", "POST"])
def chat():
    response = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        conversation.append(prompt)
        response = llm.invoke(conversation)
        conversation.append(response.content)
    return render_template_string(HTML_TEMPLATE, response=response)

if __name__ == "__main__":
    app.run(debug=True)
