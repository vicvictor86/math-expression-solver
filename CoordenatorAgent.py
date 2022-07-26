import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from AdditionAgent import AdditionAgent
from DivisionAgent import DivisionAgent
from EquationAnalysis import resolve_expressao, separa_elementos_string
from makeMessage import makeMessage
from MultiplyAgent import MultiplyAgent
from SubtractionAgent import SubtractionAgent


class CoordenatorAgent(Agent):
    class CoordenatorBehav(CyclicBehaviour):

        async def run(self):
            print("CoordenatorBehav running")
            # data = str(input("Digite a expressão > "))

            # Tratar a expressão para saber qual agente chamar

            data = separa_elementos_string("2-4*3/4")
            print(data)

            while(len(data) > 1):
                operands = resolve_expressao(data)

                onlyNumbersData = f"{operands['x1']} {operands['x2']}"

                # Enviar mensagem para o respectivo agente
                receiveragent = None
                if operands["Op"] == "+":
                    receiveragent = AdditionAgent("sumagent@anoxinon.me", "sum")
                    del(data[data.index('+') + 1])
                    del(data[data.index('+') - 1])
                elif operands["Op"] == "-":
                    receiveragent = SubtractionAgent("minusagent@anoxinon.me", "minus")
                    del(data[data.index('-') + 1])
                    del(data[data.index('-') - 1])
                elif operands["Op"] == "/":
                    receiveragent = DivisionAgent("divisionagent@anoxinon.me", "division")
                    del(data[data.index('/') + 1])
                    del(data[data.index('/') - 1])
                elif operands["Op"] == "^":
                    pass
                    # receiveragent = PotentiationAgent("sumagent@anoxinon.me", "sum")
                elif operands["Op"] == "*":
                    receiveragent = MultiplyAgent("multiplyagent@anoxinon.me", "multiply")
                    del(data[data.index('*') + 1])
                    del(data[data.index('*') - 1])

                await receiveragent.start(auto_register=True)

                print(onlyNumbersData)
                msg = makeMessage(str(receiveragent.jid), onlyNumbersData)

                await self.send(msg)
                print(f"Message sent! ({onlyNumbersData})")

                msg = await self.receive(timeout=10)
                if msg:
                    print(f"Result received! ({msg.body})")

                    data[data.index(operands["Op"])] = msg.body
                    print(f"Solucao: {data}")
                    # self.run(str(data).strip('[]'))
                    # await self.agent.stop()
            print(f"================SOLUCAO FINAL: {data}================")

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
