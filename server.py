import socket
import threading
import os

peers = []
rfcs = []
global counter

class PeerList:
        def __init__(self,hostName="None",port=11111):
                self.hostName=hostName
                self.port=port
	def getPort(self, hostName):
		if self.hostName==hostName:
			return self.port
		return "None"
class RFCList:
        def __init__(self,rfcNumber,title="None", hostName="None"):
                self.rfcNumber=rfcNumber
                self.title=title
                self.hostName=hostName

	def getNameofHost(self, number):
		if self.number==number:
			return self.hostName
		return "None"
	
	def getName(self):
		return self.hostName

	def getrfcNumber(self):
		return self.rfcNumber
	
	def getTitle(self):
		return self.title

class PeerThread(threading.Thread):
        def __init__(self, client, addr):
                threading.Thread.__init__(self)
                self.client=client
                self.addr=addr
		self.count=0

	def run(self):
		message=self.client.recv(2048)
		datasplit=shlex.split(message)
		global counter 
		index=0
		if self.count==0:
			self.count=self.count+1
			peers.insert(0,peerList(datasplit[5],datasplit[7]))
			counter=counter+1

		req=datasplit[0]
		if req=="ADD":
			titlesplit=message.rsplit('Title:',1)
			title=titlesplit[1].rsplit('ADD',1)
			rfcs.insert(0,RFCList(datasplit[2], title[0], datasplit[5]))

			index=message.find('ADD',index+3,len(message))
			while(index!=-1):
				tempsplit=shlex.split(title[1])
				titlesplit=title[1].rsplit('Title:',1)
        	                title=titlesplit[1].rsplit('ADD',1)
				rfcs.insert(0,RFCList(tempsplit[1], title[0],tempsplit[4]))
				index=message.find('ADD',index+3,len(message))

		if req=="LOOKUP":
			titlesplit=message.rsplit('Title:',1)
                        title=titlesplit[1]
			
		#	response="P2P-CI/0 "+
	
				

		
	#def lookup(rfcNumber):
			 
	
if __name__ == "__main__":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 7745
        s.bind ((host,port))
        s.listen(10)
        while True:
                c,addr = s.accept()
		peer=PeerThread(c, addr)
                peer.start()	
	s.close()
