#!/usr/bin/env python
import json
import sys
# from concurrent import futures
from threading import Thread, activeCount

import Node
import Locks
import Logging

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
        Logging.log_stderr("Number of threads active {} {}".format(node.id, activeCount()))
        thread = Thread(target=node.broadcast, args=(obj,))
        thread.start()
    elif 'read' == obj['body']['type']:
        node.read(obj)
    elif 'broadcast_ok' == obj['body']['type']:
        node.handlers[obj['body']['in_reply_to']](obj)
        del node.handlers[obj['body']['in_reply_to']]
