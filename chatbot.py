from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
from openai_init import generate_prompt, generate_image
from database import Database
from utils import get_number_details


app = Flask(__name__)

@app.route('/', methods=['GET'])
def link():
    return render_template("templates/whatsapp_page.html")

@app.route('/whatsapp', methods=['POST'])
def main():
    incoming_msg = request.values.get('Body', '').lower()
    phone_number_extended = request.form.get("From")

    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    
    user_id, phone_number = get_number_details(phone_number_extended)
    db = Database()
    user_exists: bool = db.check_user(user_id)
    if user_exists is None:
        db.create_user(user_id, phone_number)
        msg.body("""Hello, I've detected that you're a new user. Before we begin let me give you some details on how to use me properly.
                 \nTo create a text generation response include any of these keywords: text, story or default.
                 \nTo create an image generation response include any of these keywords: image, draw or picture.
                 \nIf you ever forget how to use me, just type "help" in chat and you'll receive instructions :).
                 \nNow that you know how what to do, if your previous message was a prompt please repeat it so it can be processed, if not go ahead and create your first response now!""")
        responded = True
        return str(resp)

    else:
        image_resp = False
        text_keywords = ['text', 'story', 'default']
        image_keywords = ['image', 'draw', 'picture']
        chatbot_text = True if len(list(filter(lambda word: True if word in text_keywords else False, incoming_msg.split()))) >= 1 else False
        chatbot_img = True if len(list(filter(lambda word: True if word in image_keywords else False, incoming_msg.split()))) >= 1 else False
        if chatbot_text:
            response = generate_prompt(incoming_msg, 50)
            responded = True
        elif chatbot_img:
            response = generate_image(incoming_msg, 1)
            msg.media(response)
            image_resp = True
            responded = True
        elif 'help' in incoming_msg:
            response = 'To create a text generation response include any of these keywords: text, story or default. \n To create an image generation response include any of these keywords: image, draw or picture.'
        if not responded:
            response = 'Try creating a prompt that includes these keywords \n Text creating: "text", "story", "default". \n Image creation: "image", "draw", "picture".'
        
        if image_resp != True:
            msg.body(response)

        db.insert_message(user_id, incoming_msg)
        db.insert_response(response)
        db.close()
        return str(resp)





if __name__ == '__main__':
    app.run(port=4000)