import socket
import threading
import os

peer_list = []
rfc_list = []

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
