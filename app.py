from flask import Flask, request, render_template
from chatbot import chatbot_flow


app = Flask(__name__)

@app.route('/', methods=['GET'])
def link():
    return render_template("templates/whatsapp_page.html")

@app.route('/whatsapp', methods=['POST'])
def chatbot():
    chatbot_flow(request)






if __name__ == '__main__':
    app.run(port=4000)