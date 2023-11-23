from time import time
import json
import hashlib
from affinity_redefined.encrypt import Key

class Event:

    METADATA_KIND = 0
    TEXT_NOTE_KIND = 1
    UPDATE_RELAY_LIST = 15000
    NEW_RELAY_ADDITION = 15001

    def __init__(self, key: Key, kind, tags, content):
        self.public_key = key.public_key
        self.created_at = (time())
        self.kind = kind
        self.tags = tags
        self.content = content
        self.serialized_event = json.dumps([0, self.public_key, self.created_at, self.kind, self.tags, self.content], separators=(',', ':'), ensure_ascii = False).encode('utf8')
        self.id = hashlib.sha256(self.serialized_event).hexdigest()
        self.sig = key.sign(self.id)
        self.json_string = json.dumps({"id":self.id, "pubkey":self.public_key, "created_at":self.created_at, "kind": self.kind, "tags":self.tags, "content": self.content, "sig": self.sig}, separators=(',',':'), ensure_ascii=False).encode('utf8')
        
        

class RelayListEvent(Event):
    def __init__(self, key: Key, content):
        #Pass server instance instead of content so that automatically able to fetch list
        Event.__init__(self, key = key, kind = 15000, tags = ['z',], content = content)

