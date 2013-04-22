from collections import defaultdict
import json
import requests
import sys
from django.template.defaultfilters import slugify
import pprint
import copy
import MySQLdb
import config

def insert_institute(c, insertValues):
    c.executemany(
      """INSERT IGNORE INTO institutes (`institute`, `name`)
      VALUES (%s, %s)""",insertValues)


def insert_affiliations(c, insertValues):
    c.executemany(
      """INSERT IGNORE INTO affiliations (`institute_id`, `contact_person_id`)
      VALUES (%s, %s)""",insertValues)


def insert_contact_person(c, insertValues):
    c.executemany(
      """INSERT IGNORE INTO contact_persons (`contact_person`, `email`, `name`)
      VALUES (%s, %s, %s)""",insertValues)

def insert_studies_contact_person(c, insertValues):
    c.executemany(
      """INSERT IGNORE INTO studies_contact_persons (`study_id`, `contactperson_id`, `contact_type`)
      VALUES (%s, %s, %s)""",insertValues)

def insert_study(c, insertValues):
    c.executemany(
      """INSERT IGNORE INTO studies (`study`, `title`, `study_code`, `legacy_name`, `description`, `alfresco_node`, `web_study_code`, `web_study_legacy_name`)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",insertValues)

def parse_contacts(c, study_contacts, study_id, contact_list, contact_type):

  for af_contact in contact_list:
          name = ' '.join([af_contact['firstName'], af_contact['lastName']])
          affs = af_contact['company'].split(';')
          all_affs = []
          for aff in affs:
            institute = slugify(aff[:100]),aff[:100]
            insts = []
            insts.append(institute)
            insert_institute(c, insts)
            affiliation = slugify(aff[:100]),slugify(name)
            all_affs.append(affiliation)
          contact = slugify(name),af_contact['email'],name
          contacts = []
          contacts.append(contact)
          insert_contact_person(c, contacts)
          insert_affiliations(c, all_affs)
          scp = study_id, slugify(name), contact_type
          scps = []
          scps.append(scp)
          insert_studies_contact_person(c, scps)

def insert_studies(c, alfresco_json):
    #Find those studies and insert them
    contact_URI_by_name = {}
    affiliation_URI_by_name = {}
    study_URI_by_legacy_name = {}
    af = json.load(open(alfresco_json))
    for af_study in af['collaborationNodes']:
                study_id = af_study['name']
                study_code = af_study['name'].split('-')[0]
                study_contacts = []
                other_contacts = []
                studies = []
                web_study = ''
                web_study_legacy = ''
                if 'webStudy' in af_study:
                  web_study = af_study['webStudy']['name']
                  web_study_legacy = af_study['webStudy']['legacyID']
                study = study_id, af_study['webTitle'],study_code,af_study['legacyID'],af_study['description'],af_study['nodeRef'],web_study,web_study_legacy
                studies.append(study)
                insert_study(c, studies)
                parse_contacts(c, study_contacts, study_id, af_study['primaryContacts'], 'lead')
                parse_contacts(c, other_contacts, study_id, af_study['contacts'], 'key')
    return study_URI_by_legacy_name

db=MySQLdb.connect(host=config.DBSRV, user=config.DBUSER, passwd=config.DBPASS, db=config.DB, charset='utf8')
c=db.cursor()

#Insert the two sample set types
study_URI_by_legacy_name = insert_studies(c, 'alfresco.json')

db.commit()
