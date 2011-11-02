import os, sys, shutil
import select
import socket

class swypConnectionSession():
	
	
	def __init__(self, remoteServerTuple):
		self._sessionDelegates 	= []
		self._remoteServer 	= remoteServerTuple
		self.start()

	def start(self):	
		address		= self._remoteServer[0]
		port		= self._remoteServer[1]
		serverSocket	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			serverSocket.connect((address,port))
		except socket.error, msg:
			print ('Connection error: ', socket.error, msg)
		else:
			self.serverConnection = serverSocket
			print('Connected successfully!')
	def update(self):
		pass

	def stop(self):
		serverConnection.close()
	
	def addSessionDelegate(self, delegate):
		self._sessionDelegates.append(delegate)
	
	#observer pattern
	
	#callbacks

