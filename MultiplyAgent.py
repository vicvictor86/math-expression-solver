import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from CoordenatorAgent import CoordenatorAgent
from makeMessage import makeMessage


class MultiplyAgent(Agent):
    class MultiplyBehav(CyclicBehaviour):
        def generateResult(self, numbers):
            result = 1
            for number in numbers:
                result *= int(number)
            return result

        async def run(self):
            print("MultiplyBehav running")

            # wait for a message for 10 seconds
            msg = await self.receive(timeout=10)
            if msg:
                numbers = msg.body.split(" ")
                result = self.generateResult(numbers)
                msgSend = makeMessage("coordenatoragent@anoxinon.me", result)

                await self.send(msgSend)

                print(f"Result send! ({result})")
                await self.agent.stop()
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            #

    async def setup(self):
        print("ReceiverAgent started")
        multiplyBehav = self.MultiplyBehav()

        template = Template()
        template.set_metadata("performative", "inform")

        self.add_behaviour(multiplyBehav, template)


if __name__ == "__main__":
    receiveragent = MultiplyAgent("cleitin@anoxinon.me", "coxinha123")
    future = receiveragent.start()
    future.result()

    receiveragent.web.start(hostname="127.0.0.1", port="10000")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break

    print("Agents finished")
