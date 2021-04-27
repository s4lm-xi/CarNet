# CarNet

<hr>

## Note
<code>Python 3.8.3</code>.
In order to change the image resolution, modify the following: `line 14` in `detect.py`
<hr>

## Installation

after cloning the repo, you need to install the project requirements by executing the following command in your terminal.
<hr>
### Optional
Create a virtual enviroment before installing the required dependencies
<br>
execute the following command to create a virtual enviroment  
`pip install virtualenv`  

Create an enviroment called env  
`virtualenv env`  

then activate the enviroment, within the project directory  
**Linux**  
`source env/bin/activate`  

**Windows**  
`env/Scripts/activate.bat`  
<hr>
Install the required dependencies  
`pip install -r requirements.txt`  
<hr>

## Real-Time Detection
`python live.py -t 30`
### Options
    --help -h          show the help message and exit

    --thresh -t          the threshold value of each frame 0-100. lower for
                        darker areas, higher for brighter areas. Default is 30  

after launching the script, select the desired **Region of Intrest** in a shape of a polygon, covering the region of the road lanes. Start from the top right and go counter-clockwise.

**Example**   
***Step 1***: 
Click the first point of the polygon. The small black dot is the result of the first click

![](other/readme/1.png)  

***Step 2***: 
Then select the 2nd point on the top left. The program will automatically draw a line between the two selected points

![](other/readme/2.png)  

***Step 3***: 
The 3rd point would be the bottom left of the lane.

![](other/readme/3.png)  

***Step 4***: 
Finally, the final point would be the remaining corner of the polygon which is the bottom right corner.

![](other/readme/4.png)  

Then the program should be running using your default webcam, if running a third-party webcam please change the code however it suits your device.

The detection will be on the same time as the program grabs each frame of the live stream, if you find some lanes arent being detected pleane fine-tune the **--thresh** argument accordingly


