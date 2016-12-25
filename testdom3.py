#!/usr/bin/python
# Author   : chipmunkdx
# Revision : 
# Id       : 
# Save Script as : create_domain.py
# ==============================================================================
# 
# ------------------------------------------------------------------------------
# Usage and Command option
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
# Handling Property file.
# ------------------------------------------------------------------------------
# Load the properties from the properties file.
from java.io import FileInputStream
 
propInputStream = FileInputStream(properties)
configProps = Properties()
configProps.load(propInputStream)

# ------------------------------------------------------------------------------
# Set Variables.
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
# WebLogic template.
# ------------------------------------------------------------------------------
# Load the template. Versions < 12.2
readTemplate(wlsPath + '/common/templates/wls/wls.jar')

# Load the template. Versions >= 12.2
#selectTemplate('Base WebLogic Server Domain')
#loadTemplates()

# ------------------------------------------------------------------------------
# basic setting for domain.
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
# Start admin server and connection.
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

# ------------------------------------------------------------------------------
# Configuration JDBC Resources.
# ------------------------------------------------------------------------------
#
servermb=getMBean("Servers/examplesServer")
    if servermb is None:
       print '@@@ No server MBean found'
    else:
       def addJDBC(prefix):

       print("")
       print("*** Creating JDBC with property prefix " + prefix)
      
      # Create the Connection Pool.  The system resource will have
      # generated name of <PoolName>+"-jdbc"

      myResourceName = props.getProperty(prefix+"PoolName")
      print("Here is the Resource Name: " + myResourceName)

      jdbcSystemResource = wl.create(myResourceName,"JDBCSystemResource")
      myFile = jdbcSystemResource.getDescriptorFileName()
      print ("HERE IS THE JDBC FILE NAME: " + myFile)
      
      jdbcResource = jdbcSystemResource.getJDBCResource()
      jdbcResource.setName(props.getProperty(prefix+"PoolName"))

      # Create the DataSource Params
      dpBean = jdbcResource.getJDBCDataSourceParams()
      myName=props.getProperty(prefix+"JNDIName")
      dpBean.setJNDINames([myName])

      # Create the Driver Params
      drBean = jdbcResource.getJDBCDriverParams()
      drBean.setPassword(props.getProperty(prefix+"Password"))
      drBean.setUrl(props.getProperty(prefix+"URLName"))
      drBean.setDriverName(props.getProperty(prefix+"DriverName"))

      propBean = drBean.getProperties()
      driverProps = Properties()
      driverProps.setProperty("user",props.getProperty(prefix+"UserName"))

      e = driverProps.propertyNames()
      while e.hasMoreElements() :
	 propName = e.nextElement()
	 myBean = propBean.createProperty(propName)
	 myBean.setValue(driverProps.getProperty(propName))

      # Create the ConnectionPool Params
      ppBean = jdbcResource.getJDBCConnectionPoolParams()
      ppBean.setInitialCapacity(int(props.getProperty(prefix+"InitialCapacity")))
      ppBean.setMaxCapacity(int(props.getProperty(prefix+"MaxCapacity")))
      ppBean.setCapacityIncrement(int(props.getProperty(prefix+"CapacityIncrement")))

      if not props.getProperty(prefix+"ShrinkPeriodMinutes") == None:
         ppBean.setShrinkFrequencySeconds(int(props.getProperty(prefix+"ShrinkPeriodMinutes")))

      if not props.getProperty(prefix+"TestTableName") == None:
	 ppBean.setTestTableName(props.getProperty(prefix+"TestTableName"))

      if not props.getProperty(prefix+"LoginDelaySeconds") == None:
         ppBean.setLoginDelaySeconds(int(props.getProperty(prefix+"LoginDelaySeconds")))
                  
	          # Adding KeepXaConnTillTxComplete to help with in-doubt transactions.
	          xaParams = jdbcResource.getJDBCXAParams()
	          xaParams.setKeepXaConnTillTxComplete(1)

	          # Add Target
	          jdbcSystemResource.addTarget(wl.getMBean("/Servers/examplesServer"))

# ------------------------------------------------------------------------------
# JMS configuration.
# ------------------------------------------------------------------------------
# simple test for JMS configuration.
cd(‘/’)
print ‘Creating JMS Server.’
//Step 1
servermb=getMBean("Servers/examplesServer")
    if servermb is None:
        print '@@@ No server MBean found'

else:
    //Step 2
    jmsMySystemResource = create(myJmsSystemResource,"JMSSystemResource")
    //Step 3
    jmsMySystemResource.addTarget(servermb)

    //Step 4
    theJMSResource = jmsMySystemResource.getJMSResource()

    //Step 5
    connfact1 = theJMSResource.createConnectionFactory(factoryName)
    jmsqueue1 = theJMSResource.createQueue(queueName)
    //Step 6
    connfact1.setJNDIName(factoryName)
    jmsqueue1.setJNDIName(queueName)

    //Step 7
    jmsqueue1.setSubDeploymentName('DeployToJMSServer1')  
    connfact1.setSubDeploymentName('DeployToJMSServer1')
    //Step 8
    jmsserver1mb = create(jmsServerName,'JMSServer')
    //Step 9
    jmsserver1mb.addTarget(servermb)

    //Step 10
    subDep1mb = jmsMySystemResource.createSubDeployment('DeployToJMSServer1')
    //Step 11
    subDep1mb.addTarget(jmsserver1mb)

    # simple test.
    #cmo.createJMSServer(‘JMSServer0′)
    #cd(‘/JMSServers/JMSServer0′)
    #cmo.addTarget(getMBean(‘/Servers/AdminServer’))
    #activate()

    # Creating a Module
    #
    #startEdit()
    # cd(‘/’)
    #cmo.createJMSSystemResource(‘JMSSystemResource0′)
    #cd(‘/JMSSystemResources/JMSSystemResource0′)
    #cmo.addTarget(getMBean(‘/Servers/AdminServer’))
    #cmo.createSubDeployment(’subdeployment0′)
    #activate()

    # Creating Queue
    #
    #startEdit()
    #print ‘Creating Queue & Topic ‘
    #cd(‘/’)
    #cd(‘/JMSSystemResources/JMSSystemResource0/JMSResource/JMSSystemResource0′)
    #cmo.createQueue(‘Queue0′)
    #cd(‘/JMSSystemResources/JMSSystemResource0/JMSResource/JMSSystemResource0/Queues/
    #Queue0′)
    #set(‘JNDIName’,’jms/Queue0′)
    #set(‘SubDeploymentName’,’subdeployment0′)
    #cd(‘/JMSSystemResources/JMSSystemResource0/SubDeployments/subdeployment0′)
    #cmo.addTarget(getMBean(‘/JMSServers/JMSServer0′))
    #activate()

    # Creating Topic

    #startEdit()
    #cd(‘/’)
    #cd(‘/JMSSystemResources/JMSSystemResource0/JMSResource/JMSSystemResource0′)
    #cmo.createTopic(‘Topic0′)
    #cd(‘/JMSSystemResources/JMSSystemResource0/JMSResource/JMSSystemResource0/Topics/
    #Topic0′)
    #set(‘JNDIName’,’jms/Topic0′)
    #set(‘SubDeploymentName’,’subdeployment0′)
    #cd(‘/JMSSystemResources/JMSSystemResource0/SubDeployments/subdeployment0′)
    #set(‘Targets’,jarray.array([ObjectName(‘com.bea:Name=JMSServer0,Type=JMSServer’)],
    #ObjectName))
    
    #activate()

# ------------------------------------------------------------------------------
# Others...
#------------------------------------------------------------------------------
#

# ------------------------------------------------------------------------------
# Admin Server shutdown and Exit.
# ------------------------------------------------------------------------------
#
shutdown(force='true')

exit()

# ------------------------------------------------------------------------------
# End Of Script...
# ------------------------------------------------------------------------------
