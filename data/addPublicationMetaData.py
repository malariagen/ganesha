import os
import urllib2
import ConfigParser
import MySQLdb
import config
import xml.dom.minidom

opener = urllib2.build_opener()

def updateMetadata(c, pmid):
  print pmid
  # create "opener" (OpenerDirector instance)

  pm_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=' + str(pmid)
  print pm_url

  pubmed = opener.open(pm_url)
  doc = xml.dom.minidom.parse(pubmed)
#  for line in pubmed:
#    print line
  pubmed.close
#Probably overly cautious...
  for node in doc.getElementsByTagName("DateCreated"):
    for n in node.getElementsByTagName("Year"):
      value = ''
      for n1 in n.childNodes:
        value += n1.data
      year = value
    for n in node.getElementsByTagName("Month"):
      value = ''
      for n1 in n.childNodes:
        value += n1.data
      month = value
    for n in node.getElementsByTagName("Day"):
      value = ''
      for n1 in n.childNodes:
        value += n1.data
      day = value
  dateCreated = year + '-' + month + '-' + day
  print str(pmid) + ':' + dateCreated
  c.execute("UPDATE publications SET dateCreated = %s WHERE pmid = %s", (dateCreated,str(pmid)))

db=MySQLdb.connect(host=config.DBSRV, user=config.DBUSER, passwd=config.DBPASS, db=config.DB, charset='utf8')
c=db.cursor()

c.execute("SELECT pmid FROM publications")

rows = c.fetchall()

for row in rows:
  updateMetadata(c,row[0])

db.commit()

