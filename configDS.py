###################****##############****########################
# Generic script applicable on any Operating Environments (Unix, Windows)
# ScriptName    : ConfigDS.py
# Properties    : ConfigDS.properties
# Author        : Srikanth Panda
# Updated by    : Pavan Devarakonda
###############     Connecting to Start     #################################
def connectAdmin() :
 try:
  connect(CONUSR,CONPWD, CONURL)
  print('Successfully connected')
 except:
  print 'Unable to find admin server...'
  exit()
################### Configuring Connection Pool #############################
def connPool(DSnam) :
 DRVPARM='/JDBCSystemResources/'+DSnam+'/JDBCResource/'+DSnam+'/JDBCDriverParams/'+DSnam
 cd(DRVPARM)
 set('Url',DBURL)
 set('DriverName',DBDRV)
 set('Password',DBPASS)
 cd(DRVPARM+'/Properties/'+DSnam)
 cmo.createProperty('user')
 cd(DRVPARM+'/Properties/'+DSnam+'/Properties/user')
 set('Value',DBUSR)
 
############         Creating Data source    ###############################
def createDS() :
 print('Naming the datasource')
 DSnam = DSName
 cmo.createJDBCSystemResource(DSnam)
 RESOURCE='/JDBCSystemResources/'+DSnam+'/JDBCResource/'+DSnam
 cd(RESOURCE)
 set('Name',DSnam)
 
 #Setting JNDI name
 cd(RESOURCE+'/JDBCDataSourceParams/'+DSnam)
 print RESOURCE+'/JDBCDataSourceParams/'+DSnam
 set('JNDINames',jarray.array([String(DSnam)], String))
 
 connPool(DSnam)
 
 #Set Connection Pool specific parameters
 cd(RESOURCE+'/JDBCConnectionPoolParams/'+DSnam)
 cmo.setTestConnectionsOnReserve(true)
 cmo.setTestTableName('SQL SELECT 1 FROM DUAL')
 cmo.setConnectionReserveTimeoutSeconds(25)
 cmo.setMaxCapacity(15)
 cmo.setConnectionReserveTimeoutSeconds(10)
 cmo.setTestFrequencySeconds(120)
 
 cd(RESOURCE+'/JDBCDataSourceParams/'+DSnam)
 cmo.setGlobalTransactionsProtocol('TwoPhaseCommit')
 cd('/JDBCSystemResources/'+DSnam)
 
 # targets the DS to Servers(Cluster or Server)
 targetType=raw_input('Target to (C)luster or (S)erver: ')
 if targetType in ('C','c') :
  clstrNam=raw_input('Cluster Name: ')
  set('Targets',jarray.array([ObjectName('com.bea:Name='+clstrNam+',Type=Cluster')], ObjectName))
 else:
  servr=raw_input('Server Name: ')
  set('Targets',jarray.array([ObjectName('com.bea:Name='+servr+',Type=Server')], ObjectName))
 
###############     Main Script   #####################################
if __name__== "main":
 print('This will enable you to create or update a Datasource')
 connectAdmin()
 edit()
 startEdit()
 # Create a new JDBC resource)
 cd('/')
 createDS()
 save()
 activate()
 disconnect()
####################################
