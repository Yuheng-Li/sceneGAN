import os 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np
from PIL import Image
from copy import deepcopy 
import time 
import shutil










def get_box(mask):
    """ 

    Input mask should be a 2D np.array.

    returned box will touch foreground object itself. For example:

       [0., 0., 0., 0., 0.],
       [0., 0., 1., 1., 1.],
       [0., 0., 1., 1., 1.],
       [0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0.].

    Then return box will be: x1=2, y1=1, x2=4, y2=2

    Note that if you need to calculate box size using box outputed from here, you need to add 1 in each dimension
    that is: size = (x2-x1+1)*(y2-y1+1)
    
    """ 
    y,x = np.where(mask == 1)
    x1,x2,y1,y2 = x.min(),x.max(),y.min(),y.max()

    return x1,y1,x2,y2




class Crop_instance_processor():
    def __init__(self):
        """       
        This class will crop each instance of specific classes 
        please make sure full_data is located in the same folder         
        """ 

        self.full_data_root = './'
           
        objectinfo_path = 'objectInfo.txt'
        data = pd.read_csv(objectinfo_path, sep='\t', lineterminator='\n') 
        self.mapping = {}
        for i in range(len(data)):
            line = data.loc[i]
            self.mapping[ line['Name']  ] = line['Idx']


    def load_data(self, temp):

        path_to_img_folder = os.path.join(self.full_data_root, 'full_data/images/', temp)
        path_to_sem_folder = os.path.join(self.full_data_root, 'full_data/annotations/', temp)
        path_to_ins_folder = os.path.join(self.full_data_root, 'full_data/annotations_instance/', temp)

        self.img_files = os.listdir( path_to_img_folder )
        self.sem_files = os.listdir( path_to_sem_folder )
        self.ins_files = os.listdir( path_to_ins_folder )

        self.img_files = [  os.path.join( path_to_img_folder, item) for item in self.img_files  ]
        self.sem_files = [  os.path.join( path_to_sem_folder, item) for item in self.sem_files  ]
        self.ins_files = [  os.path.join( path_to_ins_folder, item) for item in self.ins_files  ]

        self.img_files.sort()
        self.sem_files.sort()
        self.ins_files.sort()

        assert len(self.img_files) == len(self.sem_files) == len(self.ins_files) 

        
    
    def process(self, class_name, class_label, info_path):

             
        for i in range( len(self.img_files) ):  # check image one by one 
            print(i)
            img = Image.open(  self.img_files[i]   )
            sem = Image.open(  self.sem_files[i]   )
            ins = Image.open(  self.ins_files[i]   )
            
            sem_array = np.array(sem)
            ins_array = np.array(ins)

            wanted_class_mask = (sem_array==class_label)*1

            if wanted_class_mask.sum()==0:
                pass # no this class in this image and pass 
            else:

                for j in range( ins_array.max()+1  ):  # check instance one by one
                    
                    wanted_instance_mask =  wanted_class_mask * ( (ins_array==j)*1 )                  
                    
                    pixels = wanted_instance_mask.sum()
                    if pixels>16: # hardcode, each instance at least has 16 pixels, otherwise consider as noise
                        x1,y1,x2,y2 = get_box(wanted_instance_mask)
                        box_size = (x2-x1+1)*(y2-y1+1)

                        # for each cropped instance, store its source_image_global_idx, source_image_name, instance_index, box_size, box, pixels  
                        with open(  info_path, 'a' ) as f:
                            basename = os.path.split( self.img_files[i] )[-1][:-4]
                            line = str(i)+'  '+basename+'  '+str(j)+'  '+str(box_size)+'  '+str(x1)+'  '+str(y1)+'  '+str(x2)+'  '+str(y2)+'  '+str(pixels)+'\n' 
                            f.write(line)
                        
            
        
    
    
    def __call__(self, names):
        """
        names is a list which contain class names such as ['people', 'car' ....] (name must exist)
        for each name it will create a output folder with the same name as class name.
        Please make sure there is no same folder in current dirctor        
        """
        
        # first create output folders      
        training_infos = []
        validation_infos = []    
        for name in names:
            assert not os.path.exists(name)
            os.makedirs(name)

            training_info = name+'/training_info.txt'
            training_infos.append( training_info )
            with open( training_info, 'w+') as f:
                pass 

            validation_info = name+'/validation_info.txt'
            validation_infos.append( validation_info )
            with open( validation_info, 'w+') as f:
                pass 
            
                    
        # get class label for these wanted class 
        wanted_labels = [  self.mapping[name]   for name in names       ]


        # load training data 
        self.load_data('training')        
        # start processing training data
        for name, wanted_label, training_info in zip( names, wanted_labels, training_infos ):
            self.process( name, wanted_label, training_info )


        # load validation data 
        self.load_data('validation')        
        # start processing validation data
        for name, wanted_label, validation_info in zip( names, wanted_labels, validation_infos ):
            self.process( name, wanted_label, validation_info )
            
        
           
        
        

        


if __name__ == '__main__':
    cro = Crop_instance_processor()

    names = []
    names.append('face')
    cro( names )



        