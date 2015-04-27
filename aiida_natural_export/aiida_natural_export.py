# paste it into 'verdi shell'

"""
giovannipizzi [10:13 AM]
You can loop over structure.sites
And for each site store the kind_name and the coordinates (3 floats)
If you want to store everything, in case of doubt, both s
Each kind object and each site object (the elements returned by S.kinds and s.sites
Should have a get_raw() method that gives you a storable dict with all the stored info
Which basically is kind_name and positions for the sites
And some info for the kinds, that you won't probably use for the project, but it's good to have in generale
Then it's correct that you store the cell
And if you want to be complete, you can also store structure.pbc, an array of 3 booleans
Which in the data provided should always be [T,T,T]
Pbc= periodic boundary conditions
It says if the system is periodic along the 1st,2nd and 3rd axis
"""


import aiida
import aiida.orm
import aiida.orm.data
import aiida.orm.data.structure
import json

DataFactory = aiida.orm.DataFactory

SD=DataFactory('structure')
q=SD.query()

with open("text.json", "w+") as outfile:
    j=json.JSONEncoder()
    for structure in q:
        outfile.write(j.encode({"uuid": structure.uuid, "cell": structure.cell, "cell_volume": structure.get_cell_volume(), "pbc": structure.pbc,"sites": [x.get_raw() for x in e.sites]})+"\n")


