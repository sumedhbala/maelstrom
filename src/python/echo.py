#!/usr/bin/env python
import json
import sys
import msg_helper
import Node

nodes = {}
while True:
    line = sys.stdin.readline()
    obj = json.loads(line.rstrip())
    sys.stderr.write("Received {}".format(line))

    if 'init' == obj['body']['type']:
        node_id = obj['body']['node_id']
        nodes[node_id] = Node.Node(node_id, obj)
    elif 'echo' == obj['body']['type']:
        node_id = obj['dest']
        nodes[node_id].echo(obj)
