
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


# # Generate the graph
#
# ## Step 1 : Iterate through the input files, discarding lines with fewer than 10 movies. Generate a actor to movies mapping, and a reverse movies to actor mapping
#
# The lines are cleaned by:
# - Removing unprintable characters
# - Removing stuff in brackets () or {}

# In[ ]:

A = {}
M = {}

lc = {"data/actress_movies.txt" : 1182813, "data/actor_movies.txt" : 2167653}

printable = set(string.printable)

def clean_string(s):
    return(re.sub(r'\(.*\)|\{.*\}|\'|\"', "", s).lstrip().rstrip())

for fname in ["data/actor_movies.txt", "data/actress_movies.txt"]:
    with open(fname, "r") as f:
        for line in timer(f, total = lc[fname], desc=fname.split("/")[1]):
            if line.count('\t\t') < 10:
                pass
            else:
                line = filter(lambda x : x in printable, line.decode('latin1')).encode('ascii')
                splits = line.split("\t\t")
                actor_name = splits[0]
                movies =  set(map(clean_string, splits[1:]))

                if actor_name in A:
                    A[actor_name] = A[actor_name].union(movies)
                else:
                    A[actor_name] = movies

                for movie in movies:
                    if movie not in M:
                        M[movie] = [actor_name]
                    else:
                        M[movie].append(actor_name)


# # Next find movies with less than 10 actors and drop these movies. This could easily be a cyclic process, so we STOP here!

# In[ ]:

for (m, alist) in M.iteritems():
    if len(alist) <= 10 or m == '':
        for actor in alist:
            A[actor].remove(m)

M = {m : alist for (m, alist) in M.iteritems() if len(alist) >= 10}
A = {actor : movies for (actor, movies) in A.iteritems() if len(movies) > 10}


# ## Number of Actors

# In[ ]:

len(A.keys())


# ## Number of Movies

# In[ ]:

len(M.keys())


# ## Step 2: Generate an edgelist from the actor data

# In[ ]:

with open('elist.txt', 'w') as f:
    for a in timer(sorted(A.keys()), desc="Edgelist"):
        edges = set()

        for movie in A[a]:
            for b in M[movie]:
                edges.add(b)

        f.write(''.join(map(lambda x : '\t'.join((str(a), str(x), '\n')), sorted(edges))))


# ## Step 3: Read graph from file
