#' % Draft of a script importing json documents from mongodb json to HBase
#' % Artur Skonecki
#' % 21.04.2015

#' # Intro
#' install Pweave to generate docs: 
#' pypublish -f pdf import_json.py

from IPython.core.debugger import Tracer
import json
from pprint import pprint
import sys

from random import randint

#' HBase does not allow all characters for keys so 
#' only_std_chars leaves only desired chars

def only_std_chars(string):
    return ''.join(e for e in string if (e.isalnum() or e in ['_']))


#' Converts json documents to hbase format.
#' Hbase does not support nested structures, so ZONK for mongodb documents.
#' This function deals with it by using hbase 'families'.
#' Each hbase table can have multiple families.
#' So the hacky way to readd structures from nested documents is to add
#' nested structures that have 'nested' family names'.
#' E.g. Lets take table named *'hulls'*. Inside there are entries with different family names: 
#' *family name **'hulls'** for root level entries*
#' hulls  has subfield *'params_id'* which is a dict
#' This subfield cannot be nested so another family is created
#' *named **'hulls_param_id'** to be referenced from the entry in the root*


def convert(j,basefamily):
    families = {}
    d={}
    families.update(basefamily)
    #print('Family:' + str(basefamily))
    for k,v in j.items():
        if type(v)== type({}):
            #print 'convert DICT ' + k
            #Tracer()()
            d2, families2 = convert(
                    v,
                    {
                        basefamily.keys()[0]+'_'+only_std_chars(k) : dict()
                    }
                )
            d.update(d2)
            families.update(families2)
            d[basefamily.keys()[0] + ':' + only_std_chars(k)] = 'DICT_REFERENCE_TODO'
        elif type(v) == type([]):
            d[basefamily.keys()[0] + ':' + only_std_chars(k)] = 'LIST_REFERENCE_NOT_IMPL'
            pass
        else:
            d[basefamily.keys()[0] + ':' + only_std_chars(k) ] = str(v)
    return d, families


#' Src json with mongodb collection.

src_name = sys.argv[1]

#' Target table in hbase.

table_name = sys.argv[2] if len(sys.argv) > 2 else src_name + str(randint(10,1000)) 

print (table_name)

import happybase


#jT={u'ns': u'lj.params', u'name': u'_id_'}


#' Open source file and read the first json document
#' to determine families for created table.
#' It is not easy to add families to a table later.

families = {}
with open('smallexport/' + src_name + '.json') as f:    
    rowid = 0
    for line in f:
        family_name = src_name
        j = json.loads(line)
        jn, fam = convert(j, {family_name :dict()})
        families.update(fam)
        break # read just a single line to get families

print ('FAMILIES'); print (families)


#' Connect with target hbase instance.

connection = happybase.Connection('hbase-docker', 9090)

#' Create table, display tables, get table handle.

connection.create_table(table_name, families )
connection.tables()
table = connection.table(table_name)


#' Read all json documents from the file and convert them to hbase accepted format.
#' Insert generated entries into opened hbase table.

data=[]
with open('smallexport/'+src_name+'.json') as f:    
    rowid = 0
    for line in f:
        j = json.loads(line)
        data.append(j)
        family_name = src_name
        #Tracer()()
        jn, families = convert(j, {family_name :dict()})
        #print j,jn
        table.put(str(rowid), jn)
        rowid+=1

for k, data in table.scan():
    print k, data

