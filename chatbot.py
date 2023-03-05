from twilio.twiml.messaging_response import MessagingResponse
from openai_init import generate_prompt, generate_image
from configparser import ConfigParser
from client import Client

config = ConfigParser()
config.read('config.ini')

def chatbot(request):
    # The request key: "From" contains the extended whatsapp number of the current user
    extended_number = request.form.get("From")
    # The request key: "Body" contains the message the user sent
    incoming_msg = request.values.get('Body', '').lower()
    resp = main_process(extended_number, incoming_msg)
    return str(resp)


def main_process(user_phone_details, incoming_msg):
    resp = MessagingResponse()
    response_msg = resp.message()

    user = Client(user_phone_details)
    
    # If this is a new user then dont do anything except send the user instructions. No need to save data to database other than creating the user and thats implemented in the login method of the Client class.
    if not user.login():
        response_msg.body(config.get("automated_responses", "new_user")) 
        return resp
    
    # If a user's current message is either "Text" or "Image", then dont bother checking last message
    if incoming_msg == "text" or incoming_msg == "image":
        response = f"Input received, prompt type selected: {incoming_msg}. You have one hour to enter your prompt before the session expires"
    else:
        last_message = user.check_last_message()
        img = False
        if last_message == "text":
            response = generate_prompt(incoming_msg, 150)
        elif last_message == "image":
            img = True
            response = generate_image(incoming_msg)
            response_msg.media(response)
        else:
            response = config.get("automated_responses", "help")

    if not img:
        response_msg.body(response)
    
    user.insert_message(incoming_msg)
    user.insert_response(response)
    return resp


