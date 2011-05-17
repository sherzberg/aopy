"""This module contains a few default aspects"""

__author__ =  'Spencer Herzberg, Yuji Fujiki'
__version__=  '1.0'

from core import AOPWrapper
import os


class Logger(AOPWrapper):
    
    def __init__(self,signature, numargs, kwargs):
        AOPWrapper.__init__(self,signature, numargs, kwargs)
        self.setBefore(self.before)
        self.setAfter(self.after)
        self.setAround(self.around)
        
    def before(self,*args,**kwargs):
        print "\tbefore method",self.signature
        
    def after(self, retval, exc):
        print "\tafter method",self.signature
        
    def around(self,target, method, *args, **kwargs):
        print "\tbefore around %s:" %self.signature,target,method, args, kwargs
        ret = method(*args,**kwargs)
        print "\tafter around %s:" %self.signature,ret
        return ret


class Writer(AOPWrapper):
    """Writer aspect used to dynamically change the buffer size for a file read operation depending on the ram usage"""
    
    def intercept(self, target, method, *args, **kwargs):
        print "intercepting"
        """Around adivice to change the read buffer size"""
        total = int(os.popen('free').read().split()[16])/1024
        used = int(os.popen('free').read().split()[15])/1024
        percent = used/total
        free = total-used
        chunk = free/10
        print chunk
        retval = method(*(args[0],args[1]),**{"chunksize":chunk})
        return retval
        
    def __init__(self,signature, numargs, kwargs):
        """Constructor
        
        Arguments:
        signature --  string of the method/function to advise
        numargs -- string to represent the number of possible argument for this advise
        kwargs -- list of possible keyword arguments, possible values: ["*"], ["4"], ["apple","banana"]
        """
        AOPWrapper.__init__(self,signature, numargs, kwargs)
        self.setAround(self.intercept)

