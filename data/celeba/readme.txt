Purpose of these scripts: we convert celeba data into format used by SceneGAN, and convert semantic labels according to 
Human dataset (from Adobe) such that we can use this processed data to augment number of face images. 

Note that: during our experiments we found that faces from Human have more variances in terms of orientation thus you can not 
directly use celeba to do data augmentation, you need to match distributions based on face orientation. Check FaceDistMatch folder 


First run change_name.py to convert image name (do padding 0.png --> 00000.png)

Then run get_mask.py This will combine all part masks into a semantic masks (This code
is based on offical code)

Fianlly run sementic_convert.py. This will convert semantic labels into human_standing data 
format also in the meantime it will create annotations_instance folder. Please check its details for how does semantic convertion work

Run split.py which will create a full_data folder 


After that you can rm all folders here except for CelebaRawData. If you want to process it again, just follow the above processes.
You can not use data in full_data folder, check FaceDistMatch 


