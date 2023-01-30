#!/usr/bin/python3

#implementation of tree structure by inline hashing using nested dictionaries

import string
import collections

#object dedicated to test the object handling ability of Tree
class Apple(object):
    def __init__(self,name):
        self.name = name

    def echo(self):
        print(self.name)

    def __str__(self):
        return self.name

#inline treemap structure
## /a/b/c/
## /a/b/d/
class Tree(object):
    def __init__(self):
        #self.root = {}
        self.root = collections.OrderedDict()
        #self.symbolic = '/'
        self.symbolic = '|'

    def __test__(self):
        print("run : Tree")
        t = Tree()
        print("run : Set")
        t.Set()
        print("run : Get")
        t.Get()
        print("run : Remove")
        t.Remove()

    def local_join(self,*args):
        concat = self.symbolic
        for arg in args:
            concat+=str(arg)+self.symbolic
        return concat

    #Set0 support the insertion of array
    def SetN(self,*args):
        if len(args) > 0:
            if isinstance(args[0],tuple) or isinstance(args[0],list):
                concat = self.symbolic
                for arg in args[0]:
                    if not self.root.get(concat,0):
                        self.root[concat] = {}
                    local_dict = self.root[concat]
                    local_dict[arg] = bool(1)
                    self.root[concat] = local_dict
                    concat+= str(arg)+self.symbolic
                #define the last item of the branch
                if not self.root.get(concat,0):
                    self.root[concat] = {}
        
    def Set(self,*args):
        if len(args)== 0:
            return
        else:
            concat = self.symbolic
            for arg in args:
                if not self.root.get(concat,0):
                    self.root[concat] = {}
                local_dict = self.root[concat]
                local_dict[arg] = bool(1)
                self.root[concat] = local_dict
                concat+= str(arg)+self.symbolic
            #define the last item of the branch
            if not self.root.get(concat,0):
                self.root[concat] = {}
                
    def Get(self,*args):
        concat = self.local_join(*args)
        return self.root.get(concat,{})

    def Get0(self,*args):
        concat = self.local_join(*args)
        return str(list(self.root.get(concat,{}).keys())[0])

    def Remove(self,*args):
        if len(args) == 0:
            return
        else:
            concat = self.local_join(*args)
            self.root.pop(concat,None)
            concat = self.local_join(*args[:-1])
            self.root[concat].pop(args[-1],None)

    def Echo(self):
        for branch,leaves in self.root.items():
            for leave in leaves.items():
                print(branch,leave)

    def Contains(self,*args):
        concat = self.local_join(*args)
        try:
            str(list(self.root.get(concat,{}).keys())[0])
        except:
            pass
        else:
            return True
        return False

