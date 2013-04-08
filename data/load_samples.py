from collections import defaultdict
import csv
import json
import requests
import sys
from django.template.defaultfilters import slugify
from urlparse import urlparse
import pprint
import ganesha.util.iso_countries as iso_countries

HOST = 'http://localhost:8000'
API = '/api/v1'


def post(object, data):
    headers = {'Content-Type': 'application/json',
               #'Authorization': 'ApiKey ben:204db7bcfafb2deb7506b89eb3b9b715b09905c8'
    }
    r = requests.post(HOST + API + '/' + object + '/', data=json.dumps(data), headers=headers)
    print '========================================='
    print HOST + API + '/' + object + '/'
    pprint.pprint(json.dumps(data))
    if r.text:
        print r.text
    r.raise_for_status()
    return urlparse(r.headers['Location']).path

def URI_from_id(object, id):
    return API + '/' + object + '/' + id + '/'


class Reader:
    def __init__(self, file):
        self.file = open(file, 'r')
        dialect = csv.Sniffer().sniff(self.file.read(2048 * 4))
        self.file.seek(0)
        reader = csv.reader(self.file, dialect)
        #Read a line so we get the fieldnames loaded
        self.field_names = next(reader)
        names = []
        for name in self.field_names:
            names.append(name.split('#')[0])
        self.field_names = names
        self.reader = csv.reader(self.file, dialect)

    def fieldnames(self):
        return self.field_names

    def __iter__(self):
        return self

    def next(self):
        return dict(zip(self.field_names, next(self.reader)))

    def __del__(self):
        self.file.close()


def insert_locations(location_file):
    #Find all the sites and insert them
    location_desc_by_id = {}
    location_URI_by_id = {}
    for line in Reader(location_file):
        location_desc_by_id[line['ID']] = line['Name']
        location = {
            'location': line['ID'],
            'name': ' '.join(line['ID'].split('_')[1:]),
            'name': line['Name'],
            'lattit': line['Latitude'],
            'longit': line['Longitude'],
            'country': line['Country'],
            'description': line['Description']
        }
        location_URI_by_id[line['ID']] = post('location', location)
    return location_URI_by_id, location_desc_by_id


def list_wanted_studies(sample_metadata_file):
    #Find which studies we actually want (those with included samples)
    #TODO Should be all then filtered on release
    wanted_legacy_studies = set()
    for line in Reader(sample_metadata_file):
        if line['Exclude'] != 'TRUE':
            wanted_legacy_studies.add(line['Study'])
    return wanted_legacy_studies


def insert_studies(study_list, alfresco_json):
    #Find those studies and insert them
    contact_URI_by_name = {}
    affiliation_URI_by_name = {}
    study_URI_by_legacy_name = {}
    af = json.load(open(alfresco_json))
    for af_study in af['collaborationNodes']:
        for legacy_study in study_list:
            if legacy_study == af_study['intDescrip'] or legacy_study == af_study['intDescrip'].split(':')[0] or legacy_study == af_study['title'].split(' ')[0]:
                study_contacts = []
                for af_contact in af_study['primaryContacts']:
                    name = ' '.join([af_contact['firstName'], af_contact['lastName']])
                    #Some have no email so have to use name for unique key for now....
                    contact = contact_URI_by_name.get(name, None)
                    if contact is None:
                        contact = {'name': name,
                                   'email': af_contact['email'],
                                   'affiliations': [
                                       {
                                           'institute': {'name': af_contact['company'][:100]},
                                           'url': 'http://',
                                       },
                                   ],
                                   'description': '',
                                   }
#                        affiliation = affiliation_URI_by_name.get(af_contact['company'][:100], None)
#			if affiliation is None:
#			   affiliation = {
#                                           'name': af_contact['company'][:100],
#                                           'institute': af_contact['company'][:50]
#                                       }
#                           affiliation = post('institute', affiliation)
#                           affiliation_URI_by_name[af_contact['company'][:100]] = affiliation
                        contact = post('contact_person', contact)
                        contact_URI_by_name[name] = contact
                    study_contacts.append(contact)
                study = {'study': af_study['name'],
                         'title': af_study['title'].split(' - ')[-1],
                         'legacy_name': legacy_study,
                         'description': af_study['description'],
                         'alfresco_node': af_study['nodeRef'],
                         'people': '',
                         'contact_persons': study_contacts
                }
                study_URI_by_legacy_name[legacy_study] = post('study', study)
    return study_URI_by_legacy_name


def insert_sample_contexts(sample_metadata_file, study_URI_by_legacy_name, location_URI_by_id, location_desc_by_id):
    #Loop over the samples grouping them into sample_contexts
    sample_contexts_by_id = {}
    for line in Reader(sample_metadata_file):
        if line['Exclude'] != 'TRUE':
            sample_context_id = line['Study'] + '_' + line['SiteCode']
            if line['LabSample'] == 'TRUE':
                sample_context_id = line['Study'] + '_' + 'LAB_Lab_Sample'
            if not line['Site']:
                sample_context_id = line['Study'] + '_' + 'XX_Unknown'
            sample_context = sample_contexts_by_id.get(sample_context_id, None)
            if not sample_context:
                sample_context = {
                    'sample_context': sample_context_id,
                    'title': ' '.join(sample_context_id.split('_')[2:]),
                    'description': location_desc_by_id.get(line['Site'], ''),
                    'location': location_URI_by_id[line['SiteCode']],
                    'study': study_URI_by_legacy_name[line['Study']],
                    'samples': []
                }
                sample_contexts_by_id[sample_context_id] = sample_context
            sample_context['samples'].append({
                'sample': line['Sample'],
                'is_public': False,
        })
    for sample_context in sample_contexts_by_id.values():
        post('sample_context', sample_context)

def insert_sample_classification_types():
    sample_classification_types = [
        {
            'name': 'Region',
            'description': 'Used for the calculation of genetic marker frequencies on a detailed geographical scale.',
            'ordr': 2
        },
        {
            'name': 'Subcontinent',
            'description': 'Used for the calculation of SNP allele frequencies.',
            'ordr': 1
        }
    ]
    return dict((sstype['name'], post('sample_classification_type', sstype)) for sstype in sample_classification_types)



def insert_sample_classifications(ss_URI_by_name, sample_metadata_file):
    ss_by_type_by_id = defaultdict(lambda: defaultdict(list))
    types = ['Region', 'SubCont']
    for line in Reader(sample_metadata_file):
        if line['Exclude'] != 'TRUE':
            for t in types:
                ss_by_type_by_id[t][line[t]].append(line['Sample'])
    for t in types:
        for _id, samples in ss_by_type_by_id[t].items():
            post('sample_classification', {
                'sample_classification': _id,
                'sample_classification_type': ss_URI_by_name[t],
                'name': iso_countries.names_by_id.get(_id,_id),
                'lattit': iso_countries.lat_long_by_id.get(_id, (0, 0))[0],
                'longit': iso_countries.lat_long_by_id.get(_id, (0, 0))[1],
                'geo_json': '',
                'samples': [URI_from_id('sample', s) for s in samples]
            })

#Insert the two sample set types
location_URI_by_id, location_desc_by_id = insert_locations('Data/SitesInfo.txt')
studies = list_wanted_studies('Data/metadata-2.2_withsites.txt')
study_URI_by_legacy_name = insert_studies(studies, 'doc.json')
insert_sample_contexts('Data/metadata-2.2_withsites.txt', study_URI_by_legacy_name, location_URI_by_id, location_desc_by_id)
ss_URI_by_name = insert_sample_classification_types()
#Replaced by sql/merge_sample_contexts.sql
#insert_sample_classifications(ss_URI_by_name, 'Data/metadata-2.2_withsites.txt')
