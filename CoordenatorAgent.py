import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from AdditionAgent import AdditionAgent
from DivisionAgent import DivisionAgent
from ExponentiationAgent import ExponentiationAgent
from ExpressionAnalysis import separateString, solve_expression
from makeMessage import makeMessage
from MultiplyAgent import MultiplyAgent
from SubtractionAgent import SubtractionAgent


class CoordenatorAgent(Agent):
    class CoordenatorBehav(CyclicBehaviour):

        async def run(self):
            print("CoordenatorBehav running")

            # Receives a expression from user
            data = separateString(str(input("Digite a expressão > ")))

            # Tratar a expressão para saber qual agente chamar

            # Answer = 25
            # data = separateString("(100 – 413 * (20 – 5 * 4) + 25) / 5")

            # Answer = 32
            # data = separateString("27 + (14 + 3 * (100 / (18 – 4 * 2) + 7) ) / 13")

            # Answer = 180
            # data = separateString("10 * (30 / (2 * 3 + 4) + 15)")

            # Answer = -81
            # data = separateString("25 + (14 – (25 * 4 + 40 – 20))")

            # Answer = -16
            # data = separateString("23 + 12 - 55 + (2 + 4) - 8 / 2 ^ 2")

            # Answer = 30
            # data = separateString("32 + 22 / 2 + 5 - 6 * 3")

            print(data)

            while(len(data) > 1):
                operands = solve_expression(data)

                onlyNumbersData = f"{operands['x1']} {operands['x2']}"

                # Send the message to the agent
                receiveragent = None
                if operands["Op"] == "+":
                    receiveragent = AdditionAgent("sumagent@anoxinon.me", "sum")
                elif operands["Op"] == "-":
                    receiveragent = SubtractionAgent("minusagent@anoxinon.me", "minus")
                elif operands["Op"] == "/":
                    receiveragent = DivisionAgent("divisionagent@anoxinon.me", "division")
                elif operands["Op"] == "^":
                    receiveragent = ExponentiationAgent("exponentiationAgent@anoxinon.me", "exponentiation")
                elif operands["Op"] == "*":
                    receiveragent = MultiplyAgent("multiplyagent@anoxinon.me", "multiply")

                await receiveragent.start(auto_register=True)

                print(onlyNumbersData)
                msg = makeMessage(str(receiveragent.jid), onlyNumbersData)

                await self.send(msg)
                print(f"Message sent! ({onlyNumbersData})")
                msg = await self.receive(timeout=10)
                if msg:
                    print(f"Result received! ({msg.body})")
                    data[operands["n"]] = msg.body
                    del(data[operands['n'] + 1])
                    del(data[operands['n'] - 1])
                    print(f"Answer: {data}")
            print(f"================ FINAL ANSWER: {float(data[0])} ================")

    async def setup(self):
        print("CoordenatorAgent started")

        informBehav = self.CoordenatorBehav()

        self.add_behaviour(informBehav)


if __name__ == "__main__":
    senderagent = CoordenatorAgent("coordenatoragent@anoxinon.me", "coordenator")
    future = senderagent.start()
    future.result()

    senderagent.web.start(hostname="127.0.0.1", port="2")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            break
    print("Agents finished")
