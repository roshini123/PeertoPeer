import socket
import threading
import os
import shlex

peers = []
rfcs = []
counter=0
rfclock=threading.Lock()

class PeerList:
        def __init__(self,hostName="None",port=11111):
                self.hostName=hostName
                self.port=port
	def getPort(self, hostName):
		if self.hostName==hostName:
			return self.port
		return "None"
class RFCList:
        def __init__(self,rfcNumber,title, hostName):
                self.rfcNumber=rfcNumber
                self.title=title
                self.hostName=hostName

	def getNameofHost(self, rfcnumber):
		if self.rfcNumber==rfcnumber:
			return self.hostName
		return "None"
	

class PeerThread(threading.Thread):
        def __init__(self, client, addr):
                threading.Thread.__init__(self)
                self.client=client
                self.addr=addr
		self.count=0
		self.hostName="None"
	def sethostName(self,name):
		self.hostName=name
		
	def run(self):
	  con=0
	  while(con==0):
		message=self.client.recv(2048)
		print(message+'\n')	    	
		if(len(message)!=0):
			datasplit=shlex.split(message)
			global counter
			index=0
			if self.count==0:
				self.count=self.count+1
				if datasplit[0]=='LIST':
					self.sethostName(datasplit[4])
					peers.insert(0,PeerList(datasplit[4],int(datasplit[6])))
				else:
					self.sethostName(datasplit[5])
					peers.insert(0,PeerList(datasplit[5],int(datasplit[7])))
				counter=counter+1
	
			req=datasplit[0]
			if req=="ADD":
				titlesplit=message.rsplit('Title: ',1)
				titletemp=titlesplit[1].rsplit('ADD',1)
				title=titletemp[0].split("\n")
				print("1."+str(datasplit[2])+"2."+title[0]+"3."+datasplit[5])
				rfclock.acquire()
				rfcs.insert(0,RFCList(datasplit[2], title[0], datasplit[5]))
				rfclock.release()
				response="P2P-CI/1.0 200 OK"+"\n"	
				self.client.send(response)
			elif req=="LOOKUP":
				hcount=0
				response="P2P-CI/1.0 200 OK"+"\n"
				rfcnumber=str(datasplit[2])
				for x in range(0,len(rfcs)):
					host=rfcs[x].getNameofHost(rfcnumber)
					if(host!="None"):
						hcount=hcount+1
						for y in range(0,len(peers)):
							port=peers[y].getPort(host)
							if(port!="None"):
								response=response+"RFC "+rfcnumber+" "+rfcs[x].title+" "+host+" "+str(port)+"\n"
								break
				if hcount==0:
					response="P2P-CI/1.0 404 Not Found"
				self.client.send(response)
	
			elif req=="LIST":
				response="P2P-CI/1.0 200 OK"+"\n"
				for x in range(0,len(rfcs)):
					for y in range(0,len(peers)):
						if(rfcs[x].hostName==peers[y].hostName):
							response=response+"RFC "+rfcs[x].rfcNumber+" "+rfcs[x].title	+" "+rfcs[x].hostName+" "+str(peers[y].port)+"\n"	
				self.client.send(response)
			else:
				response="P2P-CI/1.0 400 Bad Request"
				self.client.send(response) 
	  else:
			con=1

	  for x in range(0,len(peers)):
		if peers[x].hostName==self.hostName:
			peers.remove(peers[x])
			break
	  for x in range(0,len(rfcs)):
		if rfcs[x].hostName==self.hostName:
			rfcs.remove(rfcs[x])
		
	  self.client.close()		
					 
	
if __name__ == "__main__":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 7745
        s.bind ((host,port))
        s.listen(10)
        while True:
                c,addr = s.accept()
		peer=PeerThread(c, addr)
                peer.start()	
	s.close()
