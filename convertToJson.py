import csv
import json

csv_path = 'C:/Users/tyang/Downloads/Senzing/rdc/data/data-senzing-format/cleanedFeature/person-cleanedFeature.csv'
sameEntity = []
lastId = -1

jsonRes = []
csvAddrColumns = ['HOME_ADDR_LINE1','HOME_ADDR_LINE2','HOME_ADDR_CITY','HOME_ADDR_STATE','HOME_ADDR_POSTAL_CODE','HOME_ADDR_COUNTRY']
addressColumns = ['ADDR_LINE1', 'ADDR_LINE2', 'ADDR_CITY', 'ADDR_STATE', 'ADDR_POSTAL_CODE', 'ADDR_COUNTRY']

with open(csv_path, encoding='utf8') as csvFile:
    reader = csv.DictReader(csvFile)

    for row in reader:
        
        if row['RECORD_ID'] == lastId:
            sameEntity.append(row)
        else:
            if len(sameEntity) != 0:
                #1. save current result
                entity = {}
                
                entity['RECORD_ID'] = sameEntity[0]['RECORD_ID']
                entity['NAMES'] = []
                name = {}
                name['NAME_TYPE'] = 'PRIMARY'
                name['NAME_FULL'] = sameEntity[0]['PRIMARY_NAME_FULL']
                entity['NAMES'].append(name)

                if sameEntity[0]['DATE_OF_BIRTH'] != '':
                     entity['DATE_OF_BIRTH'] = sameEntity[0]['DATE_OF_BIRTH']

                sets = [set(), set(), set(), set(), set(), set()]
                for i in range(0, len(sameEntity)):
                    address = {}
                    
                    for j in range(0, len(csvAddrColumns)):
                        if sameEntity[i][csvAddrColumns[j]] !='':
                            if not (sameEntity[i][csvAddrColumns[j]] in sets[j]):
                                address['ADDR_TYPE'] = 'HOME'
                                address[addressColumns[j]] = sameEntity[i][csvAddrColumns[j]]
                                sets[j].add(sameEntity[i][csvAddrColumns[j]])
                    
                    if 'ADDR_TYPE' in address:
                        if not ('ADDRESSES' in entity):
                            entity['ADDRESSES'] = []
                        entity['ADDRESSES'].append(address)
                        
                entity['EventCategories'] = []
                entity['EventSubCategories'] = []
                eventSet = set()

                for i in range(0, len(sameEntity)):
                    if sameEntity[i]['EventCategory'] != '' and sameEntity[i]['EventSubCategory'] != '':
                        if not ((sameEntity[i]['EventCategory'] +',' + sameEntity[i]['EventSubCategory']) in eventSet):
                            entity['EventCategories'].append(sameEntity[i]['EventCategory'])
                            entity['EventSubCategories'].append(sameEntity[i]['EventSubCategory'])
                            eventSet.add(sameEntity[i]['EventCategory'] +',' + sameEntity[i]['EventSubCategory'])

                    if sameEntity[i]['EventCategory'] != '' and sameEntity[i]['EventSubCategory'] == '':
                        if not (sameEntity[i]['EventCategory'] in eventSet):
                            entity['EventCategories'].append(sameEntity[i]['EventCategory'])
                            eventSet.add(sameEntity[i]['EventCategory'])
                    
                    if sameEntity[i]['EventSubCategory'] != '' and sameEntity[i]['EventSubCategory'] == '' :
                        if not (sameEntity[i]['EventSubCategory'] in eventSet):
                            entity['EventSubCategories'].append(sameEntity[i]['EventSubCategory'])
                            eventSet.add(sameEntity[i]['EventSubCategory'])

                jsonRes.append(json.dumps(entity))

            #2. save new data
            sameEntity = []
            sameEntity.append(row)
            lastId = row['RECORD_ID']
           
if len(sameEntity) != 0:
    #1. save current result
    entity = {}
    
    entity['RECORD_ID'] = sameEntity[0]['RECORD_ID']
    entity['NAMES'] = []
    name = {}
    name['NAME_TYPE'] = 'PRIMARY'
    name['NAME_FULL'] = sameEntity[0]['PRIMARY_NAME_FULL']
    entity['NAMES'].append(name)

    if sameEntity[0]['DATE_OF_BIRTH'] != '':
            entity['DATE_OF_BIRTH'] = sameEntity[0]['DATE_OF_BIRTH']

    sets = [set(), set(), set(), set(), set(), set()]
    for i in range(0, len(sameEntity)):
        address = {}
        
        for j in range(0, len(csvAddrColumns)):
            if sameEntity[i][csvAddrColumns[j]] !='':
                if not (sameEntity[i][csvAddrColumns[j]] in sets[j]):
                    address['ADDR_TYPE'] = 'HOME'
                    address[addressColumns[j]] = sameEntity[i][csvAddrColumns[j]]
                    sets[j].add(sameEntity[i][csvAddrColumns[j]])
        
        if 'ADDR_TYPE' in address:
            if not ('ADDRESSES' in entity):
                entity['ADDRESSES'] = []
            entity['ADDRESSES'].append(address)
            
    entity['EventCategories'] = []
    entity['EventSubCategories'] = []
    eventSet = set()

    for i in range(0, len(sameEntity)):
        if sameEntity[i]['EventCategory'] != '' and sameEntity[i]['EventSubCategory'] != '':
            if not ((sameEntity[i]['EventCategory'] +',' + sameEntity[i]['EventSubCategory']) in eventSet):
                entity['EventCategories'].append(sameEntity[i]['EventCategory'])
                entity['EventSubCategories'].append(sameEntity[i]['EventSubCategory'])
                eventSet.add(sameEntity[i]['EventCategory'] +',' + sameEntity[i]['EventSubCategory'])

        if sameEntity[i]['EventCategory'] != '' and sameEntity[i]['EventSubCategory'] == '':
            if not (sameEntity[i]['EventCategory'] in eventSet):
                entity['EventCategories'].append(sameEntity[i]['EventCategory'])
                eventSet.add(sameEntity[i]['EventCategory'])
        
        if sameEntity[i]['EventSubCategory'] != '' and sameEntity[i]['EventSubCategory'] == '' :
            if not (sameEntity[i]['EventSubCategory'] in eventSet):
                entity['EventSubCategories'].append(sameEntity[i]['EventSubCategory'])
                eventSet.add(sameEntity[i]['EventSubCategory'])

    jsonRes.append(json.dumps(entity))

with open('people.json', 'w', encoding='utf-8') as f:
    for i in jsonRes:
        f.write('%s\n' % i)
