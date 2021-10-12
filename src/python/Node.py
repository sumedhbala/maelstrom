import json
import time

import Logging
import copy


class Node:
    def __init__(self, node_id, obj):
        self.id = node_id
        self.counter = 1
        self.neighbours = []
        self.messages = set()
        self.messages_list = []
        self.reply(obj, msg_type="init_ok")
        self.handlers = {}

    def echo(self, obj):
        self.reply(obj, msg_type="echo_ok", body_params={'echo': obj['body']['echo']})

    def topology(self, obj):
        self.neighbours = obj['body']['topology'][self.id]
        self.reply(obj, msg_type="topology_ok")

    def broadcast(self, obj):
        def broadcast_ok(msg):
            neighbours.remove(msg['src'])
        self.reply(obj, msg_type="broadcast_ok")
        if obj['body']['message'] not in self.messages:
            self.messages.add(obj['body']['message'])
            self.messages_list.append(obj['body']['message'])
            neighbours = set(self.neighbours) - set([obj['src']])
            while len(neighbours) > 0:
                for node in list(neighbours):
                    self.send(node, copy.deepcopy(obj['body']), broadcast_ok)
                time.sleep(1)
            self.reply(obj, msg_type="broadcast_done {} {}".format(obj['src'], obj['body']['message']))

    def read(self, obj):
        self.reply(obj, msg_type="read_ok", body_params={'messages': self.messages_list})

    def send(self, dest, body, handler=None):
        msg = {'dest': dest, 'src': self.id, 'body': body}
        self.counter += 1
        if handler is not None:
            self.handlers[self.counter] = handler
        msg['body']['msg_id'] = self.counter
        Logging.log_stderr("Sent: {}\n".format(msg))
        Logging.log_stdout("{}\n".format(json.dumps(msg)))

    def reply(self, obj, msg_type, body_params={}):
        body = {}
        body.update(body_params)
        body['in_reply_to'] = obj['body']['msg_id']
        if msg_type is not None:
            body['type'] = msg_type
        self.send(obj['src'], body)
