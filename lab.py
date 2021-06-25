"""6.009 Lab 10: Snek Interpreter Part 2"""

import sys
sys.setrecursionlimit(5000)

#!/usr/bin/env python3
"""6.009 Lab 9: Snek Interpreter"""

import doctest
# NO ADDITIONAL IMPORTS!


###########################
# Snek-related Exceptions #
###########################

class SnekError(Exception):
    """
    A type of exception to be raised if there is an error with a Snek
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """
    pass


class SnekSyntaxError(SnekError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """
    pass


class SnekNameError(SnekError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """
    pass


class SnekEvaluationError(SnekError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SnekNameError.
    """
    pass


############################
# Tokenization and Parsing #
############################


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Snek
                      expression
    """
    
    result1 = source.split('\n')
    
    final_result = []
    
    
    for segment in result1:
        counter = 0 
        strings = segment.split()
        for string in strings: 
            if string == ';':
                counter = 1 
            
                continue 
            
            if ')' in string: 
                string = string.replace(')', ' ) ')
        
            if '(' in string: 
                string = string.replace('(', ' ( ')
                
            strings2 = string.split()
        
            if counter == 0: 
                
                for string in strings2:  
                    final_result.append(string)
                        
           
               
            
    return final_result


def check_walrus(result):
    if result[0] == ':=':
        if len(result) != 3: 
            raise SnekSyntaxError
                   
        #can be a string, a special function with string
        if type(result[1]) != str and type(result[1]) != list:
            raise SnekSyntaxError
            
        if type(result[1]) == list:
            if len(result[1]) == 0:
                raise SnekSyntaxError
                
            for i in result[1]:
                if type(i) != str:
                    raise SnekSyntaxError
                    
            
        
            
def check_function(result):
    if result[0] == 'function': 
        if len(result) != 3:
            raise SnekSyntaxError
            
        if type(result[1]) != list:
            raise SnekSyntaxError
         
        else: 
            for i in result[1]:
                if type(i) != str:
                    raise SnekSyntaxError   



def check_type(variable):
    """
    Checks the type of a variable, first a float, then an int,
    and finally the var if that does not raise an error
    """
    try: 
        return int(variable)
    except: 
        try: 
            return float(variable)
        except: 
            return variable

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    
    
    def parse_expression(index):
        """
        Helper function that uses tokens and an index to parse our tokens into
        a list
        """
        
        current = tokens[index]
    
        if current == ')':
        
            raise SnekSyntaxError
            
        
        if current != '(':
        
            return (check_type(current), index+1)
        
        else: 
            result = []
           
            index = index + 1
            
            if index >= len(tokens):
                raise SnekSyntaxError
                
            current = tokens[index]
            
            if current == ')':
            
                return (result, index+1)
            
            
            #if we start with left paren, end with right paren
            #make an empty list of current expression, continue calling parse expression until we get to right 
            while current != ')':
            #until we hit an end 
                #returns expression and index 
                
                val, index = parse_expression(index)
                
                result.append(val)
                
                
                if index >= len(tokens):
                    
                    raise SnekSyntaxError
                
                current = tokens[index]
                
                
                
            check_function(result)
                
            
            check_walrus(result)
            
                    
            
            return (result, index+1)

                
    result, index = parse_expression(0)
    if len(tokens) > index: 
        raise SnekSyntaxError
        
    
        
        
    return result
         

        #other terminating conditions: raise errors when not parsable             
                
######################
# Built-in Functions #
######################

def multiply(m_list):
    """
    Multiplies all of the numbers from a list
    """
    beg = 1
    for num in m_list: 
        beg = beg*num
        
    return beg


def divide(d_list):
    """
    Divides all of the numbers in a list
    """
    first = d_list[0]
    for num in d_list[1:]:
        first = first/num
        
    return first 


def cons(listt):
    """
    Returns Pair object from list_c, which has 2 elements
    """
    car = listt[0]
    cdr = listt[1]
    #makes the pair object and returns it 
    return Pair(car, cdr)

def car(cons_cell):
    """
    Takes a cons cell (instance of Pair class) and returns the first element 
    """
    if type(cons_cell[0]) == Pair: 
        return cons_cell[0].car
    
    else:  
        print('hi')
        raise SnekEvaluationError
        
def cdr(cons_cell):
    """
    Takes a cons cell (instance of Pair class) and returns the second element 
    """
    
    if type(cons_cell[0]) == Pair: 
        return cons_cell[0].cdr
    
    else:  
        raise SnekEvaluationError 
        
def length(lis):
    """
    Given an input list, returns its length 
    """
    
    try:  
        tracker = 0 
        val = lis[0]
        while val != None: 
            tracker += 1
            val = val.cdr
        return tracker 
    
    except:  
        raise SnekEvaluationError
        
def element_at_index(lis): 
    """
    Given an input list and a nonnegative index, returns the element
    at the given index in the given list. Indices start at index 0. 
    """
    #index is the second object
    try: 
        #if pair is a pair object
        if lis[1] != 0: 
            return element_at_index([lis[0].cdr, lis[1]-1])
        #recursively move onto next thing
        else: 
            return lis[0].car
        #just return the car if == 0 
    except:   
#    else: 
        raise SnekEvaluationError
        
        
def concat(lists): 
    """
    Takes in lists as arguments and returns a new list that concatenates them. 
    If one list passed in, return the copy of it. If no arguments, produce empty list. 
    Calling on elements that are not lists raises SnekEvaluationError
    """
    
    if lists == []: 
        return None 
    
    try: 
        if lists[0] != None: 
            
            rest_of_lis = [lists[0].cdr]+lists[1:]
            result = Pair(lists[0].car, concat(rest_of_lis))
            
            return result
        else: 
            return concat(lists[1:])
    except: 
        raise SnekEvaluationError
        
def mapping(inputs):
    """
    takes in a function and a list as arguments and returns a new list
    containing the results of applying the given function to each element
    of the given list. 
    """
    
    if not isinstance(inputs[1], Pair) and inputs[1] is not None:
        raise SnekEvaluationError
        
    if inputs[1] is None: 
        return None 
    
    if type(inputs[1]) == Pair: 
        car = inputs[0]([inputs[1].car])
        cdr = mapping([inputs[0], inputs[1].cdr])
    
    
    return Pair(car, cdr)
    
def filtered(inputs):
    """
    Takes in a function and a list as arguments, and returns a new list
    containing only the elements of the given list for which the given function returns true
    """

    if not isinstance(inputs[1], Pair) and inputs[1] is not None:
        raise SnekEvaluationError
        
    if inputs[1] is None: 
        return None 
    
    if type(inputs[1]) == Pair: 
        if not inputs[0]([inputs[1].car]):
            return filtered([inputs[0], inputs[1].cdr])
        else: 
            car = inputs[1].car
            cdr = filtered([inputs[0], inputs[1].cdr])
            
        
    result = Pair(car, cdr)
    return result 

def reduce(inputs): 
    """
    Takes in a function, a list, and an initial value as inputs. It produces
    its output by successively applying the fiven function to the elements in the 
    list, maintaining an intermediate result along the way. 
    """
    
    if not isinstance(inputs[1], Pair) and inputs[1] is not None:
        raise SnekEvaluationError
        
    if not inputs[1]: 
        return inputs[2]
    
    if not inputs[1].cdr: 
        return inputs[0]([inputs[2], inputs[1].car])
    
    else: 
        return reduce([inputs[0], inputs[1].cdr, inputs[0]([inputs[2], inputs[1].car])])

def listt(lis): 
    """
    Given a list, returns a Pair object
    """
    if len(lis) > 1: 
        return Pair(lis[0], listt(lis[1:]))
        
    if lis == []: 
        return None
    
    if len(lis) == 1: 
        return Pair(lis[0], None)
        

def begin(listt): 
    """
    Yields the last value in a list
    
    """
    return listt[-1]


def delete(var, environment = None): 
    """
    Used to delete variable bindings within the current environment. Takes one input, the variable
    name. If the variable is bound in the environment, binding should be removes and val returned. Else, 
    raise a SnekNameError
    """
    print(var)
    if environment is None: 
        environment = Environments(parent = Snek)
        
    if var in environment.variables: 
        result = environment.variables[var]
        del(environment.variables[var])
        return result 
    else: 
        raise SnekNameError 
        

def let(inputs, vals, body, tree, environment = None): 
    """
    Used to create local variable definitions. Evaluates all the given values in the environment, 
    creates a new environment whose parent is the current environment, and binds each name to its associated value 
    in this new environment
    """
    
    
    result = []
    
    if environment is None: 
        environment = Environments(parent = Snek)
        
    for element in tree[1]: 
        inputs.append(element[0])
        vals.append(element[1]) 
        
    for val in vals: 
        result.append(evaluate(val, environment))
    
    return Functions(inputs, body, environment)(result)
        

def setbang(var, exp, tree, environment = None):
    """
    Changes the value of an existing variable. Takes in var, a variable name, and expr, and expression. Evaluates the given expression
    in the current environment, finds the nearest enclosing environment in which Var is defined, and updates that binding in that environment to be
    the result of evaluating expr. If var not defined in any environments, raise a SnekNameError
    """
    
    if environment is None: 
        environment = Environments(parent = Snek)
        
    while var not in environment.variables and environment.parent:
        
            environment = environment.parent
    
    if var not in environment.variables:
        
        raise SnekNameError
        
    environment[var] = exp
    
    return exp
    

snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': multiply, '/': divide,
    '=?': lambda args: args.count(args[0]) == len(args), 
    '>': lambda args: all(args[i] > args[i+1] for i in range(len(args)-1)), 
    '>=': lambda args: all(args[i] >= args[i+1] for i in range(len(args)-1)),
    '<': lambda args: all(args[i] < args[i+1] for i in range(len(args)-1)), 
    '<=': lambda args: all(args[i] <= args[i+1] for i in range(len(args)-1)), 
    'not': lambda args: not args[0], 
    '#t': True, 
    '#f': False, 
    'cons': cons, 
    'car': car, 
    'cdr': cdr, 
    'nil': None, 
    'length': length, 
    'elt-at-index': element_at_index, 
    'concat': concat, 
    'filter': filtered, 
    'map': mapping, 
    'reduce': reduce,
    'list': listt,
    'begin': begin, 
    'del': delete, 
    'let': let, 
    'set': setbang
    
    
}


class Pair:
    """
    Represents each cons cell. Has two instance variables, car and cdr
    """
    
    def __init__(self, car, cdr):
        """
        Defines the variables car and cdr in the constructor
        """
        self.car = car
        self.cdr = cdr 

class Environments():
    """
    Environment cass - binds variable names to values, to a parent environment, 
    or places where other bindings are
    """
    
    def __init__(self, variables = None, parent = None):
        """
        Represents the built in vars and if in parent class
        """
        if variables == None: 
            self.variables = {}
            
        else:
            self.variables = variables
        
        self.parent = parent
        
        
    def __setitem__(self, key, value):
        """
        Sets the value of a variable
        """
        self.variables[key] = value
        
        
    def __getitem__(self, key):
        """
        Gets the value of a variable from a key
        """
        
        if key in self.variables.keys():
            return self.variables[key]
        
        if self.parent is None:
            raise SnekNameError
        
        else: 
            return self.parent[key]
        
        
Snek = Environments(None)
Snek.variables = snek_builtins 

class Functions: 
    """
    Class that defines functions and their values
    """    
    def __init__(self, parameters, expression, parent = Snek):
        """
        Functions have 3 things -- a parameter, an expression, and a parent(Snek)
        
        """
        self.parameters = parameters
        self.expression = expression
        self.parent = parent
        
    def __call__(self, parameter):
        """
        Handles function calls
        """
        env = Environments(parent = self.parent)
        
        if len(parameter) != len(self.parameters):
            raise SnekEvaluationError
            
        parameter_len = len(parameter)
        
        for index in range(parameter_len):
            
            env[self.parameters[index]] = parameter[index]
            
        return evaluate(self.expression, env)            
        
        

##############
# Evaluation #
##############


def evaluate(tree, environment = None):
    """
    Evaluate the given syntax tree according to the rules of the Snek
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if type(tree) == list and len(tree) == 0: 
        raise SnekEvaluationError 
    
    if environment is None: 
        environment = Environments(parent = Snek)
        
    types = (int, float)

    if type(tree) in types: 
        return tree 
    
    if type(tree) == str:
        if tree == '#f': 
            return False 
        if tree == '#t':
            return True 
        return environment[tree]
    

    if tree[0] == 'and': 
        for exp in tree[1:]: 
            if evaluate(exp, environment) == False: 
                return False
        return True 
    
    if tree[0] == 'del':
        return delete(tree[1], environment)
    
    if tree[0] == 'let': 
        return let([], [], tree[2], tree, environment)
    
    if tree[0] == 'set!':
        return setbang(tree[1], evaluate(tree[2], environment), tree, environment)

    if tree[0] == 'or': 
        for exp in tree[1:]:
            if evaluate(exp, environment) == True: 
                return True
        return False 
            
    else:
        
        if tree[0] == 'if': 
            if evaluate(tree[1], environment) == False: 
                return evaluate(tree[3], environment) 
            if evaluate(tree[1], environment) == True: 
                return evaluate(tree[2], environment)
            
        #set value
        if tree[0] == ':=':
            if type(tree[1]) != list: 
                var_name = tree[1]
                value = evaluate(tree[2], environment)
                environment[var_name] = value
                
                return value
            
            if type(tree[1]) == list: 
                function = Functions(tree[1][1:], tree[2], environment)
                if len(tree[1]) > 0: 
                    name = tree[1][0]
                    environment[name] = function
            
                return function
             
        
        if tree[0] == 'function':
            #return function instance
            return(Functions(tree[1], tree[2], environment))
            
        
        #account for nesting -- recursion
        func = evaluate(tree[0], environment)
        final_list = []
       
        for i in tree[1:]:
            final_list.append(evaluate(i, environment))
         
#        try: 
#            return func(final_list)
#        
#        except TypeError: 
#            #raise
#            #only time where you have eval error 
#            raise SnekEvaluationError
            
        if callable(func):
            return func(final_list)
        
        else: 
            raise SnekEvaluationError
        #checks if you can call something
        
        
def evaluate_file(string, environment = None): 
    """
    Function takes in a single argument, a string containing the 
    name of a file to be evaluated, and an optional argument, the environment
    in which to evaluate the expression, and return the result of evaluating the expression
    contained in the file
    """
    if environment is None: 
        environment = Environments(parent = Snek)
      
    val = open(string, 'r').read()
    val = parse(tokenize(val))
    return evaluate(val, environment)
            
    
            
def result_and_env(tree, environment = None):
    """
    Returns the result of an evalutation and the environment
    """
    if environment is None: 
        environment = Environments(parent = Snek)
        
    
    return(evaluate(tree, environment), environment)
        
    #implement a dunder call method




if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    
#    token_test1 = ['(', 'cat', '(', 'dog', '(', 'tomato', ')', ')', ')']
#    token_test2 = '(spam)'
#    print(tokenize(token_test2))
    
#    tokens = tokenize('(:= circle-area (function (r) (* 3.14 (* r r))))')
#    tokens1 = ["2", "3"]
#    #print(parse(tokens1))
#    
#    tokens2=["(","adam","adam","chris","duane",")",")"]
#    
#            
#    tokens3=[
#    "(",
#    "adam",
#    "adam",
#    "chris",
#    "duane",
#    ")",
#    ]
#    
#    print(parse(tokens2))
#    
#    print(parse(tokens3))
    #print(sys.argv)
    
    #make REPL
    env = Environments(parent = Snek)

    for file in sys.argv[1:]:
        with open(file) as f:
            token = tokenize(f.read())
            parse_f = parse(token)
            evaluate(parse_f, env) 
            
    
    while True:
        x = input('in>')
        #try: 
        if x == 'QUIT':
            break
        
        try: 
            token_x = tokenize(x)
            parse_x = parse(token_x)
            eval_x = evaluate(parse_x, env)
            print(eval_x)
            
        except SnekError: 
            
            #raise 
            print("error")
            
    
evaluate_file(test_inputs, environment = None)