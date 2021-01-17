from shutil import copyfile
import os 
from PIL import Image
"This script just renames original images"


source_folder = 'CelebaRawData/CelebA-HQ-img'
output_folder = 'images'   # you should manually mkdir this before 

source = os.listdir(source_folder)
source.sort()


for src in source:
    basename = os.path.basename(src)[:-4]
    src = os.path.join(source_folder, src)
    dst = os.path.join(output_folder, basename.zfill(5)+'.jpg')
    img = Image.open(src).resize(  (512,512), Image.NEAREST  )
    img.save(dst)