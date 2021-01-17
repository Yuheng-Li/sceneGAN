from shutil import copyfile
import os
import random
import shutil
random.seed(1)


"""
This code will create a full_data folder
Please make sure there are images, annotations and annotations_instance exist in the current folder
"""



def make_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)



train_percentage = 90

full_images = 'images'
full_annotations = 'annotations'
full_annotations_instance = 'annotations_instance'



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



   
images_files = os.listdir(full_images)
annotations_files = os.listdir(full_annotations)
annotations_instance_files = os.listdir(full_annotations_instance)
images_files.sort()
annotations_files.sort()
annotations_instance_files.sort()

assert len(images_files) == len(annotations_files) == len(annotations_instance_files) 
   
   
total = len(images_files)
train_index = random.sample(  list(range(total)),  int(total*train_percentage/100)  )

for idx in range(total):
    print(idx)
    img_src = os.path.join( full_images, images_files[idx] )
    sem_src = os.path.join( full_annotations, annotations_files[idx])
    ins_src = os.path.join( full_annotations_instance, annotations_instance_files[idx])
   
    if idx in train_index:
        img_dst = os.path.join( 'full_data/images/training', images_files[idx] )
        sem_dst = os.path.join( 'full_data/annotations/training', annotations_files[idx])
        ins_dst = os.path.join( 'full_data/annotations_instance/training', annotations_instance_files[idx])
    else:
        img_dst = os.path.join( 'full_data/images/validation', images_files[idx] )
        sem_dst = os.path.join( 'full_data/annotations/validation', annotations_files[idx])
        ins_dst = os.path.join( 'full_data/annotations_instance/validation', annotations_instance_files[idx])
       
    copyfile(img_src, img_dst)
    copyfile(sem_src, sem_dst)
    copyfile(ins_src, ins_dst)