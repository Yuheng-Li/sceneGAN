import json
import matplotlib.pyplot as plt 
import numpy as np
import os 
from shutil import copyfile
from PIL import Image




label_info = [
['unlabeled'            ,  0 ,       'void'                   , False  ],      
['ego_vehicle'          ,  1 ,       'void'                   , False  ],     
['rectification_border' ,  2 ,       'void'                   , False  ], 
['out_of_roi'           ,  3 ,       'void'                   , False  ],    
['static'               ,  4 ,       'void'                   , False  ],   
['dynamic'              ,  5 ,       'void'                   , False  ],  
['ground'               ,  6 ,       'void'                   , False  ],  
['road'                 ,  7 ,       'flat'                   , False  ],   
['sidewalk'             ,  8 ,       'flat'                   , False  ], 
['parking'              ,  9 ,       'flat'                   , False  ], 
['rail_track'           , 10 ,       'flat'                   , False  ],
['building'             , 11 ,       'construction'           , False  ],
['wall'                 , 12 ,       'construction'           , False  ],
['fence'                , 13 ,       'construction'           , False  ],
['guard_rail'           , 14 ,       'construction'           , False  ], 
['bridge'               , 15 ,       'construction'           , False  ],
['tunnel'               , 16 ,       'construction'           , False  ],
['pole'                 , 17 ,       'object'                 , False  ],
['polegroup'            , 18 ,       'object'                 , False  ],
['traffic_light'        , 19 ,       'object'                 , False  ],
['traffic_sign'         , 20 ,       'object'                 , False  ],
['vegetation'           , 21 ,       'nature'                 , False  ],
['terrain'              , 22 ,       'nature'                 , False  ],
['sky'                  , 23 ,       'sky'                    , False  ],
['person'               , 24 ,       'human'                  , True   ],
['rider'                , 25 ,       'human'                  , True   ],
['car'                  , 26 ,       'vehicle'                , True   ],
['truck'                , 27 ,       'vehicle'                , True   ],
['bus'                  , 28 ,       'vehicle'                , True   ],
['caravan'              , 29 ,       'vehicle'                , True   ],
['trailer'              , 30 ,       'vehicle'                , True   ],
['train'                , 31 ,       'vehicle'                , True   ],
['motorcycle'           , 32 ,       'vehicle'                , True   ],
['bicycle'              , 33 ,       'vehicle'                , True   ],
]


def get_files(split, file_type):
    """
    split: train or val 
    file_type: img, sem or ins
    
    I have checked that all sem lables are falling into label_info annotation 
    
    """
    
    directory = 'leftImg8bit/'+split if file_type=='img' else 'gtFine/'+split

    if file_type=='img':
        keywords = '_leftImg8bit.png'
    elif file_type == 'sem':
        keywords = '_labelIds.png'
    else:
        keywords = '_instanceIds.png'
    

    filenames = []
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if basename.endswith(keywords):
                filename = os.path.join(root, basename)
                filenames.append(filename)
    filenames.sort()            
    return filenames



def create_objectinfo():
    "It will create an objectInfo.txt file used by SceneGAN"
    assert not os.path.exists('objectInfo.txt')
    file = open('objectInfo.txt', 'x')
    file.write('Name\t'+'Idx\n')
    for item in label_info:
        line = str(item[0])+'\t' + str(item[1])+'\n' 
        file.write(line)
    file.close()



def get_instance(x):
    _,instance_mask = np.unique(x, return_inverse=True)
    instance_mask = instance_mask.reshape(x.shape)
    return instance_mask


def make_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


assert not os.path.exists('full_data')
make_dir('full_data')
make_dir('full_data/images')
make_dir('full_data/images/training')
make_dir('full_data/images/validation')
make_dir('full_data/annotations')
make_dir('full_data/annotations/training')
make_dir('full_data/annotations/validation')
make_dir('full_data/annotations_instance')
make_dir('full_data/annotations_instance/training')
make_dir('full_data/annotations_instance/validation')

create_objectinfo()


##################################################################################################

img_files = get_files('train', 'img')
sem_files = get_files('train', 'sem') 
ins_files = get_files('train', 'ins') 
assert len(img_files) == len(sem_files) == len(ins_files) 
total = len(sem_files)


for i in range(total):
    print(i)    
    
    copyfile(  img_files[i],  'full_data/images/training/'+str(i).zfill(5)+'.png' )
    copyfile(  sem_files[i],  'full_data/annotations/training/'+str(i).zfill(5)+'.png' )
    
    ins = np.array(Image.open(ins_files[i]))
    ins = get_instance(ins)
    ins = Image.fromarray(ins.astype('uint8'))    
    ins.save( 'full_data/annotations_instance/training/'+str(i).zfill(5)+'.png'  )
    
    

#################################################################################################



img_files = get_files('val', 'img')
sem_files = get_files('val', 'sem') 
ins_files = get_files('val', 'ins') 
assert len(img_files) == len(sem_files) == len(ins_files) 
total = len(sem_files)

for i in range(total):
    print(i)    
    
    copyfile(  img_files[i],  'full_data/images/validation/'+str(i).zfill(5)+'.png' )
    copyfile(  sem_files[i],  'full_data/annotations/validation/'+str(i).zfill(5)+'.png' )
    
    ins = np.array(Image.open(ins_files[i]))
    ins = get_instance(ins)
    ins = Image.fromarray(ins.astype('uint8'))    
    ins.save( 'full_data/annotations_instance/validation/'+str(i).zfill(5)+'.png'  )
    









