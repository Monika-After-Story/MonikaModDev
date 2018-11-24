# Script used to take care of generating the pickles used by the nlp module
# These will be put inside the folder pickles inside the game folder
# VER: py 2.7


import csv
import pickle
import gamedir as GDIR
import os

# default pickle location
PICKLES_DIR = os.path.normcase( GDIR.REL_PATH_GAME + '/pickles/' )

#
# Pickles for the Morphy Class
#

NOUNS_TSV = 'noun.exc'
ADJS_TSV = 'adj.exc'
ADVS_TSV = 'adv.exc'
VERBS_TSV = 'verb.exc'

NOUNS_PKL = 'nouns.pickle'
ADJS_PKL = 'adjs.pickle'
ADVS_PKL = 'advs.pickle'
VERBS_PKL = 'verbs.pickle'

def generate_morphy_pickles():
    nouns = {}
    with open(NOUNS_TSV) as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            nouns[row["variant"]] = row["root"]
    
    adjs ={}
    with open(ADJS_TSV) as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            adjs[row["variant"]] = row["root"]
    advs ={}
    with open(ADVS_TSV) as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            adjs[row["variant"]] = row["root"]
    verbs ={}
    with open(VERBS_TSV) as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            verbs[row["variant"]] = row["root"]    
    
    with open(PICKLES_DIR + NOUNS_PKL, 'wb') as handle:
        pickle.dump(nouns, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(PICKLES_DIR + ADJS_PKL, 'wb') as handle:
        pickle.dump(adjs, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(PICKLES_DIR + ADVS_PKL, 'wb') as handle:
        pickle.dump(advs, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(PICKLES_DIR + VERBS_PKL, 'wb') as handle:
        pickle.dump(verbs, handle, protocol=pickle.HIGHEST_PROTOCOL)

