# External Shape Sensing (vine robots)



## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Notes](#notes)

## Installation

 - Clone this GitHub repository onto your local machine and navigate to it in terminal.
 - If you do not already have `pip` installed, do so by following [these](https://www.geeksforgeeks.org/how-to-install-pip-in-macos/) instructions.
 - To install `virtualenv`, enter the following command (skip this step if you already have virtualenv installed):

 ```
pip3 install virtualenv
```

 - Enter the following commands:

 ```
 python3 -m virtualenv shape_sensing_virtualenv
 source shape_sensing_virtualenv/bin/activate
 pip3 install -r requirements.txt
 ```

## Usage

To run the program, enter the following:
```
python3 filename.py
```
and follow the instructions.


## Notes
 - The python program writes position data to a `.tsv` file, which can then be animated by using a MATLAB script.
