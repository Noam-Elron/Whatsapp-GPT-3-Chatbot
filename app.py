from flask import Flask, request, render_template
from chatbot import chatbot_api


app = Flask(__name__)

@app.route('/', methods=['GET'])
def link():
    return render_template("templates/whatsapp_page.html")

@app.route('/whatsapp', methods=['POST'])
def chatbot():
    req = chatbot_api(request)
    return(req)





if __name__ == '__main__':
    app.run(port=4000)