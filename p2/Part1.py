
# coding: utf-8

# In[1]:

import networkx as nx
import pandas as pd
from tqdm import tqdm as pbar
import numpy as np
from itertools import islice
import string
from scipy.sparse import lil_matrix, csc_matrix
from itertools import combinations
from tqdm import tqdm as timer
from scipy.misc import comb
import re
from collections import defaultdict


# Download files from the link (contain 6 txt files). Merge actor_movies.txt
# and actress_movies.txt files into one file, and remove all actors/actresses
# with less than 5 (so actors who have acted in four or fewer number of movies)
# movies; Note that you will have to parse the data in these lists as accurately as
# possible to extract the entities consistently and create the network. So plan on
# spending some time in cleaning the data set.

# In[ ]:

class AutoIncrement():
    def __init__(self):
        self.count = -1
    
    def next(self):
        self.count += 1
        return self.count
    
    def __str__(self):
        return str(self.count)
    
class IntMap():
    def __init__(self):
        self.data = {}
        self.ai = AutoIncrement()
    
    def decode(self, s):
        if s in self.data:
            return(self.data[s])
        else:
            count = self.ai.next()
            self.data[s] = count
            self.data[count] = s
            return(count)
    
    def encode(self, i):
        if i in self.data:
            return self.data[i]
        else:
            raise KeyError("Cannot encode number " + str(i))
    
    def __str__(self):
        return "Integer Map with %s entries" % (str(self.ai))


# In[ ]:

mdict = IntMap()
adict = IntMap()
A = {}
M = {}


# In[ ]:

printable = set(string.printable)

def clean_string(s):
    return(re.sub(r'\(.*\)|\{.*\}|\'|\"', "", s).lstrip().rstrip())


# In[ ]:

lc = {"data/actress_movies.txt" : 1182813, "data/actor_movies.txt" : 2167653}


# In[ ]:

for fname in ["data/actor_movies.txt", "data/actress_movies.txt"]:
    print("Reading from file " + fname)
    
    with open(fname, "r") as f:
        for line in timer(f, total = lc[fname]):
            if line.count('\t\t') < 5:
                pass
            else:
                line = filter(lambda x : x in printable, line.decode('latin1')).encode('ascii')
                splits = line.split("\t\t")
                actor_name =  adict.decode(splits[0])
                movies =  set(map(lambda x : mdict.decode(clean_string(x)), splits[1:]))
                A[actor_name] = movies

                for movie in movies:
                    if movie not in M:
                        M[movie] = [actor_name]
                    else:
                        M[movie].append(actor_name)


# In[ ]:

num_actors = adict.ai.count + 1
print "Number of actors", str(num_actors)


# In[ ]:

num_movies = mdict.ai.count + 1
print "Number of movies", str(num_movies)


# In[ ]:

len(M.keys())


# In[ ]:

print("Writing to edgelist")
with open('elist.txt', 'w') as f:
    for a in timer(sorted(A.keys())):
        edges = set()
        
        for movie in A[a]:
            for b in M[movie]:
                edges.add(b)
        
        edges.remove(a)
        f.write(''.join(map(lambda x : ' '.join((str(a), str(x), '\n')), sorted(edges))))


# In[ ]:

print("Writing Mappings from integers to actor names")
with open('actors.txt', 'w') as f:
    for i in timer(range(1, num_actors)):
        f.write("%s\n" % adict.encode(i))


# In[ ]:

print("Writing Mappings from integers to movie names")
with open('movies.txt', 'w') as f:
    for i in timer(range(1, num_movies)):
        f.write("%s\n" % mdict.encode(i))

