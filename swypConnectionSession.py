import os, sys, shutil
import select
import socket
import swypInputDataDiscerner

class swypConnectionSession():
	
	clientHelloHeader	=	'74;{\n \"tag\" : \"clientHello\",\n \"type\" : \"swyp/ControlPacket\",\n \"length\" : 140}'	
	clientHelloPayload	=	'{\n \"supportedFileTypes\" : [\"image/jpeg\"],\n \"sessionHue\" : \"0.990000,0.440000,0.690000,0.720000",\n \"intervalSinceSwypIn\" : 1.308031022548676}'
	
		
	def __init__(self, remoteServerTuple):
		self.connectionError	=	None
		self._sessionDelegates 	= []
		self._remoteServer 	= remoteServerTuple
		self.serverConnection	= None
		socket.setdefaulttimeout(2)
		self.inputDiscerner	= swypInputDataDiscerner.swypInputDataDiscerner()
		self.inputDiscerner.addDataDelegate(self)
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
		if self.serverConnection is None:
			return	
		ready = select.select([self.serverConnection], [], [],0)
                while self.serverConnection in ready[0]: 
			print 'ready to recv data!'
			data = self.serverConnection.recv(1024)
  	 		if data:
#				print 'Data!: "',repr(data),'"'
				self.inputDiscerner.feedInputData(data)
			else:
				self.serverConnection.close() 
				self.serverConnection = None
				return
			ready = select.select([self.serverConnection], [], [],0)
			
	def sendClientHelloPacket(self):
		self.serverConnection.send(''.join([swypConnectionSession.clientHelloHeader,swypConnectionSession.clientHelloPayload]))

	def stop(self):
		if self.serverConnection is not None:
			self.serverConnection.close()
	
	def addSessionDelegate(self, delegate):
		self._sessionDelegates.append(delegate)
	
	#delegation from discerner
	def swypSessionPackageCompleted(self, completedPackage):
		print 'recieved package of type!: ', completedPackage.fileType
		if completedPackage.fileType == "image/png":
			imageLocation	= './received/image.png'
			print 'wrote out image!! to ', imageLocation
			imageFile	= open(imageLocation, 'w')
			completedPackage.payloadData.tofile(imageFile)
			imageFile.close()
		if completedPackage.fileType == "image/jpeg":
			imageLocation	= './received/image.jpeg'
			print 'wrote out image!! to ', imageLocation
			imageFile	= open(imageLocation, 'w')
			completedPackage.payloadData.tofile(imageFile)
			imageFile.close()


	#observer pattern
	
	#callbacks

