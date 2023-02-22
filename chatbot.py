from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
from openai_init import generate_prompt, generate_image
from database import ret_db_objects, user_check, create_user

app = Flask(__name__)

#ImmutableMultiDict([('SmsMessageSid', 'SMc3a61a47bc93386f52568bfc243c1ea8'), ('NumMedia', '0'), ('ProfileName', 'Noam Elron'), ('SmsSid', 'SMc3a61a47bc93386f52568bfc243c1ea8'),
# ('WaId', '972542364358'), ('SmsStatus', 'received'), ('Body', 'Generate a story about a dog'), ('To', 'whatsapp:+14155238886'), ('NumSegments', '1'), \
# ('ReferralNumMedia', '0'), ('MessageSid', 'SMc3a61a47bc93386f52568bfc243c1ea8'), ('AccountSid', 'AC6d3755e80d1cdaa15199754fe0b68166'), ('From', 'whatsapp:+972542364358'), ('ApiVersion', '2010-04-01')])

@app.route('/', methods=['GET'])
def link():
    return render_template("templates/whatsapp_page.html")

@app.route('/whatsapp', methods=['POST'])
def main():
    incoming_msg = request.values.get('Body', '').lower()
    phone_number = request.form.get("From")

    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    db, cursor = ret_db_objects()
    user_id, exists = user_check(cursor, phone_number)
    if exists is None:
        create_user(db, cursor, user_id, phone_number)
        msg.body("""Hello, I've detected that you're a new user. Before we begin let me give you some details on how to use me properly.
                 \nTo create a text generation response include any of these keywords: text, story or default.
                 \nTo create an image generation response include any of these keywords: image, draw or picture.
                 \nIf you ever forget how to use me, just type "help" in chat and you'll receive instructions :).
                 \nNow that you know how what to do, if your previous message was a prompt please repeat it so it can be processed, if not go ahead and create your first response now!""")
        responded = True
        return str(resp)


    text_keywords = ['text', 'story', 'default']
    image_keywords = ['image', 'draw', 'picture']
    chatbot_text = True if len(list(filter(lambda word: True if word in text_keywords else False, incoming_msg.split()))) >= 1 else False
    chatbot_img = True if len(list(filter(lambda word: True if word in image_keywords else False, incoming_msg.split()))) >= 1 else False
    if chatbot_text:
        msg.body(generate_prompt(incoming_msg, 50))
        responded = True
    elif chatbot_img:
        msg.media(generate_image(incoming_msg, 1))
        responded = True
    elif 'help' in incoming_msg:
        msg.body('To create a text generation response include any of these keywords: text, story or default. \n To create an image generation response include any of these keywords: image, draw or picture.')
    if not responded:
        msg.body('Try creating a prompt that includes these keywords \n Text creating: "text", "story", "default". \n Image creation: "image", "draw", "picture".')
    return str(resp)






if __name__ == '__main__':
    app.run(port=4000)