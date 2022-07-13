import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from AdditionAgent import AdditionAgent
from makeMessage import makeMessage


class CoordenatorAgent(Agent):
    class CoordenatorBehav(CyclicBehaviour):
        async def run(self):
            print("CoordenatorBehav running")
            data = str(input("Digite a expressão > "))

            # Tratar a expressão para saber qual agente chamar

            # Enviar mensagem para o respectivo agente
            receiveragent = AdditionAgent("sumagent@anoxinon.me", "sum")
            await receiveragent.start(auto_register=True)

            msg = makeMessage("sumagent@anoxinon.me", data)

            await self.send(msg)
            print(f"Message sent! ({data})")

            msg = await self.receive(timeout=10)
            if msg:
                print(f"Result received! ({msg.body})")
                # await self.agent.stop()

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
                print(f"Message received with content: {msg.body}")
                await self.agent.stop()
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour

    async def setup(self):
        print("ReceiverAgent started")
        recvBehav = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(recvBehav, template)


if __name__ == "__main__":
    senderagent = CoordenatorAgent("coordenatoragent@anoxinon.me", "coordenator")
    senderagent.start()

    senderagent.web.start(hostname="127.0.0.1", port="2")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            break
    print("Agents finished")
