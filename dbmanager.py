#!/usr/bin/python3

#data io manager

import csv
import sys

import config

sys_root = config.sys_root
sys_project = config.sys_project
sys.path.append(sys_root+sys_project)
import mydataset as my
import os
import shutil

#DANGEROUS! DO NOT CHANGE UNLESS ABSOLUTE NECESSITY :
##this module is allow to delete data, thus, could lead to side destruction as well
sys_mem = config.sys_mem
MEM = sys_root+sys_mem

lt = False

def local_test(test = False):
    if test :
        read = my.Tree()
        io = IO()
        #20210923: need to add stand alone dummy test files
        io.ReadTree(read,"20190426_Le_bon_coin_Selected.csv")

        io.WriteCsv(read,MEM+"20190426_Le_bon_coin_Selected.csv")

        

class IO(object):
    def __init__(self,path = "",default_primary_key = "local_primary_key",mode = '//',list_separator = '|'):
        self.path = path
        self.mode = mode #define the path construction separator, ie, win or linux
        self.list_separator = list_separator
        self.default_primary_key = default_primary_key
        self.mem_directory_path = MEM

    # os.listdir(path)
    def ReadTree(self,tree,tree_name,*args):
        concat_path_current_layer = ''
        if len(args) == 0:
            tree.Set(tree_name)
            concat_path_current_layer = tree_name+"/"
        else:
            args=args[0]
            for elem in args:
                concat_path_current_layer += elem+"/"

        if os.path.exists(self.mem_directory_path+concat_path_current_layer):
            current_layer_content = os.listdir(self.mem_directory_path+concat_path_current_layer)
            for elem in current_layer_content:
                if len(args) == 0:
                    next_layer = tuple([tree_name])+tuple([elem])
                    saved_layer = tuple([tree_name.replace("\\","/")])+tuple([elem.replace("\\","/")])
                    tree.SetN(saved_layer)
                    self.ReadTree(tree,tree_name,next_layer)
                else:
                    next_layer = args+tuple([elem])
                    saved_layer = args+tuple([elem.replace("\\","/")])
                    tree.SetN(saved_layer)
                    self.ReadTree(tree,tree_name,next_layer)

    ##20190619 : removed the erase of existing directory
    def WriteTree(self,tree,*args):
        concat_path_current_layer = ""
        if len(args) != 0:
            args = args[0]
            for elem in args:
                escaped = elem.replace("/","\\")
                concat_path_current_layer += escaped+"/"

        for layer in tree.Get(*args):
            if layer != "":
               escaped = layer
               escaped = escaped.replace("/","\\")
##               if os.path.exists(self.mem_directory_path+concat_path_current_layer+escaped):
##                   shutil.rmtree(self.mem_directory_path+concat_path_current_layer+escaped)
               if not os.path.exists(self.mem_directory_path+concat_path_current_layer+escaped):
                   os.mkdir(self.mem_directory_path+concat_path_current_layer+escaped)
               if len(args) == 0:
                   next_layer = tuple([layer])
                   self.WriteTree(tree,next_layer)
               else:
                   next_layer = args+tuple([layer])
                   self.WriteTree(tree,next_layer)
               
        
    def ReadCsv(self,file_name,file_path = '',primary_key = ''):
        local_path = file_path
        if file_path == '':
            #use local_definition
            local_path = self.path
        local_path+= file_name
        #attention : rt for read text and rb for read byte
        with open(local_path,'rt') as f:
            reader = csv.reader(f,delimiter=self.list_separator,quoting=csv.QUOTE_NONE)
            local_tree = my.Tree()
            if primary_key == '':
                local_primary_key = self.default_primary_key
            else:
                local_primary_key = primary_key
            head = next(reader)
            index_pk = 0 #then if no col matched, the first one is considered as a pk
            counter = 0
            pk = ""
            for col in head:
                if col == local_primary_key:
                    index_pk = counter
                    pk = str(col)
                counter+=1
                
            for row in reader:
                counter = 0      
                for col in row:
                    if counter < len(head) and index_pk < len(row):
                        ## File/pk/head/value
                        #local_tree.Set(file_name,row[index_pk],head[counter],col)
                        ## File/head/pk/value
                        local_tree.Set(file_name,head[counter],row[index_pk],col)
                        counter+=1
                    
            return local_tree
            
    def WriteCsv(self,tree,file_path = '',scan_pk_limitor = 10000):
        #we assume the file_name do not contains the file location
        for file_name in tree.Get():
            local_file = ''
            if file_path == '':
                local_file = self.path + str(file_name)
            else :
                local_file = file_path + str(file_name)
                
            with open(local_file,'wt') as f:
                
                former_stdout = sys.stdout #20181114
                sys.stdout = f #20181114
                #scan_pk_limitor = 10000 # use it instead of dummies. Tree could help with build-in method listing all elements of a given layer
                scan_pk = 0
                local_heads = my.Tree()
                for pk in tree.Get(file_name):
                    for head in tree.Get(file_name,pk):
                        local_heads.Set(head)
                    scan_pk+=1
                    if scan_pk_limitor > 0:
                        if scan_pk > scan_pk_limitor :
                            break
                header = ''
                init = False
                for head in local_heads.Get():
                    if init :
                        header += self.list_separator
                    header += str(head)
                    init = True

                
                header+= '\n'
                f.write(header)
                
                line = ''
                init = False
                
                for pk in tree.Get(file_name):
                    for head in local_heads.Get():
                        if len(tree.Get(file_name,pk,head)) > 0 :
                            #for value in tree.Get(file_name,pk,head):
                            #this is a 2D file, not nD
                            value = tree.Get0(file_name,pk,head)
                            if init :
                                line+= self.list_separator
                            line+= str(value)
                            init = True
                        else :
                            if init :
                                line+= self.list_separator
                            line+= '' #void as the head exist but no value attached here
                            init = True
                    line+= '\n'
                    f.write(line)
                    line = ''
                    init = False
                sys.stdout = former_stdout #20181114

local_test(lt)  
