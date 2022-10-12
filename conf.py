import uuid

host = '192.168.50.163' #'localhost'
ae_name = 'SJU'
protocol = 'http'

conf = {}
cse = {}
ae = {}
cnt = {}

conf['useprotocol'] = protocol

cse['host'] = host
cse['port'] = '7579'
cse['name'] = 'Mobius'
cse['id'] = '/Mobius2'
cse['mqttport'] = '1883'
cse['wsport'] = '7577'


ae['name'] = ae_name
ae['id'] = 'S' + ae_name
ae['parent'] = '/' + cse['name']
ae['appid'] = str(uuid.uuid1())
ae['bodytype'] = 'json'  # select 'json' or 'xml' or 'cbor


cnt['parent'] = ae['parent'] + '/' + ae['name']

conf['cse'] = cse
conf['ae'] = ae
conf['cnt'] = cnt