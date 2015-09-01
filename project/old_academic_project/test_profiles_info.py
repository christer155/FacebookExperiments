# -*- coding: utf-8 -*-
import json
from pprint import pprint
from sets import Set

json_data=open("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\profiles.json")
profiles = json.load(json_data)
json_data.close()

fields=Set()
for id in profiles:
    for field in profiles[id]:
        fields.add(field)
        
"""data=""
for field in fields:
    data += field + '\t'
print data
for person in profiles:
    data=""
    for field in fields:
        print type(profiles[person].get(field, "not found"))
        if type(profiles[person].get(field, "not found")):
            data+=str(profiles[person].get(field, "not found").encode('utf-8'))+"\t"
    print data"""
    
list_p=[element for element in fields]  
    
    #relationship relationship_status
    #locale
    #hometown {u'id': u'101652363207139', u'name': u'Dang, Nepal'}
    # location {u'id': u'108429795855423', u'name': u'Brussels, Belgium'}
    
    #birthday (use the year, or better, create your categories)     1990
    
    
    
    #education [{u'school': {u'id': u'111804802171378', u'name': u'Coll\xe8ge Sainte Gertrude Nivelles'}, u'type': u'High School', u'year': {u'id': u'141778012509913', u'name': u'2008'}}, {u'school': {u'id': u'106084242764763', u'name': u'Universit\xe9 libre de Bruxelles'}, u'type': u'College'}, {u'school': {u'id': u'111910015493987', u'name': u'ULB BE'}, u'type': u'College'}]
    # try fusion with mulitple colulns...
    
    #languages [{u'id': u'108224912538348', u'name': u'French'}, {u'id': u'106059522759137', u'name': u'English'}, {u'id': u'108177092548456', u'name': u'Espa\xf1ol'}]
    
    
    #employer - trop compliqué
    


    
    

key = 'education'
#list_p[16]#16 4
print key
for person in profiles:
    data=profiles[person].get(key, "not found")
    print len(profiles[person].get(key, "not found"))
    print data
print key
print len(list_p)
print list_p



#pprint(fields)