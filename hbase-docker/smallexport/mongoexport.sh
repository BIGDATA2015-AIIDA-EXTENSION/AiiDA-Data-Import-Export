#!/bin/bash
# assuming mongo bin is in your path

host=localhost
port=27017
db=lj

for c in `mongo --quiet $host:$port/$db --eval 'db.getCollectionNames()' | sed 's/,/ /g'`
do
    #if [[ $c != *"system"* ]]; then
    mongoexport --host $host --port $port -d $db -c $c | head -500 > $c.json
    #fi
done
