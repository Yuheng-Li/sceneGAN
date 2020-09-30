These are files containing statistics for ADE (3148 class).



All files within this folder do not belong to original dataset. These files are results of preprocessing index_ade20k.mat 
The code is process_index_ade20k.ipynb. Please refer the code for more details. 

N: total files (22210) 
C: total classes (3148) 


objectnames.txt: each row is a name for an class. It does not have to be main object(car people..), it can be part
objectcounts.txt: each row is count of an class listed in above file 
proportionClassIsPart.txt: the proportion of times that class c behaves as a part. If it is 0 then it is a main object  


filename.txt: each row is a filename of an image 
folder.txt: folder path to each filename 
scene.txt: which scene it belongs to for each file 
typeset.txt: train or val 


objectsPart.npy: np.array with shape (N,C). Counting how many times an object is a part in each image. objectIsPart(i,c)=m if in image i object class c is a part of another object m times 
objectsPresence.npy: np.array with shape (N,C). With the object counts per image. objectPresence(i,c)=n if in image i there are n instances of object class c.
