import json
import Logging
import copy


class Node:
    def __init__(self, node_id, obj):
        self.id = node_id
        self.counter = 1
        self.neighbours = []
        self.messages = set()
        self.messages_list = []
        self.reply(obj, type="init_ok")

    def echo(self, obj):
        self.reply(obj, type="echo_ok", body_params={'echo': obj['body']['echo']})

    def topology(self, obj):
        self.neighbours = obj['body']['topology'][self.id]
        self.reply(obj, type="topology_ok")

    def broadcast(self, obj):
        if obj['body']['message'] not in self.messages:
            self.messages.add(obj['body']['message'])
            self.messages_list.append(obj['body']['message'])
            if 'id' in obj:
                self.reply(obj, type="broadcast_ok")
            for node in self.neighbours:
                self.send(node, copy.deepcopy(obj['body']))

    def read(self, obj):
        self.reply(obj, type="read_ok", body_params={'messages': self.messages_list})

    def send(self, dest, body):
        msg = {'dest': dest, 'src': self.id, 'body': body}
        self.counter += 1
        msg['body']['msg_id'] = self.counter
        Logging.log_stderr("Sent: {}\n".format(msg))
        Logging.log_stdout("{}\n".format(json.dumps(msg)))

    def reply(self, obj, type, body_params={}):
        body = {}
        body.update(body_params)
        body['in_reply_to'] = obj['body']['msg_id']
        if type is not None:
            body['type'] = type
        self.send(obj['src'], body)
