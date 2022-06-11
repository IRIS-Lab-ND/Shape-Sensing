# External Shape Sensing of Vine Robots



## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Notes](#notes)

## Prerequisites (skip steps if appropriate)
 - Install `pip` on your machine by entering the following commands in Terminal:

 ```
 curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
 python3 get-pip.py
 ```
 - Install `virtualenv` on your machine by entering:
 ```
 pip3 install virtualenv
 ```

## First-Time Installation

 - Clone this GitHub repository onto your local machine and navigate to it in Terminal.
 - Enter the following commands:

 ```
 python3 -m virtualenv shape_sensing_virtualenv
 source shape_sensing_virtualenv/bin/activate
 pip3 install -r requirements.txt
 ```
 - Once all installation is complete, enter the following command to deactivate the virtual environment:
 ```
 deactivate
 ```

## Usage
 - The virtual environment needs to be active in order for the program to function as intended. To do this, ensure that you are inside the correct directory (the cloned repository) and enter the following command:
 ```
 source shape_sensing_virtualenv/bin/activate
 ```

 - To run the program, enter the following:
```
python3 external_shape_sensing.py
```
and follow the instructions.

 - Deactivate the virtual environment at the end of your session by entering the following command:
```
 deactivate
 ```


## Notes
 - The python program writes position data to a `.tsv` file, which can then be animated by using a MATLAB script.
