# How To Setup Client
## step 1
#### Create Virtual Env 
* set up enviroment on anaconda with python3.8 and activate the enviroment
```
!conda create -n myenv python=3.8 
!conda activate myenv
```
Refer : [https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html]

#### NOTE : On Linux Machine Prefer Normal Enviroment Not conda (Reason : Tkinter(GUI-Package) do not work proerly with Conda in linux)
* For Linux Refer : https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
```
!pip install virtualenv
!virtualenv mypython
!source mypython/bin/activate
```

## step 2
install dependencies
```
!pip install Pillow

!pip install opencv-python

!pip install opencv-contrib-python

!pip install numpy

!pip install pprint

!pip install mysql-connector-python

!pip install DateTime

!pip install pdf2image

!pip install python-docx
```
> if Windows Machine:
```
!pip install docx2pdf
!conda install -c conda-forge poppler
```
# step 3
##### Dawnload Video From : 
* https://drive.google.com/drive/folders/1mu1aA6g2nnYfz_6xJbsgh1ld51sSyISf?usp=sharing
##### Modify Configre.json File
```
{
	"APIURL":"http://192.168.1.227:8000/test/",     // Your Server Url Here
	"DBconn": {	"host":"db4free.net",           // Database Credentials
				"user":"ksv1234",
				"passwd":"ldrp-itr",
				"database":"ksvrto",
				"port":3306
	},
	"VideoPath":"<Primary Video Path>",         // Video Path
	"VideoBasePath":"<All Video Folder Path>",  // Video Folder
	"Offances":[ 
				{	
					"Offance":"Violating parking rules",	
					"fine1":"500",
					"fine2":"1000"		
				},
        ...
        // add Other Offance Here
			]	
}
```


# step 4 
Run MainFile

```
!python MainGui.py
``` 
