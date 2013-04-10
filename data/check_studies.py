from collections import defaultdict
import csv
import json
import requests
import sys
import pprint


def check_studies(alfresco_json, word_json):
    
    wj = json.load(open(word_json))
    af = json.load(open(alfresco_json))
    for af_study in af['collaborationNodes']:
        for wj_study in wj['collaborationNodes']:
            legacy_study = wj_study['intDescrip']
            if legacy_study == af_study['intDescrip'] or legacy_study == af_study['intDescrip'].split(':')[0] or legacy_study == af_study['title'].split(' ')[0]:
                study_contacts = []
                for wj_contact in wj_study['primaryContacts']:
                  found = False
                  for af_contact in af_study['primaryContacts']:
                    if wj_contact['name'] == af_contact['name']:
                      found = True
                  if not found:
                      print legacy_study + ":Alfresco missing primary contact:" + wj_contact['name']
                for wj_contact in wj_study['contacts']:
                  found = False
                  for af_contact in af_study['contacts']:
                    if wj_contact['name'] == af_contact['name']:
                      found = True
                  if not found:
                      print legacy_study + ":Alfresco missing contact:" + wj_contact['name']
                for af_contact in af_study['primaryContacts']:
                  found = False
                  for wj_contact in wj_study['primaryContacts']:
                    if wj_contact['name'] == af_contact['name']:
                      found = True
                  if not found:
                      print legacy_study + ":Word missing primary contact:" + af_contact['name']
                for af_contact in af_study['contacts']:
                  found = False
                  for wj_contact in wj_study['contacts']:
                    if wj_contact['name'] == af_contact['name']:
                      found = True
                  if not found:
                      print legacy_study + ":word missing contact:" + af_contact['name']



check_studies('alfresco.json', 'doc.json')
