First run change_name.py to convert image name (do padding 0.png --> 00000.png)

Then run get_mask.py This will combine all part masks into a semantic masks (This code
is based on offical code)

Fianlly run sementic_convert.py. This will convert semantic labels into human_standing data 
format also in the meantime it will create annotations_instance folder. Please check its details for how does semantic convertion work

Please run split.py which will create a full_data folder 


After that you can rm all folders here except for CelebaRawData. If you want to process it again, just follow the above processes 


