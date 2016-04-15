import socket
import os
import time
import platform
import threading

class client_to_client_comm(threading.Thread):
	def __init__(self,client_to_client,ctoc_name):
		self.client_to_client=client_to_client
		self.ctoc_name=ctoc_name 

	def run(self):
		c,addr = self.client_to_client.accept()
		peer_conn=peer_to_download(c,addr)
		peer_conn.start()

class peer_to_download(threading.Thread):
	def __init__(self,peer_obj, peer_addr):
		self.peer_obj=peer_obj
		self.peer_addr=peer_addr

	def run(self):
		message=self.peer_obj.recv(2048)
		if(len(message)!=0):
			datasplit=shlex.split(message)
			if datasplit[3]!='P2P-CI/1.0':
				reply_message='P2P-CI/1.0 505 P2P-CI Version Not Supported\n'+'Date: '+time.asctime()+'\nOS: '+platform.platform()+'\nLast Modified:\nContent Length:\nContent Type: text/text\n'
			elif datasplit[0]!='GET':
				reply_message='P2P-CI/1.0 400 Bad Request\n'+'Date: '+time.asctime()+'\nOS: '+platform.platform()+'\nLast Modified:\nContent Length:\nContent Type: text/text\n'
			else:
				reply_message='P2P-CI/1.0 200 OK\n'+'Date: '+time.asctime()+'\nOS: '+platform.platform()+'\nLast Modified:\nContent Length:\nContent Type: text/text\n'
				filename='RFCList/'+datasplit[1]+datasplit[2]+'.txt'
				f=open(filename,'rb')
				l=f.read(1024)
				while(l):
					reply_message+=l
					l=f.read(1024)
				f.close()
				self.peer_obj.send(reply_message)
				self.peer_obj.close()

if __name__="__main__":
	download_port=7735
	upload_port=int(input("enter the upload port number: ")
	server_ip=input("enter the ip-address of the server host:")
	client_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	ctos_name = socket.gethostname()
	client_to_serv_comm(upload_port,download_port,server_ip,client_to_server,ctos_name)
	

	client_to_client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ctoc_name = socket.gethostname()
	client_to_client.bind ((ctos_name,upload_port))
        client_to_client.listen(10)
	ctoc=client_to_client_comm(client_to_client,ctoc_name)
	ctoc.start()
