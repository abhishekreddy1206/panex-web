#
# Copyright (c) 2013 by Mohit Singh kanwal.  All Rights Reserved.
#
import subprocess


class ProcessManager(object):
    """ProcessManager Utility Class: Its singleton"""

    INSTANCE = None

    __PROCESS_DICT = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")

    @classmethod
    def get_instance(cls):
    	if cls.INSTANCE is None:
    		cls.INSTANCE = ProcessManager()
    		cls.INSTANCE.__PROCESS_DICT = dict()
    	return cls.INSTANCE

    @classmethod
    def set_process(cls, key, value):

        if cls.__PROCESS_DICT is None:
            cls.__PROCESS_DICT = dict()
        cls.__PROCESS_DICT[key] = value

    @classmethod
    def get_process(cls, key):
        return cls.__PROCESS_DICT[key]

    @classmethod
    def get_process_dict(cls):
    	return cls.__PROCESS_DICT

#
# A small test suite
#
if __name__ == '__main__':
    s1 = ProcessManager()
    s2 = ProcessManager()
    if(id(s1) == id(s2)):
        print "Same"
    else:
        print "Different"
