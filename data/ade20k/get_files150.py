import os 
import pandas as pd 
from PIL import Image
from shutil import copyfile
import numpy as np

# For ade20k, there are two different versions (3148 classes with instance annotaion) 
# and (150 without instance annotaion). In 3148 we have a stat mat file index_ade20k.mat,
# we have processed it and store different files into the files folder. Then we have an 
# analyzer ADE_stat.py which provides us useful stat info via reading the files folder.
# Now in order to understand the 150 one, we also create a counterpart files folder, 
# we name files150, and this is the purpose of this code. Before this you need to make 
# sure you have run get_full_data.py to have a full_data folder and objectInfo150.txt
# originally from the smaller version 


if os.path.exists('files150'):
    raise IOError('output folder exists, if data is there you do not need run this code again') 
os.makedirs('files150')



PATH = 'full_data/images/'
img_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames ]
img_files.sort()

PATH = 'full_data/annotations/'
sem_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames ]
sem_files.sort()

PATH = 'full_data/annotations_instance/'
ins_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames ]
ins_files.sort()

assert( len(img_files)==len(sem_files)==len(ins_files)   )
N = len(img_files)
C = 150 
objectsPart = np.zeros((N,C)) # this is always 0 
objectsPresence = np.zeros((N,C))


# mapping will be used to form objectnames.txt and objectcounts.txt
data = pd.read_csv('objectInfo150.txt', sep='\t', lineterminator='\n') 
mapping = {}
for i in range(150):
    line = data.loc[i]
    temp = {    'name': line['Name'],  'count':0 }
    mapping[ line['Idx']  ] = temp



filename = []
folder = []
for i in range(20):
    print(i)
    
    # first get folder and file of this image and store them 
    folder.append( os.path.split( img_files[i] )[0] )
    filename.append( os.path.split( img_files[i] )[1] )
    
    # read sem ins 
    sem = np.array(Image.open( sem_files[i] ))
    ins = np.array(Image.open( ins_files[i] ))
    
    # check each instance by instance now
    for j in range(ins.max()):
        this_ins = (ins==j)*1
        this_ins_sem = this_ins*sem  # this should be 2 values: 0 and sem class. (could be 0 then just 1 value)
        unique_value = np.unique(this_ins_sem)
        if  (len(unique_value)>2):
            print('%sth instance of image %s has more than one semantic label, and was passed' % (j,img_files[i]))
        else:
            # get class lable of this instance  
            class_label = unique_value[-1]   
            
            if class_label !=0:
                # +1 to this class in total count
                mapping[class_label]['count'] +=1 

                # +1 to this class in this image (not consider non-labled, thus shfit by 1)
                objectsPresence[i, class_label-1] += 1 



# now save objectsPart.npy and objectsPresence.npy
np.save(  'files150/objectsPart.npy', objectsPart  )
np.save(  'files150/objectsPresence.npy', objectsPresence  )



# now write objectnames.txt, objectcounts.txt and proportionClassIsPart.txt
mapping_values = list(mapping.values())
for item in mapping_values:
    
    with open( 'files150/objectnames.txt', 'a' ) as f:
        line = item['name'] + '\n'
        f.write(line)
        
    with open( 'files150/objectcounts.txt', 'a' ) as f:
        line = str(item['count']) + '\n'
        f.write(line)
        
    with open( 'files150/proportionClassIsPart.txt', 'a' ) as f:
        line = '0\n' # always 0 
        f.write(line)


# write filename.txt and folder.txt
with open( 'files150/filename.txt', 'a' ) as f:
    for line in filename:
        line = line + '\n'
        f.write(line)
        
with open( 'files150/folder.txt', 'a' ) as f:
    for line in folder:
        line = line + '\n'
        f.write(line)


print('Everything is done except for scene.txt and typeset.txt, please manually copy them')