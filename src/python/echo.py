#!/usr/bin/env python
import json
import sys
import Node
import Locks


while True:
    line = sys.stdin.readline()
    obj = json.loads(line.rstrip())
    with Locks.stderr:
        sys.stderr.write("Received {}".format(line))
        sys.stderr.flush()
    if 'init' == obj['body']['type']:
        node_id = obj['body']['node_id']
        node = Node.Node(node_id, obj)
    elif 'echo' == obj['body']['type']:
        node.echo(obj)
    elif 'topology' == obj['body']['type']:
        node.topology(obj)
    elif 'broadcast' == obj['body']['type']:
        node.broadcast(obj)
    elif 'read' == obj['body']['type']:
        node.read(obj)


