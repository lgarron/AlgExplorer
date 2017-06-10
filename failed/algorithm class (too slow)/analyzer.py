import sys
import os
import ast
import math
from algorithm import Algorithm

class Analyzer:
    # construct chain from collection
    @classmethod
    def fromcollection(cls, n, collection):
        self = cls()
        self.n = n
        self.pr = {}
        if os.path.isfile(collection):
            f = open(collection, "r")
            l = f.readlines()
        else:
            sys.stdout.write("Error: " + collection + " does not exist.\n")
            return
        for line in l:
            self.count(Algorithm(line.split("\t\t")[1]))
        self.normalize()
        return self

    # update counts (order n) with Algorithm alg
    def count(self, alg):
        m = alg.getmoves()
        for i in range(self.n, len(m)):
            j = self.key(m[i-self.n:i])
            k = self.key(m[i:i+1])
            self.pr.setdefault(j, {})
            self.pr[j].setdefault(k, 0)
            self.pr[j][k] += 1

    # transform counts into transition probabilities
    def normalize(self):
        for j in self.pr:
            total = float(sum([self.pr[j][k] for k in self.pr[j]]))
            for k in self.pr[j]:
                self.pr[j][k] /= total
        
    # construct chain from stored data
    @classmethod
    def fromsaved(cls, stored):
        self = cls()
        f = open(stored, "r")
        self.n = ast.literal_eval(f.readline().strip())
        self.pr = ast.literal_eval(f.readline().strip())
        return self

    # store chain in fname
    def save(self, fname):
        g = open(fname, "w")
        g.write(str(self.n) + "\n" + str(self.pr) + "\n")
        g.close()
    
    # convert move sequence to key
    def key(self, seq):
        r = 3 * len(Algorithm.movetypes)
        return sum([seq[i]*r**i for i in range(len(seq))])
    
    # evaluate movelist m
    def analyze(self, m):
        result = 0
        zero = 1e-10
        for i in range(self.n, len(m)):
            j = self.key(m[i-self.n:i])
            k = self.key(m[i:i+1])
            if j in self.pr and k in self.pr[j]:
                result += math.log(self.pr[j][k]) # log-likelihood
            else:
                result += math.log(zero)            
        return result / len(m) # normalize by alg length
