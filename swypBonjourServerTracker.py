import os, sys, shutil
pybonjour_folder = os.path.relpath("./lib/pybonjour/")
if pybonjour_folder not in sys.path:
        sys.path.insert(0, pybonjour_folder)
import pybonjour
import select


regtype  = "_swyp._tcp"
timeout  = 5
resolved = []

class swypBonjourServerTracker():
	
	
	def __init__(self):
		self._serverTrackerDelegates = []
		self.start()

	def start(self):
		self.browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
					  callBack = self.browse_callback)

	def update(self):
		ready = select.select([self.browse_sdRef], [], [],0)
		if self.browse_sdRef in ready[0]:
			pybonjour.DNSServiceProcessResult(self.browse_sdRef)
	def stop(self):
		self.browse_sdRef.close()
	
	def addTrackerDelegate(self, delegate):
		self._serverTrackerDelegates.append(delegate)
	
	#observer pattern
	def bonjourServerTrackerResolvedServer(self, serverAddress, serverPort, serverName):
		print 'do something'
	
	def bonjourServerTrackerRemovedServer(self, serverName):
		print 'do something'
	
	#callbacks
	def resolve_callback(self, sdRef, flags, interfaceIndex, errorCode, fullname,
			     hosttarget, port, txtRecord):
		if errorCode == pybonjour.kDNSServiceErr_NoError:
#			print '  fullname   =', fullname
#			print '  hosttarget =', hosttarget
#			print '  port       =', port
			resolved.append(True)
		
		for delegate in self._serverTrackerDelegates:
			delegate.bonjourServerTrackerResolvedServer(hosttarget, port, fullname)

	def browse_callback(self,sdRef, flags, interfaceIndex, errorCode, serviceName,
			    regtype, replyDomain):
	    if errorCode != pybonjour.kDNSServiceErr_NoError:
		return

	    if not (flags & pybonjour.kDNSServiceFlagsAdd):
		for delegate in self._serverTrackerDelegates:
			delegate.bonjourServerTrackerRemovedServer(''.join([serviceName,'.',replyDomain]).replace(' ','-'))
		return

#	    print 'Service found named: ', serviceName , 'in: ',replyDomain, '; resolving')

	    resolve_sdRef = pybonjour.DNSServiceResolve(0,
							interfaceIndex,
							serviceName,
							regtype,
							replyDomain,
						self.resolve_callback)

	    try:
		while not resolved:
		    ready = select.select([resolve_sdRef], [], [], timeout)
		    if resolve_sdRef not in ready[0]:
			print 'Resolve timed out'
			break
		    pybonjour.DNSServiceProcessResult(resolve_sdRef)
		else:
		    resolved.pop()
	    finally:
		resolve_sdRef.close()
	

