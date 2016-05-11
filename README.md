# Shardnado

Allocates Elasticsearch shards for you.

## Paint me a word picture

You get paged at 3am, open your laptop, and discover your Elasticsearch cluster is stuck between a rock and a shard place.

Maybe a node blinked in and out of existence. Maybe a process hiccuped and sent everything running for the hills. Maybe someone else had been working on Elasticsearch and didn't tell you.

All you know is, this cluster is yellow and these shards are stuck.

## Quickstart

Shardado requires Python 2.7 and the requests package to run.

`$ pip install requests`

Then give it either the hostname or IP address of one of your cluster's nodes.

`$ python shardnado.py elasticsearch-node-1.com`

That's it!

```
$ python shardnado.py elasticsearch-node-1.com

      (        )          (    (         )         (         )   
     )\ )  ( /(   (      )\ ) )\ )   ( /(   (     )\ )   ( /(   
    (()/(  )\())  )\    (()/((()/(   )\())  )\   (()/(   )\())  
     /(_))((_)\((((_)(   /(_))/(_)) ((_)\((((_)(  /(_)) ((_)\   
    (_))   _((_))\ _ )\ (_)) (_))_   _((_))\ _ )\(_))_    ((_)  
    / __| | || |(_)_\(_)| _ \ |   \ | \| |(_)_\(_)|   \  / _ \  
    \__ \ | __ | / _ \  |   / | |) || .` | / _ \  | |) || (_) | 
    |___/ |_||_|/_/ \_\ |_|_\ |___/ |_|\_|/_/ \_\ |___/  \___/                                                       
    
CLUSTER HAS 894 UNASSIGNED SHARD(S)

------------------------------
Assigning index test-index-4, shard 2 to elasticsearch-node-2.com
>> SUCCESS
Assigning index test-index-16, shard 0 to elasticsearch-node-6.com
>> SUCCESS
Assigning index test-index-3, shard 4 to elasticsearch-node-1.com
>> SUCCESS
Assigning index test-index-13, shard 3 to elasticsearch-node-5.com
>> SUCCESS
Assigning index test-index-11, shard 2 to elasticsearch-node-3.com
>> SUCCESS
```

## Caveat Emptor

You will probably have to run this more than once.

Currently, Shardnado only tries each shard assignment once. And if the node it chooses already has that index on it, it might fail.

```
>>{"error":{"root_cause":[{"type":"remote_transport_exception","reason":"[elasticsearch-node-6.com][127.0.0.1:9300][cluster:admin/reroute]"}],"type":"illegal_argument_exception","reason":"[allocate] allocation of [test-index-5][3] on node {elasticsearch-node-3.com}{XXXXXXXXXXXXXXX}{127.0.0.1}{127.0.01:9300}{ec2az=us-east-1a, datacenter=use1v} is not allowed, reason: [YES(allocation disabling is ignored)][YES(allocation disabling is ignored)][YES(shard not primary or relocation disabled)][YES(no allocation awareness enabled)][YES(shard is not allocated to same node or host)][YES(node passes include/exclude/require filters)][YES(enough disk for shard on node, free: [1.6tb])][NO(too many shards for this index [test-index-5] on node [2], limit: [2])][YES(primary is already active)][THROTTLE(too many shards currently recovering [3], limit: [2])][YES(target node version [2.2.1] is same or newer than source node version [2.2.1])]"},"status":400}
```

Shardnado will keep track of the shards it failed to assign and print them out at the end of the run. Re-running the script will assign those shards again.

## Testing

You can test Shardnado with nose

`$ pip install nose`

You'll need to run the test server first, so the tests have something to hit.

```
$ python test_server.py
$ nosetests test_shardnado.py
```

## Todo

- Add retry functionality, so shards that fail to assign will try again on a different node
- Moar tests
- Complicated and completely unneccessary title animation


### We choose to use Elasticsearch and do the other things, not because they are easy, but because they are shard.
