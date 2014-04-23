from twisted.internet import reactor
from Hubbot import Hubbot, HubbotFactory
import GlobalVars

class BotHandler:
    botfactories = {}

    def __init__(self):
        for (server_with_port,channels) in GlobalVars.connections.items():
            server = server_with_port.split(":")[0]
            port = int(server_with_port.split(":")[1])
            self.startBotFactory(server, port, channels)
        GlobalVars.bothandler = self
        reactor.run()

    def startBotFactory(self, server, port, channels):
        if server in self.botfactories:
            print "Already on server '{}'.".format(server)
            return False

        print "Joining server '{}'.".format(server)

        botfactory = HubbotFactory(server, port, channels)
        self.botfactories[server] = botfactory
        return True

    def stopBotFactory(self, server, quitmessage="ohok"):
        quitmessage = quitmessage.encode("utf-8")
        if server not in self.botfactories:
            print "ERROR: Bot for '{}' does not exist yet was asked to stop.".format(server)
        else:
            print "Shutting down bot for server '{}'".format(server)
            self.botfactories[server].protocol.quit(quitmessage)
            self.unregisterFactory(server)

    def unregisterFactory(self, server):
        if server in self.botfactories:
            del self.botfactories[server]

            if len(self.botfactories)==0:
                print "No more running bots, shutting down."
                reactor.callLater(2.0, reactor.stop)

if __name__=="__main__":
    bothandler = BotHandler()
