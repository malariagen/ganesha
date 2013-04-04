#!/usr/bin/env python2.7
'''
This file opens a docx (Office 2007) file and dumps the text.

If you need to extract text from documents, use this file as a basis for your work.

Part of Python's docx module - http://github.com/mikemaccana/python-docx
See LICENSE for licensing information.
'''
from docx import *
import sys
import csv
import json
import copy

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

def contact_from_string(para):
  fields = para.split(',')
  index = 2
  name = fields[0].strip()
  names = name.split(' ')
  lastName = ' '.join(names[1:])
  email = ''
  if (len(fields) > 1):
    if ('@' in fields[1]):
      email=fields[1].strip()
    else:
      index = 1
  aff = ''
  if (len(fields) > index):
    aff = ','.join(fields[index:]).strip()
  contact = {
    'name': lastName + ", " + names[0],
    'firstName': names[0],
    'lastName': lastName,
    'email': email,
    'company': aff
  }
  return contact

def create_study(paratext, pageNr):
  primary_contacts = []
  contacts = []
  study = { 'title': paratext,
            'name': '',
            'description': '',
            'intDescrip': '',
            'primaryContacts': primary_contacts,
            'contacts': contacts,
            'nodeRef': '',
            'pageNr': pageNr
           }

  return study

if __name__ == '__main__':        
    try:
        document = opendocx(sys.argv[1])
        study_index_file = sys.argv[2]
        newfile = open(sys.argv[3],'w')        
    except:
        print('Please supply an input and output file. For example:')    
        print('''  example-extracttext.py 'My Office 2007 document.docx' 'index' 'outputfile.txt' ''')    
        exit()

    studies_index = {}
    for line in Reader(study_index_file):
      studies_index[line['study']] = line['description']

#<w:pStyle w:val="Heading2"/>

    section_titles = ["Study Title", "Other Non-Partner Study Samples", "Study Description", "Study Overview", "Sub-Study Description", "Lead Partner", "Lead Partner(s)", "Lead Partner(s) and Academic Affiliations", "Key Associates", "Key Associate(s)", "Study Overview", "Publications", "Publications " ]
    '''Return the raw text of a document, as a list of paragraphs.'''
    paratextlist = []
    # Compile a list of all paragraph (p) elements
    paralist = []
    studylist = []
    study = None
    section = None
    pageNr = 1
    #Hackity, hack
    lastPage = 0
    lastTitle = ''
    isLast = False
    for element in document.iter():
        # Find p (paragraph) elements
        if element.tag == '{'+nsprefixes['w']+'}p':
            paralist.append(element)
    # Since a single sentence might be spread over multiple text elements, iterate through each
    # paragraph, appending all text (t) children to that paragraphs text.
    for para in paralist:
        paratext = u''
        heading = False
        # Loop through each paragraph
        for element in para.iter():
            if element.tag == '{'+nsprefixes['w']+'}pStyle' and (element.attrib['{'+nsprefixes['w']+'}val'] == 'Heading2' or element.attrib['{'+nsprefixes['w']+'}val'] == 'style2'):
              heading = True
            elif element.tag == '{'+nsprefixes['w']+'}br' and element.attrib['{'+nsprefixes['w']+'}type'] == 'page':
              pageNr += 1
            elif element.tag == '{'+nsprefixes['w']+'}pageBreakBefore': 
              pageNr += 1
            # Find t (text) elements
            elif element.tag == '{'+nsprefixes['w']+'}t':
                if heading:
                  if element.text and not element.text in section_titles:
                    heading = False
                if heading:
                  section = element.text
                if element.text:
                    paratext = paratext+element.text
            elif element.tag == '{'+nsprefixes['w']+'}tab':
                paratext = paratext + '\t'
        # Add our completed paragraph text to the list of paragraph text
        if not len(paratext) == 0 and heading == False:
            if section and (section == "Study Title"):
              if study:
                studylist.append(study)
              #Assume new study is on a new page (for no hard page breaks)
              if (pageNr == lastPage):
                pageNr += 1
              if (lastTitle.startswith('TRAC')):
                pageNr += 1
              study = create_study(paratext, pageNr)
              lastPage = pageNr
              lastTitle = paratext
            elif section and section == "Other Non-Partner Study Samples":
                if not isLast:
		  study = create_study(paratext, pageNr)
                  study['description'] = study['title']
                  study['title'] = section
                  isLast = True
                else:
                  study['description'] = study['description'] + paratext
            elif section and (section == "Study Description" or section == "Sub-Study Description" or section == "Study Overview"):
              study['description'] = study['description'] + paratext
            elif section and (section == "Lead Partner" or section == "Lead Partner(s)" or section == "Lead Partner(s) and Academic Affiliations"):
              study['primaryContacts'].append(contact_from_string(paratext))
            elif section and (section == "Key Associates" or section == "Key Associate(s)"):
              study['contacts'].append(contact_from_string(paratext))
            #print section + ":" + paratext
            #paratextlist.append(paratext)
    if study:
      studylist.append(study)

    outputlist = []
    for s,page in studies_index.iteritems():
      found = False
      for study in studylist:
        #print s + '#' + page + ' ' + " " + str(study['pageNr'])
        if (str(study['pageNr']) == page):
          newStudy = copy.deepcopy(study)
          newStudy['intDescrip'] = s
          newStudy['name'] = s
          outputlist.append(newStudy)
          found = True
      if not found:
        emptyStudy = create_study('', page)
        emptyStudy['intDescrip'] = s
        emptyStudy['name'] = s
        outputlist.append(emptyStudy)

    output = {
	'collaborationNodes': outputlist
    }
    newfile.write(json.dumps(output))
 # Make explicit unicode version    
   # newparatextlist = []
   # for paratext in paratextlist:
   #     newparatextlist.append(paratext.encode("utf-8"))                  
    
    ## Print our documnts test with two newlines under each paragraph
   # newfile.write('\n\n'.join(newparatextlist))

