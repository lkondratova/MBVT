MBVT 

This macaque brain visualization tool (MBVT) is designed to visualize high throughput data. 

The list of areas represented:
00 - medulla
01 - pons
02 - cerebellum
03 - midbrain
04 - thalamus
05 - hippocampus
06 - caudate
07 - putamen
08 - occipital lobe
09 - temporal lobe
10 - parietal lobe 
11 - prefrontal lobe
12 - frontal lobe

The areas information is stored in labels.py file. 

Getting Started

There are three functions defined in a script file whole_one_color(), whole_colorscale() , and two_sided_colorscale().

Function whole_one_color()  applies one color (originally blue) to 13 areas in the macaque’s brain. The transparency of the label corresponds to the value (from 1 to 5) stored in values.csv file for the particular sample and area (see whole_one_color_example_file.pdf).

Function whole_colorscale()  applies five different colors corresponding to values in values.csv file (1 - blue, 2 - yellow, 3 - orange, 4 - red, 5 - dark red). The main difference between this function and whole_one_color() is that whole_colorscale() replaces pixels with new color while whole_one_color() puts the mask on the top of the template saving the background pixels (see whole_colorscale_example_file.pdf).

Function two_sided_colorscale() applies DNA data from values.csv file (1 to 5) to the lleft part of the template and RNA data to the right part using a cold-hot colormap (see two_sided_colorscale_example_file.pdf).


Prerequisites

Python 3. x
Packages:
OpenCV, csv, Pillow

Running the tests

We recommend running the test on fake data in the value.csv file before replacing them with the real ones.
Usage
Download or clone the whole mbvt repository. Run python ./mbvt.py in a terminal from the folder. Then respond to user input request by entering the name of the function that you are going to use (whole_one_color(), whole_colorscale(), two_sided_colorscale()). 

Output folder
The folder named ‘output’ will be created automatically. It should be removed or renamed before each new run. This folder will contain each template with applied values. 

Pdf folder
This folder will be created in the output folder and will contain the output .pdf file. All the images from the .pdf file will be stored in this folder in .png format.

Preparation of values.csv file
The file values.csv is stored in the mbvt repository and by default contains fake data, which should be replaced with data to be applied by the script (run the test on fake data to make sure the script is working on your computer). 
The current version does not make data transformation. Thus, all the data points should be integers from 0 to 5. 
Each column represents a particular area in a macaque’s brain.  Columns should not be removed or rearranged. The first column is for the names of the samples. It will appear in the final .pdf file as a compact legend. Do not use special characters in names. Use underscore (“_”) as a separator (for example AAV_0_Inj_0_Animal_0). For function two_sided_colorscale() Each sample name should be used twice: once ending with ‘_DNA’ (representing DNA results for coloring the left part) and the second time ending should be ‘_RNA’ (representing RNA results for coloring the right side). For example, AAV_0_Inj_0_Animal_0_DNA and AAV_0_Inj_0_Animal_0_RNA. In a final .pdf file images will be represented in alphabetical order regardless of the order in a values.csv file. 	

Authors
Liudmyla Kondratova (development)
Ron J. Mandel (consulting)
Sergei Zolotukhin (PI)

