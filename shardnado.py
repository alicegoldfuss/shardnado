#!/usr/bin/env python

'''
SHARDNADO allocates unassigned shards in an Elasticsearch cluster
Author: Alice Goldfuss
'''

import sys
import time
import random
import requests
import json

SHARDNADO = '''
      (        )          (    (         )         (         )   
     )\ )  ( /(   (      )\ ) )\ )   ( /(   (     )\ )   ( /(   
    (()/(  )\())  )\    (()/((()/(   )\())  )\   (()/(   )\())  
     /(_))((_)\((((_)(   /(_))/(_)) ((_)\((((_)(  /(_)) ((_)\   
    (_))   _((_))\ _ )\ (_)) (_))_   _((_))\ _ )\(_))_    ((_)  
    / __| | || |(_)_\(_)| _ \ |   \ | \| |(_)_\(_)|   \  / _ \  
    \__ \ | __ | / _ \  |   / | |) || .` | / _ \  | |) || (_) | 
    |___/ |_||_|/_/ \_\ |_|_\ |___/ |_|\_|/_/ \_\ |___/  \___/                                                       
    ''' 

def main(host):
    # Main method of the script
    # Pulls in shards and nodes in cluster, pushes unassigned back in
    # Prints out report when finished

    print SHARDNADO               

    unassigned_shards = get_shards(host)

    nodes = get_nodes(host)

    number_of_unassigned = len(unassigned_shards)

    print "CLUSTER HAS %s UNASSIGNED SHARD(S)" % str(number_of_unassigned)
    print ""

    if number_of_unassigned == 0:
        return

    print "------------------------------"

    still_unassigned = assign_shards(unassigned_shards, nodes, host)

    print "------------------------------"
    print ""

    if len(still_unassigned) > 0:
        print "ASSIGNED SHARDS: %s" % str(number_of_unassigned - len(still_unassigned))
        print "UNASSIGNED SHARDS: %s" % str(len(still_unassigned))
        for unassigned_shard in still_unassigned:
            print "Index %s, Shard %s" % (unassigned_shard[0], unassigned_shard[1])
        print "------------------------------"
        print ""
        print "Try running script again to assign remaining shards."
        print ""
        return

    print "All shards successfully assigned!"

    return

def get_shards(host):
    # Get all shards in the cluster

    raw_shards = requests.get("http://%s:9200/_cat/shards" % host)

    if raw_shards.status_code != requests.codes.ok:
        raw_shards.raise_for_status()

    return clean_shards(raw_shards)

def get_nodes(host):
    # Get all nodes in the cluster

    raw_nodes = requests.get("http://%s:9200/_cat/nodes?h=host" % host)

    if raw_nodes.status_code != requests.codes.ok:
        raw_nodes.raise_for_status()

    return clean_nodes(raw_nodes)

def clean_shards(raw_shards):
    # Cleans up shards response by fixing the encoding, stripping out
    # unneeded spaces, and only returning the UNASSIGNED shards

    shards = raw_shards.text.split('\n') 

    shards_encode = [shard.encode('UTF8') for shard in shards]

    shards_strip = [" ".join(shard.split()) for shard in shards_encode]

    shards_unassigned = []

    for shard in shards_strip:
        if 'UNASSIGNED' in shard:
            shards_unassigned.append(shard)

    shards_clean = [shard.split() for shard in shards_unassigned]

    return shards_clean

def clean_nodes(raw_nodes):
    # Cleans up nodes response by fixing the encoding and stripping
    # out unneccessary spaces

    nodes = raw_nodes.text.rstrip().split('\n')

    nodes_encode = [node.encode('UTF8') for node in nodes]

    nodes_strip = [" ".join(node.split()) for node in nodes_encode]

    return nodes_strip

def assign_shards(unassigned_shards, nodes, host):
    # Attempts to allocate unassigned shards to random node in cluster
    # Sometimes the node chosen already has that shard data on it and
    # the request is refused

    still_unassigned = []

    for shard in unassigned_shards:
        random_node = random.choice(nodes)

        payload = {"commands" : [ {
                        "allocate" : {
                        "index" : shard[0], 
                        "shard" : shard[1], 
                        "node" : random_node, 
                        "allow_primary" : False
                        }
                    }
                ]
            }

        print "Assigning index %s, shard %s to %s" % (str(shard[0]), str(shard[1]), str(random_node))

        assign_response = requests.post("http://%s:9200/_cluster/reroute" % host, data=json.dumps(payload))

        if assign_response.status_code == requests.codes.ok:
            print ">> SUCCESS"
        else:
            print ">>" + assign_response.text
            still_unassigned.append(shard)

        # Elasticsearch can get overwhelmed by requests, so sleep for 5 seconds
        time.sleep(5)

    return still_unassigned

if __name__ == '__main__':
    # Takes cluster node hostname or IP as argument
    try:
        main(str(sys.argv[1]))
    except KeyboardInterrupt:
        # clean close on CTRL-C
        pass


