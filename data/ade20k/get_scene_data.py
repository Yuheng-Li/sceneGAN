import os 
import pandas as pd 
from PIL import Image
from shutil import copyfile


# for full data we generate a full_data for a specific scene 
# let's say bedrooms, then this code will geenrate a bedroom full data folder 
# You have to have full_data

WANTED_SCENE = 'bedroom'
dataroot = 'full_data_'+WANTED_SCENE
if os.path.exists(dataroot):
    raise IOError('output folder exists, if data is there you do not need run this code again') 

os.makedirs(dataroot)

os.makedirs(dataroot+'/images')
os.makedirs(dataroot+'/images/training')
os.makedirs(dataroot+'/images/validation')

os.makedirs(dataroot+'/annotations')
os.makedirs(dataroot+'/annotations/training')
os.makedirs(dataroot+'/annotations/validation')

os.makedirs(dataroot+'/annotations_instance')
os.makedirs(dataroot+'/annotations_instance/training')
os.makedirs(dataroot+'/annotations_instance/validation')


# these three files are same in files or files150 
scenes = pd.read_csv( 'files/scene.txt', sep='  ', lineterminator='\n', header=None, engine='python')[0].tolist() 
files = pd.read_csv( 'files/filename.txt', sep='  ', lineterminator='\n', header=None, engine='python')[0].tolist()
typesets = pd.read_csv( 'files/typeset.txt', sep='  ', lineterminator='\n', header=None, engine='python')[0].tolist()



def fetch_data(file, typeset):
    temp = 'training' if typeset==1 else 'validation'
    img = os.path.join('full_data', 'images', temp, file )  
    sem = os.path.join('full_data', 'annotations', temp, file[:-3]+'png' )  
    ins = os.path.join('full_data', 'annotations_instance', temp, file[:-3]+'png' )  
    return [img, sem, ins]
    

def store_data(data):
    temp = 'training' if typeset==1 else 'validation'    
    copyfile( data[0] , data[0].replace("full_data", dataroot) )
    copyfile( data[1] , data[1].replace("full_data", dataroot) )
    copyfile( data[2] , data[2].replace("full_data", dataroot) )
    

for scene, file, typeset in zip( scenes, files, typesets ):
    if scene == WANTED_SCENE:
        data = fetch_data(file, typeset)
        store_data(data)
        
    



















