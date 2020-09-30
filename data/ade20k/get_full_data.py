from ADE_stat import ADE_STAT
import os 
from PIL import Image
import matplotlib.pyplot as plt 
import pandas as pd 
from copy import deepcopy
import numpy as np




# purpose of this code: there are two version of ADE20K dataset.
# The original one with higher resolution and it has semantic and instance mask. but there are 3148 class.
# the smaller one with lower resolution with 150 class and semantic anno but without instance anno
# This code will recreate annotation for higher resolution images with 150 semantic anno (same as smaller one)
# and in the meantime create instance mask.  
# it will create a output folder named full_data within three folders: images, annotations, annotations_instance 
# each one will have two folders: training and validation 
# what you need to have is: 
# 1: ADE_STAT class 
# 2: files folder (preprocessing results of index_ade20k.mat)
# 3: objectInfo150.txt from smaller version dataset 
# 4: images folder from original bigger version dataset


if os.path.exists('full_data'):
    raise IOError('output folder exists, if data is there you do not need run this code again') 

os.makedirs('full_data')

os.makedirs('full_data/images')
os.makedirs('full_data/images/training')
os.makedirs('full_data/images/validation')

os.makedirs('full_data/annotations')
os.makedirs('full_data/annotations/training')
os.makedirs('full_data/annotations/validation')

os.makedirs('full_data/annotations_instance')
os.makedirs('full_data/annotations_instance/training')
os.makedirs('full_data/annotations_instance/validation')





def process_mask(seg):
    """
    the func is adopted from offical matlab code
    seg should be a 2D np.array  with range 0-255 float type, NOT uint8!!!  
    it will return a class_mask(semantic mask), and instance mask 
    """ 
    R,G,B = seg[:,:,0], seg[:,:,1], seg[:,:,2]
    class_mask = R/10 * 256 + G
    
    _,instance_mask = np.unique(B, return_inverse=True)
    instance_mask = instance_mask.reshape(B.shape)
    
    return class_mask, instance_mask




def process_instance_mask(instance_mask):
    """
    Let's say before applying indicator, there are 100 instances, so instance_mask will have
    100 different numbers[0,1,...99]. After applying indicator, some instances, say 10,  will be zerod out,
    as these 10 instances do not belong to classes from anno150, and there are treated as unlabled.
    It is no harm just use that zeroed out instance mask, but I prefer to re-order these class, such that 
    the remaining 90 instances have numbering from 0 to 89  
    """
    _,new_instance_mask = np.unique(instance_mask, return_inverse=True)
    new_instance_mask = new_instance_mask.reshape(instance_mask.shape)
    
    return new_instance_mask






ade = ADE_STAT('files')

# read class name of annotation150
data = pd.read_csv('objectInfo150.txt', sep='\t', lineterminator='\n') # this file is from smaller datase
mapping = {}
for i in range(150):
    line = data.loc[i]
    key = line['Name'] 
    mapping[key] = None

# for names also existing in annotation3148 map them to class label from annotation3148 
ade = ADE_STAT('files')
all_class_names = ade.all_class_names
for key in mapping.keys():
    if key in all_class_names:
        class_label = ade.from_name(key)['label']
        mapping[key] = [class_label]

# there are two classes from annotation150 not found in annotation3148 
# 'door, double door' and this class is actually combine of 'door' and 'double door' from annotation3148 
# 'crt screen', and this class is actually 'screen, crt screen' in annitation3148 
# I got the above two results by manually checking
mapping['door, double door'] = [ ade.from_name('door')['label'] ] + [ ade.from_name('double door')['label'] ]
mapping['crt screen'] = [ ade.from_name('screen, crt screen')['label'] ] 





# read all image files
path = 'files'
filename = pd.read_csv(path+'/filename.txt', delim_whitespace=True, header=None)[0].tolist()
folder = pd.read_csv(path+'/folder.txt', delim_whitespace=True, header=None)[0].tolist()
typeset = pd.read_csv('files/typeset.txt', lineterminator='\n', header=None)[0].tolist() 
assert(  len(filename) == len(folder)  == len(typeset) )





# now create our own mask(with 150 class) for these bigger images
for i in range( len(filename) ):
    print(i)
    img_file = filename[i]
    seg_file = filename[i][:-4]+'_seg.png'
    img = Image.open(  os.path.join( folder[i][18:], img_file )  )
    seg = Image.open(  os.path.join( folder[i][18:], seg_file )  )
    class_mask, instance_mask = process_mask( np.array(seg).astype('float') )
    

    ################ below is core of this code ###############

    indicator = np.zeros_like(class_mask) # a mask, used later for unlabel regrion of instance mask  
    new_class_mask = np.zeros_like(class_mask) # we will work on this array, and this finally is semantic mask 
    old_class_mask = class_mask # rename, used for indicator calculation

    for j, key in enumerate(mapping):
        
        new_class_label = j+1  # for example the first class in anno150 is 'wall', and actually is label 1, label 0 is for unlabeled
        old_lables = mapping[key] # get old labels for this class     
        
        for old_lable in old_lables: # for some class there are multiple old class mapping to the same class in anno150
            indicator += (old_class_mask==old_lable) # change to 1 for region having class from anno150 
            new_class_mask += np.where(old_class_mask==old_lable, new_class_label, 0) # RHS: if it is old label, then change to new laebl, and remiang is 0. Add RHS to new_class_label

    instance_mask *= indicator.astype('uint8') # apply instance mask 
    instance_mask = process_instance_mask(instance_mask) # purpose see inside of this function 
    class_mask = new_class_mask # overwrite class_mask with new one 


    # below is just saving  
    temp = 'training/' if typeset[i] == 1 else 'validation/'

    name = img_file
    img.save(  'full_data/images/' + temp + name )

    name = img_file.replace('jpg', 'png')  
    Image.fromarray(class_mask.astype('uint8')).save(   'full_data/annotations/' + temp + name      )
    Image.fromarray(instance_mask.astype('uint8')).save(   'full_data/annotations_instance/' + temp + name      )

        
    