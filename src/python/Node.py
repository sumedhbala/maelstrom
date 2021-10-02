import sys
import msg_helper
import json


class Node:
    def __init__(self, node_id, obj):
        self.id = node_id
        self.counter = 1
        msg = msg_helper.generate_msg_stub(obj, self.counter)
        msg['body']['type'] = 'init_ok'
        sys.stderr.write("Initialized node {}\n".format(node_id))
        sys.stderr.flush()
        sys.stdout.write("{}\n".format(json.dumps(msg)))
        sys.stdout.flush()

    def echo(self, obj):
        self.counter += 1
        msg = msg_helper.generate_msg_stub(obj, self.counter)
        msg['body']['type'] = 'echo_ok'
        msg['body']['echo'] = obj['body']['echo']
        sys.stderr.write("Echoing {}\n".format(obj['body']))
        sys.stderr.flush()
        sys.stdout.write("{}\n".format(json.dumps(msg)))
        sys.stdout.flush()

