#!/usr/bin/python
# Author : Tim Hall
# Save Script as : create_domain.py

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
import time
import getopt
import sys
import re
import os

# Get location of the properties file.
properties = 'myDomain.properties'
try:
   opts, args = getopt.getopt(sys.argv[1:],"p:h::",["properies="])
except getopt.GetoptError:
   print 'create_domain.py -p <path-to-properties-file>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'create_domain.py -p <path-to-properties-file>'
      sys.exit()
   elif opt in ("-p", "--properties"):
      properties = arg
print 'properties=', properties

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
# Load the properties from the properties file.
from java.io import FileInputStream
 
propInputStream = FileInputStream(properties)
configProps = Properties()
configProps.load(propInputStream)

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
# Set all variables from values in properties file.
wlsPath=configProps.get("path.wls")
domainConfigPath=configProps.get("path.domain.config")
appConfigPath=configProps.get("path.app.config")
domainName=configProps.get("domain.name")
username=configProps.get("domain.username")
password=configProps.get("domain.password")
adminPort=configProps.get("domain.admin.port")
adminAddress=configProps.get("domain.admin.address")
adminPortSSL=configProps.get("domain.admin.port.ssl")
adminServerName=domainName + "Admin"
adminServerUrl=configProps.get("admin.Server.Url")
asu=configProps.get("admin.server.url")
ASU=asu+":"+adminPort

# Display the variable values.
print 'wlsPath=', wlsPath
print 'domainConfigPath=', domainConfigPath
print 'appConfigPath=', appConfigPath
print 'domainName=', domainName
print 'username=', username
print 'password=', password
print 'adminPort=', adminPort
print 'adminAddress=', adminAddress
print 'adminPortSSL=', adminPortSSL
print 'adminServerName=', adminServerName
print 'adminServerUrl=', adminServerUrl
print 'adminServerUrl(ASU)=', ASU

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
# Load the template. Versions < 12.2
readTemplate(wlsPath + '/common/templates/wls/wls.jar')

# Load the template. Versions >= 12.2
#selectTemplate('Base WebLogic Server Domain')
#loadTemplates()

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
# AdminServer settings.
cd('/Security/base_domain/User/' + username)
cmo.setPassword(password)
cd('/Server/AdminServer')
cmo.setName(adminServerName)
cmo.setListenPort(int(adminPort))
cmo.setListenAddress(adminAddress)

# Enable SSL. Attach the keystore later.
#create('AdminServer','SSL')
#cd('SSL/AdminServer')
#set('Enabled', 'True')
#set('ListenPort', int(adminPortSSL))

# If the domain already exists, overwrite the domain
setOption('OverwriteDomain', 'true')

#setOption('ServerStartMode','prod')
setOption('ServerStartMode','dev')
setOption('AppDir', appConfigPath + '/' + domainName)

writeDomain(domainConfigPath + '/' + domainName)
closeTemplate()

domainHome = "/db/domains/" + domainName

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
print "JAVA_HOME %s" % os.getenv("JAVA_HOME")
print "CLASSPATH %s" % os.getenv("CLASSPATH")

try:
    print "try connect to WLS %s" % adminServerName
    hideDumpStack("true")
    connect(username, password, adminServerUrl)
    hideDumpStack("false")
    print "Connected to %s" % adminServerName
except WLSTException:
    hideDumpStack("false")
    print "Server not started, try start %s " % adminServerName
    startServer(adminServerName,domainName,
        adminServerUrl, username, password,
        domainHome,block="true",timeout=0)
    print "started %s" % adminServerName
    connect(username, password, adminServerUrl)

ls()

shutdown(force='true')

exit()

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
