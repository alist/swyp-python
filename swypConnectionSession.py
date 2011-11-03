import os, sys, shutil
import select
import socket

class swypConnectionSession():
	
	clientHelloHeader	=	'74;{\n \"tag\" : \"clientHello\",\n \"type\" : \"swyp/ControlPacket\",\n \"length\" : 139}'	
	clientHelloPayload	=	'{\n \"supportedFileTypes\" : [\"image/png\"],\n \"sessionHue\" : \"0.990000,0.440000,0.690000,0.720000",\n \"intervalSinceSwypIn\" : 1.308031022548676}'
	
		
	def __init__(self, remoteServerTuple):
		self.connectionError	=	None
		self._sessionDelegates 	= []
		self._remoteServer 	= remoteServerTuple
		self.serverConnection	= None
		self.start()

	def start(self):	
		address		= self._remoteServer[0]
		port		= self._remoteServer[1]
		serverSocket	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:	
			print ('connecting to: ',address, ' port: ',port)
			serverSocket.connect((address,port))
		except socket.error, msg:
			print ('Connection error: ', socket.error, msg)
			self.connectionError	=	socket.error
		else:
			self.serverConnection = serverSocket
			self.sendClientHelloPacket()
			print('Connected successfully!')
	def update(self):
		self.updateSocket()	

	def updateSocket(self):
		data = self.serverConnection.recv(1024)
  	 	if data:
			print ('Data!: ', repr(data)) 
		
	def sendClientHelloPacket(self):
		self.serverConnection.send(''.join([swypConnectionSession.clientHelloHeader,swypConnectionSession.clientHelloPayload]))

	def stop(self):
		self.serverConnection.close()
	
	def addSessionDelegate(self, delegate):
		self._sessionDelegates.append(delegate)
	
	#observer pattern
	
	#callbacks

