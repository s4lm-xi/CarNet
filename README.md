# CarNet

<hr>

## Note
<code>Python 3.8.3</code>.
<hr>

## Installation

after cloning the repo, you need to install the project requirements by executing the following command in your terminal.
<hr>
##### Optional
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



