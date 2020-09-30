These are files containing statistics for ADE (3148 class). <br />
(I did not upload those files, please run process_index_ade20k.ipynb to get them)


All files within this folder do not belong to original dataset. These files are results of preprocessing index_ade20k.mat <br />
The code is process_index_ade20k.ipynb. Please refer the code for more details. 

N: total files (22210) <br />
C: total classes (3148) 


objectnames.txt: each row is a name for an class. It does not have to be main object(car people..), it can be part<br />
objectcounts.txt: each row is count of an class listed in above file <br />
proportionClassIsPart.txt: the proportion of times that class c behaves as a part. If it is 0 then it is a main object <br />


filename.txt: each row is a filename of an image <br />
folder.txt: folder path to each filename <br />
scene.txt: which scene it belongs to for each file <br />
typeset.txt: train or val <br />


objectsPart.npy: np.array with shape (N,C). Counting how many times an object is a part in each image. objectIsPart(i,c)=m if in image i object class c is a part of another object m times <br />
objectsPresence.npy: np.array with shape (N,C). With the object counts per image. objectPresence(i,c)=n if in image i there are n instances of object class c.
