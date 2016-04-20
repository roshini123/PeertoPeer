import socket
import os
import time
import platform
import threading
import shlex

class client_to_serv_comm(threading.Thread):
	def __init__(self,upload_port,download_port,server_ip,client_to_server,ctos_name):
		threading.Thread.__init__(self)
		self.upload_port=upload_port
		self.download_port=download_port
		self.server_ip=server_ip
		self.client_to_server=client_to_server
		self.ctos_name=ctos_name

	#	self.start()
	
	def run(self):
		self.client_to_server.connect((self.server_ip,self.download_port))
		con=1
		while con==1:
			print("\n1.Add RFC\n2.LOOKUP RFC\n3.LISTALL RFCs\n4.Exit\n Enter your choice")
			choice=int(input())	
			if choice==1:
				print("Enter the RFC number:")
				rfcnumber=str(raw_input())
				print("Enter the title of the RFC")
				rfctitle=str(raw_input())
				add_request='ADD RFC '+rfcnumber+' P2P-CI/1.0\nHost: '+str(self.ctos_name)+'\nPort: '+str(self.upload_port)+'\nTitle: '+rfctitle+'\n'
				self.client_to_server.send(add_request)
				add_reply=self.client_to_server.recv(2048)
				print("\n"+add_reply+"\n")
			elif choice==2:
				print("Enter the RFC number to lookup:")
				rfcnumber=str(raw_input())
				print("Enter the RFC title: ")
				rfctitle=str(raw_input())
				lookup_request='LOOKUP RFC '+rfcnumber+' P2P-CI/1.0\nHost: '+self.ctos_name+'\nPort: '+str(self.upload_port)+'\nTitle: '+rfctitle+'\n'
				self.client_to_server.send(lookup_request)
				lookup_reply=self.client_to_server.recv(2048)

				if '200 OK' in lookup_reply:
					lines=lookup_reply.split("\n")
					for i in range(1,len(lines)-1):
						print(lines[i]+"\n")
					print("press 1 to download :")
					val=int(input())
					if val==1:
						print("enter the host name:")
						host=str(raw_input())
						print("enter the download port:")
						port=int(input())
						download_request='GET RFC '+rfcnumber+' P2P-CI/1.0\nHost: '+str(self.ctos_name)+'\nOS: '+platform.platform()+'\n'
						new_rfc_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
						print "done before connect" 
						new_rfc_sock.connect((host,port))
						print "done after connect"
						new_rfc_sock.send(download_request)
						filnam='recvfiles/RFC'+rfcnumber+'.txt'
						data=''
						with open(filnam,'wb') as fs:
        						data+=new_rfc_sock.recv(1024)
        						s,a=data.split("Content Type: text/text\n")
        						fs.write(a)
						fs.close()
						new_rfc_sock.close()
						
				else:
					print(lookup_reply)
			elif choice==3:
				list_request='LIST ALL P2P-CI/1.0\nHost: '+self.ctos_name+'\nPort: '+str(self.upload_port)+'\n'
				self.client_to_server.send(list_request)
				list_reply=self.client_to_server.recv(4098)
				if '200 OK' in list_reply:
					lines=list_reply.split("\n")
					for i in range(1,len(lines)-1):
						print(lines[i]+"\n")
				else:
					print(list_reply)
			elif choice==4:
				con=0
				end_request='END P2P-CI/1.0\nHost: '+self.ctos_name+'\nPort: '+str(self.upload_port)+'\n'
				self.client_to_server.send(end_request)
				end_reply=self.client_to_server.recv(1024)
				print end_reply	
			else:
				print("wrong choice")
		self.client_to_server.close()

	
class client_to_client_comm(threading.Thread):
	def __init__(self,client_to_client,ctoc_name):
		self.client_to_client=client_to_client
		self.ctoc_name=ctoc_name 
		threading.Thread.__init__(self)

	def run(self):
		while True:
			c,addr = self.client_to_client.accept()
			print "accepting done"
			peer_conn=peer_to_download(c,addr)
			peer_conn.start()

class peer_to_download(threading.Thread):
	def __init__(self,peer_obj, peer_addr):
		self.peer_obj=peer_obj
		self.peer_addr=peer_addr
		threading.Thread.__init__(self)

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
				try:
					f=open(filename,'rb')
					l=f.read(1024)
					while(l):
						reply_message+=l
						l=f.read(1024)
					f.close()
				except:
					reply_file='////the content is empty as the requested file does not exist on the requested peer'
				self.peer_obj.send(reply_message)
		#		self.peer_obj.send(reply_file)
				self.peer_obj.close()
				
if __name__=="__main__":
	download_port=7745
	server_ip='127.0.0.87'
	print("enter the upload port number: ")
	upload_port=int(input())
	print("enter the ip-address of the host:")
	ctos_name=str(raw_input())
	client_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print ctos_name+" is the host name"
	c=client_to_serv_comm(upload_port,download_port,server_ip,client_to_server,ctos_name)
	c.start()
	client_to_client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ctoc_name = ctos_name

	client_to_client.bind ((ctoc_name,upload_port))
        client_to_client.listen(10)
	ctoc=client_to_client_comm(client_to_client,ctoc_name)
	ctoc.start()
