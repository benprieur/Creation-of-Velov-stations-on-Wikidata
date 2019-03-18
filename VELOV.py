# -*- coding: utf-8 -*

import pywikibot
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

import csv, sys



def create_wd_item(site, label_dict):
    new_item = pywikibot.ItemPage(site)
    new_item.editLabels(labels=label_dict, summary=u"Création d'un nouvel élément")
    return new_item.getID()


nature = 'Q61663696'


lieux = {
    'Lyon 1 er': 'Q3337',
    'Lyon 2 ème': 'Q3344',
    'Lyon 3 ème': 'Q3348',
    'Lyon 4 ème': 'Q3351',
    'Lyon 5 ème': 'Q3354',
    'Lyon 6 ème': 'Q3358',
    'Lyon 7 ème': 'Q3360',
    'Lyon 8 ème': 'Q3363',
    'Lyon 9 ème': 'Q3366',
    'VILLEURBANNE':'Q582',
    'CALUIRE-ET-CUIRE':'Q244717',
    'VAULX-EN-VELIN':'Q13596',
    'VENISSIEUX':'Q13598'

}


with open('VELOV.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in reader:
        coords = row[0]
        locadmin = row[6]
        loc = lieux[locadmin]

        libelle = row[2] + " - " + row[3]
        description = 'station de vélopartage Vélo\'v, région lyonnaise, France'

        # create WD
        some_labels = {"fr": libelle}
        new_item_id = create_wd_item(site, some_labels)
        print(new_item_id)

        item = pywikibot.ItemPage(repo, new_item_id)
        item.get()

        claim = pywikibot.Claim(repo, u'P31') # nature de l'élément
        target = pywikibot.ItemPage(repo, 'Q61663696')
        claim.setTarget(target)
        item.addClaim(claim, summary=u'Nature')

        desc = { u'fr': description }
        item.editDescriptions(desc, summary=u'Set description')

        claim = pywikibot.Claim(repo, u'P17') # pays
        target = pywikibot.ItemPage(repo, u'Q142') # France
        claim.setTarget(target)
        item.addClaim(claim, summary=u'Pays')

        claim = pywikibot.Claim(repo, u'P131')  # localisation administrative
        target = pywikibot.ItemPage(repo, loc)
        claim.setTarget(target)
        item.addClaim(claim, summary=u'Localisation')

        claim = pywikibot.Claim(repo, u'P361') # partie de
        target = pywikibot.ItemPage(repo, 'Q4096')
        claim.setTarget(target)
        item.addClaim(claim, summary=u'Partie de')

        latS, lonS = coords.split(',')
        latI = float(latS)
        lonI = float(lonS)
        print(f'Lat: {latI}, lon: {lonI}')

        coordinateclaim = pywikibot.Claim(repo, u'P625')
        coordinate = pywikibot.Coordinate(lat=latI, lon=lonI, precision=0.0001, site=site)
        coordinateclaim.setTarget(coordinate)
        item.addClaim(coordinateclaim, summary=u'Coordinates')

        line_count += 1


