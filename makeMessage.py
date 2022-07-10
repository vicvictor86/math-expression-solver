from spade.message import Message


def make_message(send_to, result):
    msg = Message(to=send_to)     # Instantiate the message
    # Set the "inform" FIPA performative
    msg.set_metadata("performative", "inform")
    msg.body = str(result)
    return msg
