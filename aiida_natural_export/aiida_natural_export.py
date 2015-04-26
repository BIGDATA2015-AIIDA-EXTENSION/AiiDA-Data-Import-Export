# paste it into 'verdi shell'

import aiida
import aiida.orm
import aiida.orm.data
import aiida.orm.data.structure
import json

DataFactory = aiida.orm.DataFactory

SD=DataFactory('structure')
q=SD.query()


def write_json_structure(outfile, structure):
        json.dump({"cell": structure.cell,"pbc": structure.pbc,"sites": [x.get_raw() for x in e.sites]}, outfile, indent=4)

with open("text.json", "w+") as outfile:
    for e in q:
        write_json_structure(outfile, e)
