# TODO: Make separate class for tags
 
from time import time
import json
import hashlib
from affinity_redefined.encrypt import Key

class Event:

    def __init__(self, key: Key, kind, tags, content):
        self.public_key = key.public_key
        self.created_at = (time())
        self.kind = kind
        self.tags = tags
        self.content = content
        self.serialized_event = json.dumps([0, self.public_key, self.created_at, self.kind, self.tags, self.content], separators=(',', ':'), ensure_ascii = False).encode('utf8')
        self.id = hashlib.sha256(self.serialized_event).hexdigest()
        self.sig = key.sign(self.id)
        
        