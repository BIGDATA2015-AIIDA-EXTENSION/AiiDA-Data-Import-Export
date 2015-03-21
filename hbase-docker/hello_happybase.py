import happybase
connection = happybase.Connection('hbase-docker', 9090)
connection.create_table('table-name', { 'family': dict() } )
connection.tables()
table = connection.table('table-name')
table.put('row-key', {'family:qual1': 'value1', 'family:qual2': 'value2'})
for k, data in table.scan():
  print k, data
