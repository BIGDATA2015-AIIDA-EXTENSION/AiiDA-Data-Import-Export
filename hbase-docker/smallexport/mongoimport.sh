#!/bin/bash

host=localhost
port=27017
db=lj_small

for f in *.json; do
 echo $f
 col=`echo $f | cut -d. -f1`
 echo $col
 mongoimport --host localhost --db $db --type json --collection $col --file $f
done

