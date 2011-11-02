import os, sys, shutil
import swypBonjourServerTracker
import swypConnectionSession

class swypInteractionManager():

	def __init__(self):
		self.running 		= True
		self.state 		= None
		self.transitioning	= False
		self.serverCandidates	= dict()
		self.activeConnections	= []
		self.serverTracker	= swypBonjourServerTracker.swypBonjourServerTracker()
		self.serverTracker.addTrackerDelegate(self)
	
	def bonjourServerTrackerResolvedServer(self, serverAddress, serverPort, serverName):
		#the server name here is different in that white space is \32 encoded, so the dict doesn't properly function yet-- but ignore for now
		candidate	=	(serverAddress, serverPort, serverName)
		try:
			self.serverCandidates[serverName]
		except:
			self.serverCandidates[serverName] = candidate
			print('added new to candidate list: ',self.serverCandidates)
			self.makeSwypServerConnection(candidate)
		else:
			print('candidate already exists')

	def bonjourServerTrackerRemovedServer(self, serverName):
		if serverName in self.serverCandidates is True:
			del self.serverCandidates[serverName]
			print ('removed!: ', serverName)
		else:
			print ('Candidate non-existant:', serverName)
		
		
	#def __call__(self, *pargs, **kargs):
	#	print('Called:',pargs,kargs)
	#for testing callbacks


	def updateServices(self):
		self.serverTracker.update()
	
	def makeSwypServerConnection(self, serverInfoTuple):
		newSession	=	swypConnectionSession.swypConnectionSession(serverInfoTuple)
		self.activeConnections.append(newSession)
			
	def run(self):
		try:
			try:
				while True:
					self.updateServices()	
			except KeyboardInterrupt:
				pass
		finally:
			self.serverTracker.stop()
mainSwypManager = swypInteractionManager()
mainSwypManager.run()
