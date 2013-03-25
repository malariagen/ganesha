import os
import urllib2
import ConfigParser
from cmislib.model import CmisClient,Folder

configFileName='alfresco.cfg'
cmisConfigSectionName='cmis_repository'

config = ConfigParser.RawConfigParser()
config.read(configFileName)

def getFiles(folder):
  children= folder.getChildren()
  if not os.path.exists(folder.name):
    os.makedirs(folder.name)
  for child in children:
     print child.name
     print child.__class__
     if (isinstance(child,Folder)):
    # if (child.name == "Population genetics data"):
	getFiles(child)
     else:
       stream = child.getContentStream()
       f = open(folder.name+"/"+child.name,"w")
       for line in stream:
	f.write(line)
       f.close()

client = CmisClient(config.get(cmisConfigSectionName, "serviceUrl"),config.get(cmisConfigSectionName, "user_id"),config.get(cmisConfigSectionName, "password"))
print client
repo = client.defaultRepository
print repo
#someFolder = repo.getObjectByPath('Sites/pf-web-app/documentLibrary/Data')
someFolder = repo.getObject('workspace://SpacesStore/21f48cad-ecc7-4b27-92c2-4a633478e782')
getFiles(someFolder)

# create a password manager
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
jsonConfigSectionName='json_repository'
top_level_url = config.get(jsonConfigSectionName, "top_level")
password_mgr.add_password(None, top_level_url, config.get(cmisConfigSectionName, "user_id"),config.get(cmisConfigSectionName, "password"))

handler = urllib2.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib2.build_opener(handler)

json_url = config.get(jsonConfigSectionName, "studies")
print json_url
# use the opener to fetch a URL
json = opener.open(json_url)

f = open("alfresco.json","w")
for line in json:
  f.write(line)
f.close()
