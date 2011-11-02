import os, sys, shutil
pybonjour_folder = os.path.relpath("./lib/pybonjour/")
if pybonjour_folder not in sys.path:
        sys.path.insert(0, pybonjour_folder)
print pybonjour_folder
import pybonjour
import select

name    = "MacLaptop Lest"
regtype = "_swyp._tcp"
port    = 1011


def register_callback(sdRef, flags, errorCode, name, regtype, domain):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        print 'Registered service:'
        print '  name    =', name
        print '  regtype =', regtype
        print '  domain  =', domain


sdRef = pybonjour.DNSServiceRegister(name = name,
                                     regtype = regtype,
                                     port = port,
                                     callBack = register_callback)

try:
    try:
        while True:
            ready = select.select([sdRef], [], [])
            if sdRef in ready[0]:
                pybonjour.DNSServiceProcessResult(sdRef)
    except KeyboardInterrupt:
        pass
finally:
    sdRef.close()
