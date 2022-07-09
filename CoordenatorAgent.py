import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from makeMessage import make_message

class CoordenatorAgent(Agent):
    class CoordenatorBehav(CyclicBehaviour):
        async def run(self):
            print("CoordenatorBehav running")
            msg = make_message("cleitin@anoxinon.me", "2 4 6")

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            # await self.agent.stop()

            msg = await self.receive(timeout=10)
            if msg:
                print("CoordenatorAgent received the message with content {}".format(msg.body))
                await self.agent.stop() 
            
    async def setup(self):
        print("CoordenatorAgent started")

        informBehav = self.CoordenatorBehav()

        self.add_behaviour(informBehav)

class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=10)
            if msg:
                numbers = msg.body.split(" ")
                result = 0
                for number in numbers:
                    result += int(number)
                print("Message received with content: {}".format(result))

            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            # await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        recvBehav = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(recvBehav, template)

if __name__ == "__main__":
    print("Running")

    receiveragent = ReceiverAgent("cleitin@anoxinon.me", "coxinha123")
    future = receiveragent.start()
    future.result()

    senderagent = CoordenatorAgent("vicvictor@anoxinon.me", "clEitonr@cha12")
    senderagent.start()

    receiveragent.web.start(hostname="127.0.0.1", port="10000")
    senderagent.web.start(hostname="127.0.0.1", port="10001")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")