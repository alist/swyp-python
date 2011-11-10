import os, sys, shutil
import select
import json
import array

class swypSessionPackage():
	def __init__(self, packageTag, payloadFileType, payloadLength):
		self.tag		= packageTag
		self.fileType		= payloadFileType
		self.payloadLength	= payloadLength
		self.payloadData	= array.array('c')

	def remainingDataNeeded(self):
		return self.payloadLength - self.payloadData.buffer_info()[1] 
	
	def addPayloadData (self, data):
		self.payloadData.extend(data)
		if self.remainingDataNeeded() > 0:
			return False
		else:
			return True

class swypInputDataDiscerner():

        def __init__(self):
                self._dataDelegates  	= []
		self.pendingPackage	= None
		self.inputData 		= array.array('c') 
	
	def addDataDelegate(self, delegate):
                self._dataDelegates.append(delegate)
		
	def feedInputData(self, newData):
		self.inputData.extend(newData)
		self.handleInputData()

	def attemptDiscernNewPackageFromInput(self):
	#find first semi colon, determine if all the data we need is there, then grab until header is over, then parse header, then add new payload		
		semicolon		= self.inputData.index(';') #calling self.inputdata[semicolon] gives character before semicolon
		headerLength	 	= 0 
		if semicolon > 0:
			headerLengthStr	= ''.join(self.inputData[0:semicolon])
			headerLength	= int(headerLengthStr)
		if headerLength + semicolon + 1 < self.inputData.buffer_info()[1]:
			self.inputData[0:semicolon+1]	= array.array('c')
			headerString	= ''.join(self.inputData[0:headerLength])
			self.inputData[0:headerLength]   = array.array('c')
			print headerString
			header		= json.loads(headerString)
			if header is not None:
				tag	= header['tag']
				type	= header['type']
				length	= header['length']
				if tag and type and length: 
					print 'found header of:', tag , type , length
					self.pendingPackage	=	swypSessionPackage(tag, type, length)
					self.handleInputData()	
	def handleInputData(self):
		if self.pendingPackage is None:
			self.attemptDiscernNewPackageFromInput()
		else:
			numberOfBytesToAdd	= min(self.inputData.buffer_info()[1],self.pendingPackage.remainingDataNeeded())
			print 'need #bytes:', self.pendingPackage.remainingDataNeeded(), 'have bytes #:', self.inputData.buffer_info()[1]
			complete		= self.pendingPackage.addPayloadData(self.inputData[0:1+numberOfBytesToAdd])
			self.inputData[0:1+numberOfBytesToAdd] 	= array.array('c')
			if complete is True:
				for delegate in self._dataDelegates:
					delegate.swypSessionPackageCompleted(self.pendingPackage)
				self.pendingPackage = None
