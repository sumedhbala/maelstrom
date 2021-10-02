def generate_msg_stub(obj, counter):
    msg = {'src': obj['dest'], 'dest': obj['src'], 'body': {}}
    msg['body']['in_reply_to'] = obj['body']['msg_id']
    msg['body']['msg_id'] = counter
    return msg
