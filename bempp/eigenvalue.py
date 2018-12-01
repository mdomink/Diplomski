import bempp.api
import scipy.sparse.linalg as spla
import numpy as np
import datetime

class Timer(object):
    """A simple timer class"""
    
    def __init__(self):
        pass
    
    def start(self):
        """Starts the timer"""
        self.start = datetime.datetime.now()
        return self.start
    
    def stop(self, message="Total: "):
        """Stops the timer.  Returns the time elapsed"""
        self.stop = datetime.datetime.now()
        return message + str(self.stop - self.start)
    
    def now(self, message="Now: "):
        """Returns the current time with a message"""
        return message + ": " + str(datetime.datetime.now())
    
    def elapsed(self, message="Elapsed: "):
        """Time elapsed since start was called"""
        return message + str(datetime.datetime.now() - self.start)
    
    def split(self, message="Split started at: "):
        """Start a split timer"""
        self.split_start = datetime.datetime.now()
        return message + str(self.split_start)
    
    def unsplit(self, message="Unsplit: "):
        """Stops a split. Returns the time elapsed since split was called"""
        return message + str(datetime.datetime.now() - self.split_start)

k=5

def fun(x, n, domain_index, result):    
    result[0] =1j * k * np.exp(1j * k * x[0]) * (n[0]-1)

def smallest_eigenvalue(operator, iteration = False):
    '''Takes matrix and returns its smallest eigenvalue '''
    print("smallest1")
    
    #discrete_operator=bempp.api.as_matrix(operator.weak_form())
    #discrete_operator=operator.weak_form()
    discrete_operator=operator
    print("smallest2")
    #discrete_operator=operator
    random_vector = np.random.rand(3,1)
    #random_vector = grid_fun.projections(operator.dual_to_range)
    difference = 1;
    norm_vector = 1;
    
    random_vector = random_vector/np.linalg.norm(random_vector) 
    #error 
    e = 0.0001;                    
    c = []
    koraci = [500]
    i = 0
    
    if(iteration):
        koraci = [10, 13, 15, 17, 20, 25, 30, 40, 50, 60, 70, 80, 100, 120 ,150]
    print("smallest3")    
    while difference >= e:
        i += 1
        #x = np.linalg.solve(matrix, random_vector)
        x, info = spla.gmres(discrete_operator, random_vector)
        norm_vector = np.linalg.norm(x)

        if(norm_vector != 0):
            x = x/norm_vector
        else:
            return 0;

        difference = np.linalg.norm(np.abs(random_vector)-np.abs(x))
        #print(difference)
        random_vector = x
        old = x

    c.append(1/norm_vector)
    return c, i

def smallest_eigenvalue_inverse(operator, iteration = False):
    '''Takes matrix and returns its smallest eigenvalue '''
    #print(matrix)
    
    discrete_operator=np.linalg.inv(bempp.api.as_matrix(operator.weak_form()))
    #discrete_operator=operator
    random_vector = np.random.rand(discrete_operator.shape[1],1)
    difference = 1;
    norm_vector = 1;
    res = 1;
    
    random_vector = random_vector/np.linalg.norm(random_vector)
    #error 
    e = 0.0001;                  
    c = []
    koraci = [500]
    i = 0
    
    if(iteration):
        koraci = [10, 13, 15, 17, 20, 25, 30, 40, 50, 60, 70, 80, 100, 120 ,150]
        
    while difference >= e:
        i += 1
        #x = np.linalg.solve(matrix, random_vector)
        x = discrete_operator.dot(random_vector)
        norm_vector = np.linalg.norm(x)
        x /= norm_vector

        difference = np.linalg.norm(np.abs(random_vector)-np.abs(x)) 
        random_vector = x 

    c.append(1/norm_vector)
    return c, i
