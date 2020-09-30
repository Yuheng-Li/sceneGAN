import os 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np
from PIL import Image
from copy import deepcopy 



class ADELabel():
    def __init__(self, files_path):
                
        self.objectcounts = pd.read_csv( files_path+'/objectcounts.txt', delim_whitespace=True, header=None)[0].tolist()
        self.proportionClassIsPart = pd.read_csv(files_path+'/proportionClassIsPart.txt', delim_whitespace=True, header=None)[0].tolist()

        self.objectnames = []
        with open(files_path+'/objectnames.txt') as file:
            for line in file:
                self.objectnames.append(line[:-1]) # rm \n
        
        assert( len(self.objectcounts)==len(self.objectnames)==len(self.proportionClassIsPart)  )
                
        self.class_label = list( np.arange(len(self.objectnames)) + 1 ) 
        
        self.sort_accordining_count()
        
        
    def sort_accordining_count(self):
        
        objectcounts_least = deepcopy(self.objectcounts)
        objectnames_least = deepcopy(self.objectnames)
        proportionClassIsPart_least = deepcopy(self.proportionClassIsPart)
        class_label_least = deepcopy(self.class_label)
                
        self.objectcounts_least, self.objectnames_least, self.proportionClassIsPart_least, self.class_label_least = zip(*sorted(zip(objectcounts_least, objectnames_least, proportionClassIsPart_least, class_label_least)))

        self.objectcounts_most = deepcopy(self.objectcounts_least)[::-1]
        self.objectnames_most  = deepcopy(self.objectnames_least)[::-1]
        self.proportionClassIsPart_most = deepcopy(self.proportionClassIsPart_least)[::-1]
        self.class_label_most = deepcopy(self.class_label_least)[::-1]

                
        
    def from_name(self, name):
        "given name of class, it return class label, counts and proportion"
        
        idx = self.objectnames.index(name)
        label, count, prop = self.class_label[idx], self.objectcounts[idx], self.proportionClassIsPart[idx]
        
        return {'label': label, 'count':count, 'proportion':prop}
    

            
    def from_label(self, label):
        "given class label, it return class label counts and proportion"
        
        idx = self.class_label.index(label)
        name, count, prop = self.objectnames[idx], self.objectcounts[idx], self.proportionClassIsPart[idx]
        
        return {'name': name, 'count':count, 'proportion':prop} 
    
    
    def index_the_most(self,idx):
        "if give 0 then it give label, name count and proportion of the most frequent class"
        label = self.class_label_most[idx]
        name = self.objectnames_most[idx]
        count = self.objectcounts_most[idx]
        prop = self.proportionClassIsPart_most[idx]
        return {'label': label, 'name': name, 'count':count, 'proportion':prop} 
    

    def index_the_least(self,idx):
        "if give 0 then it give label, name count and prop of the least frequent class"
        label = self.class_label_least[idx]
        name = self.objectnames_least[idx]
        count = self.objectcounts_least[idx]
        prop = self.proportionClassIsPart_least[idx]
        return {'label': label, 'name': name, 'count':count, 'proportion':prop} 
        
        
        
                


class ADE_STAT():
    def __init__(self, files_path):
        """
        This is a class which can help you understand statistics of ADE dataset, the input path 
        to a folder where it contains the following files: 
        objectsPresence.npy
        scene.txt
        objectcounts.txt
        proportionClassIsPart.txt
        objectnames.txt
   
        
        It has two functions which give your idea about each scene 
        self.this_scene_obj_stat
        self.this_scene_image
        
        Four fucntions which give your idea about each objecl class 
        self.from_name
        self.from_label
        self.index_the_most
        self.index_the_least     
        
        NOTE: the stat is about the entire dataset(train and test). 
        """
        
        
        self.adelabel = ADELabel(files_path)                  
        
        objectsPresence = np.load( files_path+'/objectsPresence.npy')
        scenes = []
        with open('files/scene.txt') as file:
            for line in file:
                scenes.append(line[:-1])

        obj_number = objectsPresence.shape[1]
        
        # get object count and image count for each scene 
        self.each_scene_object_count = {}
        self.each_scene_image_count = {}

        for i, scene in enumerate(scenes):
            if scene not in self.each_scene_object_count:              
                self.each_scene_object_count[scene] = np.zeros(obj_number)   # first time then init it with all zeros 
            self.each_scene_object_count[scene] += objectsPresence[i]
            
            if scene not in self.each_scene_image_count:
                self.each_scene_image_count[scene] = 0 
            self.each_scene_image_count[scene] += 1 


        self.each_scene_image_count_sorted = sorted(self.each_scene_image_count.items(), key=lambda x: x[1], reverse=True)
            
        self.all_scene_names = list(self.each_scene_object_count.keys())
        self.all_class_names = self.adelabel.objectnames
        
        
    def this_scene_obj_stat(self, scene_name, sort=False):
        """
        Given scene name(str), it return each object counts in each scene
        if sort then obj is ordered in descending manner 
        """
        
        obj_count = self.each_scene_object_count[scene_name].tolist()
        obj_name = deepcopy(self.all_class_names) 
        
        if sort:
            obj_count, obj_name =  zip(*sorted(zip( obj_count, obj_name  ))) 
            obj_count = obj_count[::-1] 
            obj_name = obj_name[::-1]
        
        return dict(zip(obj_name, obj_count)) 
    
        
    def this_scene_image(self, scene_name):
        """
        Given scene name(str), it return number of images in this scene
        """
        return self.each_scene_image_count[scene_name]

    
    def from_name(self, name):    
        return self.adelabel.from_name(name)
               
    def from_label(self, label):
        return self.adelabel.from_label(label)  
   
    def index_the_most_obj(self,idx):
        return self.adelabel.index_the_most(idx)
    
    def index_the_least_obj(self,idx):
        return self.adelabel.index_the_least(idx)
        
        
        
                