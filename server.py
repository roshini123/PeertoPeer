import socket
import threading
import os

peers = []
rfcs = []
global counter

 class PeerList:
        def __init__(self,hostName="None",port):
                self.hostName=hostName
                self.port=port

 class RFCList:
        def __init__(self,rfcNumber,title="None", hostName="None"):
                self.rfcNumber=rfcNumber
                self.title=title
                self.hostName=hostName

 class PeerThread(threading.Thread):
        def __init__(self, client, addr):
                threading.Thread.__init__(self)
                self.client=client
                self.addr=addr
		self.count=0

	def run(self):
		message=self.client.recv(2048)
		if(self.count==0)
			count++
			addPeer(message)
		datasplit=shlex.split(message)
		req=datasplit[0]
		if req=="ADD":
			titlesplit=message.rsplit('Title:',1)
			title=titlesplit[1].rsplit('ADD',1)
			rfcs.insert(0,RFCList(datasplit[2], title[0], datasplit[5]))


		
 def addPeer(message)
	global counter
	counter=counter+1
	datalist=shlex.split(message)
	peers.insert(0,peerList(datalist[5],datalist[7])
		 

 if __name__ == "__main__"
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
