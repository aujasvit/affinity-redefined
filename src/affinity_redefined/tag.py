from copy import deepcopy

class TagArray:
    def __init__(self, tags = []):
        # tags should either be TagArray or an array of Tag's
        assert type(tags) == list or type(tags) == TagArray

        if type(tags) == TagArray:
            # If tag array is already given, just create deep copy
            self = deepcopy(tags)
            return
        
        for i in tags:
            # Check each element of tagreturn [self.key, self.value]s is actually a Tag
            assert type(i) == Tag
        self.value = tags
    
    def append(self, tags):
        #Appends all tags present in normal array tags
        assert type(tags) == list or type(tags) == TagArray
        
        if type(tags) == list:
            for i in tags:
                assert type(i) == Tag
            self.value += tags
        else:
            self.value += tags



class Tag:

    EVENT_KEY = 'e'
    REFER_TO_ANOTHER_USER_KEY = 'p'
    REPLACEABLE_EVENT = 'a'
    
    def __init__(self, key, value = "", misc = []):
        self.key = key
        self.value = value
        self.misc = misc
        assert self.key != ""
    
    def toArray(self):
        return [self.key, self.value] + self.misc