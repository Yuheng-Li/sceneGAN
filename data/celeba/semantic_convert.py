import os 
import numpy as np 
from PIL import Image 
import matplotlib.pyplot as plt 



"""

below is the list (from official github) used to create semantic map. Note that 0 is unlabeled, so skin is 1 
['skin', 'nose', 'eye_glass', 'l_eye', 'r_eye', 'l_eyebrow', 'r_eyebrow', 'l_ear', 'r_ear', 'mouth', 'u_lip', 'l_lip', 'hair', 'hat', 'ear_ring', 'necklace', 'neck', 'cloth']
[1     ,  2,      3,           4,       5,       6,           7,           8,        9,       10,      11,      12,     13,     14,    15,         16,         17,      18 ]

This scipt will convert:

unlabeled 0 --> 24  
neck 17 --> 19 
cloth 18 --> 4 
hat 14 --> 1 
hair 13 --> 2 
all_the_other --> 12 


"""


mapping = {0: 24,          
           13: 2,
           14: 1,          
           17: 19,
           18: 4 }


source_folder = 'CelebAMask'
output_folder = 'annotations'   # please manually mkdir 
output_instance_folder = 'annotations_instance'  # please manually mkdir 



masks = os.listdir(source_folder)
masks  = [  os.path.join(source_folder, item) for item in masks  ]
masks.sort()



for idx, mask in enumerate(masks):
    print(idx)
    mask = plt.imread(mask)*255
    new_mask = np.ones((512,512))*12
    
    for key in mapping:
        region = mask==key
        new_mask = region*mapping[key]+(1-region)*new_mask

    _,instance_mask = np.unique(new_mask, return_inverse=True)
    instance_mask = instance_mask.reshape(new_mask.shape)
        
    new_mask = Image.fromarray(new_mask.astype('uint8'))
    new_mask.save(  os.path.join(output_folder, str(idx).zfill(5)+'.png')  )

    instance_mask = Image.fromarray(instance_mask.astype('uint8'))
    instance_mask.save(  os.path.join(output_instance_folder, str(idx).zfill(5)+'.png')  )

    