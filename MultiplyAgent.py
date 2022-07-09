import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from makeMessage import make_message
from CoordenatorAgent import CoordenatorAgent

class MultiplyAgent(Agent):
    class MultiplyBehav(CyclicBehaviour):
        def generate_result(self, numbers):
            result = 1
            for number in numbers:
                result *= int(number)
            return result

        async def run(self):
            print("MultiplyBehav running")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                numbers = msg.body.split(" ")

                result = self.generate_result(numbers)
                
                msg_send = make_message("vicvictor@anoxinon.me", result)

                await self.send(msg_send)

                print("MultiplyAgent received the message with content: {}".format(numbers))

            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            # await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        multiplyBehav = self.MultiplyBehav()

        template = Template()
        template.set_metadata("performative", "inform")

        self.add_behaviour(multiplyBehav, template)

if __name__ == "__main__":
    print("Running")

    receiveragent = MultiplyAgent("cleitin@anoxinon.me", "coxinha123")
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