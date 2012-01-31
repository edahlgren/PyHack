import re, inspect
import operator as op

"""
A rocking module to parse basic arithmatic (binary) operations 
  string syntax : Lisp 
  method : Recursive descent

Erin Dahlgren :: January 15 2012

"""



class Parser:
    def __init__(self, streamf, recursef):
        self.stream = streamf
        self.descent = recursef

    def run(self, stringy):
        if space(stringy): return self.descent(stringy)
        else: return int(stringy)


def splitstream(stream):
    """
    Splits a string 'stream' into isolated computation parts
    [String] -> ["(", "binary", "expression", "expression", ")"]
    
    """
    (l,r,sp,ls) = (0,0,0,len(stream))
    for x in range(2, ls-1):
        if l != 0 and l == r:
            return ["(", stream[1:2], stream[3:x], stream[x+1:ls-1], ")"]
        if stream[x] == " ":
            sp = x
        if stream[x] == "(":
            l += 1
        if stream[x] == ")":
            r += 1
    if l == 0 and l == r:
        return ["(", stream[1:2], stream[3:sp], stream[sp+1:ls-1], ")"]


def uncurry(f):
    """
    f((1,2)) -> f(1,2)
    
    """
    return lambda x: f(*x)


def singlearg(f,x,valargs):
    """
    If decorator has a single argument
      a. decorator argument is a reg ex -> is decorator-argument in x?
      b. decorator argument is a function -> f(decorator-argument(x))
      replaces x with a. or b.

    """
    F = inspect.isfunction(valargs[0])
    if F:
        y = valargs[0](x)
        return f(y)
    elif re.search(valargs[0], x): 
        return f(x)


def mulargs(f,fargs,valargs):
    """
    If decorator has multiple arguments
      a. decorator argument is a reg ex -> is decorator-argument in x?
      b. decorator argument is a function -> f(decorator-argument(x))
      replaces each 'fargs' with a or b -> f(a or b, a or b, ...)

    """
    global switchargs
    for i in range(0, len(valargs)):
        F = inspect.isfunction(valargs[i])
        if F:
            y = valargs[i](fargs[i])
            switchargs.append(y)
        else: 
            if re.search(valargs[i], fargs[i]): 
                swichargs.append(fargs[i])
            else: switchargs.append(None)
    tswitchargs = tuple(switchargs)
    return uncurry(f)(tswitchargs)


def validate(*valargs):
    """
    Decorator: 
    performs singlearg or mulargs depending on num decorator args

    """
    if len(valargs) == 1:
        def wrap(f):
            def wrapped_f(x):
                return singlearg(f,x,valargs)
            return wrapped_f
        return wrap
    else:
        def wrap(f):
            def wrapped_f(*fargs):
                return mulargs(f,fargs,valargs)
            return wrapped_f
        return wrap


@validate(r"(^[1-9][0-9]*)|^0")
def checkint(string):
    if string is not None:
        return True

@validate(r"\ ")
def space(string):
    return True

@validate(r"\+")
def plus(string):
    return op.add

@validate(r"\-")
def minus(string):
    return op.sub

@validate(r"\*")
def mul(string):
    return op.mul

@validate(plus, minus, mul)
def operation(op1, op2, op3):
    return op1 or op2 or op3


def getop(string):
    """
    Selects matching binary by recursing through the decorator applications above
      Args : string is "binary" to be matched
      Returns : composable binary operator

    """
    global switchargs 
    switchargs = []
    return operation(string, string, string)


def f(string):
    """
    Recurses through stream by breaking up each expression if it is not an int
    Applies operators to their leaf integer arguments
      Args : string to parse
      Returns : computed single integer

    """
    y = splitstream(string)
    e1 = checkint(y[2])
    e2 = checkint(y[3])
    op = getop(y[1])
    if e1 == e2:
        if e1: return op(int(y[2]), int(y[3]))
        else: return op(f(y[2]), f(y[3]))
    else:
        if e1: return op(int(y[2]), f(y[3]))
        else: return op(f(y[2]), int(y[3]))





"""
Testing
"""
binaryParser = Parser(splitstream, f)
assert binaryParser.run("45") == 45
print binaryParser.run("45")
assert binaryParser.run("(+ 45 50)") == 95
print binaryParser.run("(+ 45 50)")
assert binaryParser.run("(+ (- 8 3) 50)") == 55
print binaryParser.run("(+ (- 8 3) 50)")
assert binaryParser.run("(+ (- 8 3) (+ (- 7 33) 24))") == 3
print binaryParser.run("(+ (- 8 3) (+ (- 7 33) 24))")
assert binaryParser.run("(* 3 6)") == 18
print binaryParser.run("(* 3 6)")
print 'Baaaaam :)'

