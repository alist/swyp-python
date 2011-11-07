import os, sys, shutil
import select
import json

class swypSessionPackage():
	def __init__(self, packageTag, payloadFileType, payloadLength):
		self.tag		= packageTag
		self.fileType		= payloadFileType
		self.payloadLength	= payloadLength
		self.payloadData	= []

	def remainingDataNeeded(self):
		return payloadLength - self.payloadData.length()
	
	def addPayloadData (self, data):
		self.payloadData.append(data)
		if self.remainingDataNeeded() > 0:
			return False
		else:
			return True

class swypInputDataDiscerner():

        def __init__(self):
                self._dataDelegates  	= []
		self.pendingPackage	= None
		self.inputData 		= []
	
	def addDataDelegate(self, delegate):
                self._dataDelegates.append(delegate)
		
	def appendInputData(self, newData):
		self.inputData.append(newData)
		self.handleInputData()

	def attemptDiscernNewPackageFromInput(self):
	#find first semi colon, determine if all the data we need is there, then grab until header is over, then parse header, then add new payload		

	def handleInputData(self):
		if self.pendingPackage is None:
			self.attemptDiscernNewPackageFromInput()
		else:
			numberOfBytesToAdd	= min(inputData.length(),self.pendingPackage.remainingDataNeeded())
			complete		= self.pendingPackage.addPayloadData(inputData[0:1+numberOfBytesToAdd])
			inputData[0:1+numberOfBytesToAdd] 	= []
			if complete is True:
				for delegate in self._dataDelegates:
					delegate.swypSessionPackageCompleted(self.pendingPackage)
				self.pendingPackage = None
				print 'Completed package recieve!'
