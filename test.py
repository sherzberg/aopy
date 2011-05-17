
from aopy.core import weave,getPointcutter,AOPWrapper


class Logger(AOPWrapper):
    
    def __init__(self,signature, numargs, kwargs):
        AOPWrapper.__init__(self,signature, numargs, kwargs)
        self.setBefore(self.before)
        self.setAfter(self.after)
        self.setAround(self.around)
        
    def before(self, *args, **kwargs):
        print "before call"
        
    def after(self, retval, exc):
        print "after call"
        
    def around(self,target, method, *args, **kwargs):
        print "before around:",target,method, args, kwargs
        ret = method(*args,**kwargs)
        print "after around: ",ret
        return ret


@weave
def run():
    print "I'm running"       


def main():
    
    #setup logger aspect for all methods named run
    #with no args and any kwargs
    logger = Logger("run","0", ["*"])

    #setup pointcutter singleton
    pc = getPointcutter()
    
    #add the logger aspect
    pc.addPointcuter(logger)
    
    run()
    
    #runtime reset of logger aspect to a new pointcut
    #the next run call to run() will not be advised
    logger.setPointcut("notrun","0", ["*"])
    run()
    
main()
