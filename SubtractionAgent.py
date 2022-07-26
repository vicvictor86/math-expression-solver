import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from makeMessage import makeMessage


class SubtractionAgent(Agent):
    class SubtractionBehav(CyclicBehaviour):
        def generateResult(self, numbers):
            result = 0
            result = float(numbers[0]) - float(numbers[1])

            return result

        async def run(self):
            print("SubtractionBehav running")

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
        print("SubtractionAgent started")
        subtractBehav = self.SubtractionBehav()

        template = Template()
        template.set_metadata("performative", "inform")

        self.add_behaviour(subtractBehav, template)


if __name__ == "__main__":
    receiveragent = SubtractionAgent("minusagent@anoxinon.me", "minus")
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
