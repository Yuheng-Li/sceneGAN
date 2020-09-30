This is the order you should check the code and files <br />

Originally I download ADE dataset from https://groups.csail.mit.edu/vision/datasets/ADE20K/ <br />
and there are only one images folder and a mat file inside it. <br />

First check files folder to process mat file and get all statistic files we need. <br />

Then I created ADE_stat.py as a helper class to see statistic of this class.  <br />

Later I realiszed that there is another version of ADE (http://sceneparsing.csail.mit.edu/) with only 150 classes.  <br />
But it does not have instance annotation and images are in small resolution. So I convert ADE(3184) into 150 classes. <br />
See get_full_data.py for details. <br />

In order to get same files folder for our 150 classes one, please run get_files150.py. And files150 folder is a placehoder <br />

If you only want to get same structrue as full_data just for a specific scene (say bedroom), run get_scene_data.py <br />




