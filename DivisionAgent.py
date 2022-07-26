import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from makeMessage import makeMessage


class DivisionAgent(Agent):
    class DivisionBehav(CyclicBehaviour):
        def generateResult(self, n1, n2):
            return float(n1) / float(n2)

        async def run(self):
            print("DivisionBehav running")

            # wait for a message for 10 seconds
            msg = await self.receive(timeout=10)
            if msg:
                numbers = msg.body.split(" ")
                result = self.generateResult(numbers[0], numbers[1])
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
        divisionBehav = self.DivisionBehav()

        template = Template()
        template.set_metadata("performative", "inform")

        self.add_behaviour(divisionBehav, template)


if __name__ == "__main__":
    receiveragent = DivisionAgent("divisionagent@anoxinon.me", "division")
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
