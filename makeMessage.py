from spade.message import Message


def makeMessage(sendTo, result):
    msg = Message(to=sendTo)     # Instantiate the message
    # Set the "inform" FIPA performative
    msg.set_metadata("performative", "inform")
    msg.body = str(result)
    return msg
