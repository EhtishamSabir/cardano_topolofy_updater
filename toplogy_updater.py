import json
import requests
from icmplib import multiping


def get_topology_file(continent='eu'):
    """ None for all topology"""
    topology = requests.get("https://a.adapools.org/topology").text
    print(topology)
    with open('out.json', "w+") as f:
        f.write(topology)
    json_object = json.loads(open('out.json', 'r').read())
    ip_port_list = []
    for loc in json_object['Producers']:
        ip = loc['addr']
        ip_port_list.append(ip)
    hosts = multiping(ip_port_list, count=2, interval=0.01, timeout=2, source=None, privileged=True)
    relay_list = json_object['Producers']
    for host, relay in zip(hosts, relay_list):
        if host.is_alive:
            relay['rtt'] = host.avg_rtt
        else:
            relay['rtt'] = -1

    json_object['Producers'] = relay_list
    f_name = 'updated_topology.json'
    with open(f_name, 'w+') as n:
        json.dump(json_object, n, indent=1)
    return f_name


print('updating...')
updated = get_topology_file()
with open('updated_topology.json') as f:
    raw_text = f.read()
    if len(raw_text) < 100:
        exit()
    updated_topology = json.loads(raw_text)
    sorted_relays = sorted(updated_topology['Producers'], key=lambda k: k['rtt'], reverse=False)
top20 = []
for count in range(len(sorted_relays)):
    rel = sorted_relays[count]
    if rel['addr'] == '206.189.4.149':
        print('skiping', rel['addr'])
        continue
    if rel['addr'] == '34.72.59.169':
        print('skiping', rel['addr'])
        continue
    if rel['rtt'] > 0 and count < 3:
        print(rel)
        tmp = {}
        tmp['addr'] = rel['addr']
        tmp['port'] = rel['port']
        tmp['valency'] = rel['valency']
        top20.append(tmp)
        continue
    if rel['rtt'] > 0 and count % 1 == 0:
        print(rel)
        tmp = {}
        tmp['addr'] = rel['addr']
        tmp['port'] = rel['port']
        tmp['valency'] = rel['valency']
        top20.append(tmp)

with open('mainnet-topology-ini.json', 'r') as f:
    ini_object = json.loads(f.read())
    old_objects = ini_object['Producers']

updated_topology['Producers'] = old_objects + top20[:12]

with open('mainnet-topology.json', 'w+') as f:
    json.dump(updated_topology, f, indent=4)
