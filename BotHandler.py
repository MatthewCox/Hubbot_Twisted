from twisted.internet import reactor
from Hubbot import Hubbot, HubbotFactory
from FunctionHandler import AutoLoadFunctions
import GlobalVars

class BotHandler:
    botfactories = {}

    def __init__(self):
        for (server_with_port,channels) in GlobalVars.connections.items():
            server = server_with_port.split(":")[0]
            port = int(server_with_port.split(":")[1])
            self.startBotFactory(server, port, channels)
        AutoLoadFunctions()
        GlobalVars.bothandler = self
        reactor.run()

    def startBotFactory(self, server, port, channels):
        if server in self.botfactories:
            print "Already on server '{}'.".format(server)
            return False

        print "Joining server '{}'.".format(server)
        #for chan in channels:
        #    print type(chan)
        botfactory = HubbotFactory(server, port, channels)
        self.botfactories[server] = botfactory
        return True

    def stopBotFactory(self, server, quitmessage=None):
        if quitmessage == None:
            self.quitmessage = "ohok".encode("utf-8")
        else:
            self.quitmessage = quitmessage
        if server not in self.botfactories:
            print "ERROR: Bot for '{}' does not exist yet was asked to stop.".format(server)
        else:
            print "Shutting down bot for server '{}'".format(server)
            self.botfactories[server].protocol.Quitting = True
            self.botfactories[server].protocol.restarting = False
            try:
                self.botfactories[server].protocol.quit(quitmessage)
            except:
                self.botfactories[server].stopTrying()
            self.unregisterFactory(server)
            print "Successfully shut down bot for server '{}'".format(server)

    def unregisterFactory(self, server):
        if server in self.botfactories:
            del self.botfactories[server]

            if len(self.botfactories)==0:
                print "No more running bots, shutting down."
                reactor.callLater(2.0, reactor.stop)

    def shutdown(self, quitmessage="Shutting down..."):
        quitmessage = quitmessage.encode("utf-8")
        for server, botfactory in self.botfactories.iteritems():
            botfactory.protocol.Quitting = True
            botfactory.protocol.restarting = False
            botfactory.protocol.quit(quitmessage)
        self.botfactories = {}
        reactor.callLater(4.0, reactor.stop)

if __name__=="__main__":
    bothandler = BotHandler()
