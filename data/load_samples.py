import csv
import json
import requests
import sys
from django.template.defaultfilters import slugify
from urlparse import urlparse

HOST = 'http://localhost:8000'
API = '/api/v1'


def post(object, data):
    headers = {'Content-Type': 'application/json',
               #'Authorization': 'ApiKey ben:204db7bcfafb2deb7506b89eb3b9b715b09905c8'
    }
    r = requests.post(HOST + API + '/' + object + '/', data=json.dumps(data), headers=headers)
    r.raise_for_status()
    return urlparse(r.headers['Location']).path


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


paul_id_to_desc = {}
paul_id_to_location = {}
for line in Reader('SitesInfo.txt'):
    paul_id_to_desc[line['ID']] = line['Name']
    location = {
        'location': line['ID'],
        'name': ' '.join(line['ID'].split('_')[1:]),
        'lattit': line['Latitude'],
        'longit': line['Longitude'],
        'country': line['Country'],
        #'sub-continent': line['SubCont'],
    }
    paul_id_to_location[line['ID']] = post('location', location)

unknown_location = post('location', {
    'location': 'UNKNOWN',
    'name': 'Unknown',
    'lattit': None,
    'longit': None,
    'country': None,
    #'sub-continent': line['SubCont'],
})

wanted_legacy_studies = set()
for line in Reader('metadata-2.2_withsites.txt'):
    wanted_legacy_studies.add(line['Study'])

studies = []
contact_persons_by_name = {}
institutes_by_name = {}

af = json.load(open('alfresco121218.json'))
for af_study in af['collaborationNodes']:
    for legacy_study in wanted_legacy_studies:
        if legacy_study in af_study['title']:
            print legacy_study, af_study['name']
            study_contacts = []
            for af_contact in af_study['contacts']:
                name = ' '.join([af_contact['firstName'], af_contact['lastName']])
                #Some have no email so have to use name for unique key for now....
                contact = contact_persons_by_name.get(name, None)
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
                    contact = post('contact_person', contact)
                    contact_persons_by_name[name] = contact
                study_contacts.append(contact)
            study = {'study': af_study['name'],
                     'title': af_study['title'].split(' - ')[-1],
                     'legacy_name': legacy_study,
                     'description': af_study['description'],
                     'alfresco_node': af_study['nodeRef'],
                     'people': '',
                     'contact_persons': study_contacts
            }
            post('study', study)

sample_contexts_by_id = {}
for line in Reader('metadata-2.0.2_withsites.txt'):
    sample_context_id = line['Study'] + '_' + line['Site']
    if line['LabSample'] == 'TRUE':
        sample_context_id = line['Study'] + '_' + 'LAB_Lab_Sample'
    if not line['Site']:
        sample_context_id = line['Study'] + '_' + '??_Unknown'
    sample_context = sample_contexts_by_id.get(sample_context_id, None)
    if not sameple_context:
        sample_context = {
            'sample_context': sample_context_id,
            'title': ' '.join(sample_context_id.split('_')[1:]),
            'description': paul_id_to_desc.get(line['Site'], ''),
            'location': paul_id_to_location.get(line['Site'], unknown_location),
            'study': line['Study']
        }
        sample_contexts_by_id[sample_context_id] = sample_context
    sample_context['samples'].append({
        'ox_code': line['Sample'],
        'excluded': line['Exclude'] == 'TRUE',
        'year': line['Year'],
    })
for sample_context in sample_contexts_by_id.values():
    #SAVE