"""This module is the main AOPy module that will allow
the use of aspects in Python in AspectJ style.

"""
__author__ =  'Spencer Herzberg, Yuji Fujiki'
__version__=  '1.0'

def p(*args, **kwargs):
    """Use as a placeholder function/method for AOPWrapper"""
    pass

class InvalidParameters(Exception):
    """Error to raise when the parameters are incorrect for a method."""
    pass


class AOPWrapper:
    """Base class for an AspectJ style aspect"""
    
    def __init__(self,signature, numargs, kwargs):
        """Default constructor
        
        Arguments:
        signature --  string of the method/function to advise
        numargs -- string to represent the number of possible argument for this advise
        kwargs -- list of possible keyword arguments, possible values: ["*"], ["4"], ["apple","banana"]
        """
        
        self.setBefore(p)
        self.setAfter(p)
        self.setAround(p)
        
        self.setPointcut(signature, numargs, kwargs)
    
    def hasAround(self):
        """Returns boolean for if this aspect has around advice set"""
        return self.advice_around != None
    
    def setBefore(self,fn):
        """Sets the before advice
        
        Arguments:
        fn -- function reference to set the before advice to
        """
        self.advice_before = fn
        
    def setAfter(self,fn):
        """Sets the after advice
        
        Arguments:
        fn -- function reference to set the after advice to
        """
        self.advice_after = fn
        
    def setAround(self,fn):
        """Sets the around advice
        
        Arguements:
        fn -- function reference to set the round advice to
        """
        self.advice_around = fn
        
    def before(self,*args,**kwargs):
        """Calls the before advice"""
        self.advice_before()
        
    def after(self,retval, exc):
        """Calls the after advice"""
        return self.advice_after(retval, exc)
    
    def around(self, target, method, *args, **kwargs):
        """Calls the around advice
        
        Arguments:
        target -- is the object that the method was called on, None if on called on function
        method -- is the string name of the method that was called
        args -- is the list of arguments that the method was called with
        kwargs -- is the list of keyword arguements that the method was called with
        
        Returns the returned value of the set around advice
        """
        
        ret = self.advice_around(target, method, *args, **kwargs)
        return ret
    

    def setPointcut(self,pointcutsig,numargs,kwargs):
        """Sets the pointcut for the aspect
        
        Arguments:
        pointcutsig -- string of the method name
        numargs -- string of the number of arguements allowed, * for any
        kwargs -- list of the allowed keyword arguments, can be ["*"], ["8"], ["apple","banana"]
        
        Raises InvalidParameters error if this method is passed the incorrect arguement types
        """
#        print self._parsePointcut(pointcutstring)
#        pc = self._parsePointcut(pointcutstring)
#        self.signature = pc[0]
#        self.args = pc[1]
#        self.kwargs = pc[2]
#        print type(pointcutsig) == type("")
#        print type(numargs) == type("") and (numargs.isdigit() or numargs=="*")
#        print type(kwargs)==type([]) and len(kwargs)>0
        if not (type(pointcutsig) == type("")
           and type(numargs) == type("") and (numargs.isdigit() or numargs=="*")
           and type(kwargs)==type([]) and len(kwargs)>0
           ):
            raise InvalidParameters()
        
        self.signature = pointcutsig
        self.args = str(numargs)
        self.kwargs = kwargs
        
        
    def isPointcut(self, signature, args, kwargs):
#        print "-"*40
        """Returns if the given signature is equal to the set pointcut"""
        
        sig = True if self.signature == "*" else self.signature == signature
#        print "sig", sig
        arg = True if self.args=="*" else self.args == str(len(args))
#        print "arg", arg
        
        if self.kwargs!=["*"]:
#            numargs=len(kwargs)
#            print type(kwargs),kwargs
            if (self.kwargs[0].isdigit()):
                #
                n = len(kwargs)
                if(n==int(self.kwargs[0])):
                    kwarg=True
                else:
                    kwarg=False
            else:
#                print "got here"
                self.kwargs.sort()
                kwargs.sort()
                
                if self.kwargs == kwargs:
                    kwarg=True
                else: kwarg=False
        else:
            kwarg = True
        
#        print "kwarg", kwarg
        return sig and arg and kwarg
    
#    def _parsePointcut(self,pointcut):
#        tmp = pointcut.split()
#        if len(tmp)==1:
#            return [tmp[0],"*",[]]
#        else:
#            return [tmp[0],tmp[1],tmp[2:]]
    
    
    


def weave(method, *args, **kwargs):
    """Decorator used to "weave" a method/function with the list of aspects"""
    global pclist
#    retval = method(*args, **kwargs)
    
    def invoke_advice(*args, **kwargs):
        found = False
        for pc in getPointcutter().getPointcutters():
            if pc.isPointcut(method.__name__, args, kwargs.keys()):
                found = True
                break
        if not found:
            return method(*args, **kwargs)
        
        print pc.before,pc.advice_before
        pc.before(*args,**kwargs)
        try:
            if not pc.hasAround():
                retval = method(*args, **kwargs)
            else:
                try:
                    retval = pc.around(method.im_self,method, *args, **kwargs)
                except:
                    retval = pc.around(None,method, *args, **kwargs)
        except Exception, e:
            pc.after(None, e)
            raise
        else:
            pc.after(retval, None)
            return retval
    # Replace the method with our weaved one.
    try:
        class_ = method.im_class
    except:
        # The method is actually a simple function, wrap it in its namespace;
        method.func_globals[method.func_name] = invoke_advice
    else:
        #name = method.__name__
        setattr(class_, method.__name__, invoke_advice)
    return invoke_advice


POINTCUTTER = None

def getPointcutter():
    """Used as the singleton getter"""
    global POINTCUTTER
    if POINTCUTTER==None:
        POINTCUTTER=Pointcutter()
    return POINTCUTTER

class Pointcutter(object):
    """Singleton object used to store aspects"""
    _instance = None
    def __init__(self):
        self.pclist = []
    
    def addPointcuter(self,pointcutter):
        print "added pointcutter"
        self.pclist.append(pointcutter)

    def getPointcutters(self):
        return self.pclist








    

    
