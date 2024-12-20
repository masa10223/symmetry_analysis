# Deciphering the origin of developmental stability: the role of intracellular expression variability in evolutionary conservation　
Yui Uchida,  Masato Tsutsumi,  Shunsuke Ichii,  Naoki Irie,  Chikara Furusawa

Journal: Evolution & Development.  
doi: https://doi.org/10.1111/ede.12473

URL: https://onlinelibrary.wiley.com/doi/abs/10.1111/ede.12473



## What this repository is
This repository provides GUI-operated software that can automatically extract expression regions by scrolling or typing in threshold values.


## How to use 
```
git clone https://github.com/masa10223/symmetry_analysis
cd scripts
pip install requirements.yml
python Extract_Embryo_GUI.py
```
You can then scroll or type in the threshold values from the image in the GUI screen to automatically extract the expression area.

![github_movie](https://github.com/masa10223/symmetry_analysis/assets/38234714/71ac86bd-8ad2-4f6d-8809-8c6367eb55ca)



## Description of buttons
### Draw Area
This button allows you to enclose the expression area you wish to extract with a blue rectangle.
### Crop Area
This button allows you to crop the image inside the blue rectangular area enclosed by the Draw area. The cropped area will be displayed in the window on the right.
## Detect Area
When you move the scale bar in "Scroll Threshold," the right window will display all the areas below the value in the cropped area. The scale bar can be moved freely using the numeric keypad. The same operation can also be performed on the text input form above it by typing a number between 0 and 255. In the latter case, clicking "Detect Area" button will display the area below that value in the window on the right.
In both cases, clicking the Binarize button will fill the largest of the displayed rectangular areas.　　Tweak the number so that this equals the expression area.
