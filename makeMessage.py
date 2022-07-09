from spade.message import Message

def make_message(send_to, result):
    msg = Message(to=send_to)     # Instantiate the message
    msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
    msg.body = str(result) 
    return msg