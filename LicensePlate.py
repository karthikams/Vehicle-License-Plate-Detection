
# coding: utf-8

# In[2]:


#Processing for single image
#Extension: For loop for multiple images
#Addition for character segmentation

from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import skimage
from skimage import img_as_uint
import pytesseract
from PIL import Image
import os
from glob import glob

get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


def license_plate(full_image):
    
    car_image = full_image[1430:1572,1410:1790]
    
    # the next line is not compulsory however, a grey scale pixel
    # in skimage ranges between 0 & 1. multiplying it with 255
    # will make it range between 0 & 255 (something we can relate better with
    gray_car_image = car_image * 255
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(gray_car_image, cmap="gray")
    threshold_value = threshold_otsu(gray_car_image)
    binary_car_image = gray_car_image >= threshold_value
    ax2.imshow(binary_car_image, cmap="gray")
    plt.show()
    
    #Drawing bounding boxes over detected license plate
    label_image = measure.label(binary_car_image)
    fig, (ax1) = plt.subplots(1)
    ax1.imshow(gray_car_image, cmap="gray");

    for region in regionprops(label_image):
        if region.area < 1000:
            #if the region is so small then it's likely not a license plate
            continue
        # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        region_height = max_row - min_row
        region_width = max_col - min_col
        #print(region.bbox)
    
        if min_row != 0 and min_col != 0:
            #Height will be less than width for license plate
            if max_row - min_row < max_col - min_col:
                rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="green", linewidth=2, fill=False)
                ax1.add_patch(rectBorder)
                ax1.imshow(binary_car_image, cmap="gray")

                # #crooping the licene plate region
                plate_like_objects = []
                plate_like_objects.append(binary_car_image[min_row:max_row,
                                 min_col:max_col])  


    #inverting the pixel values, black to white and vice versa
    license_plate = np.invert(plate_like_objects[0])
    
    
    #save the above cropped license plate

    labelled_plate = measure.label(license_plate)
    fig, ax1 = plt.subplots(1)
    ax1.imshow(license_plate, cmap="gray")
    skimage.io.imsave("licenseplate.jpg",img_as_uint(license_plate))

    #from skimage.transform import resize
    fig, ax1 = plt.subplots(1)
    ax1.imshow(license_plate, cmap="gray")
    # the next two lines is based on the assumptions that the width of
    # a license plate should be between 5% and 15% of the license plate,
    # and height should be between 35% and 60%
    # this will eliminate some

    #get the entire license plate region by adjusting height and width

    character_dimensions = (0.50*license_plate.shape[0], 0.85*license_plate.shape[0], 0.08*license_plate.shape[1], 1*license_plate.shape[1])
    min_height, max_height, min_width, max_width = character_dimensions

    characters = []
    counter=0
    column_list = []
    region_area = []
    name = ''

    for regions in regionprops(labelled_plate):
        minRow, minCol, maxRow, maxCol = regions.bbox
        region_height = maxRow - minRow
        region_width = maxCol - minCol

        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width:
            roi = license_plate[minRow+3:maxRow-3, minCol:maxCol]
            print(regions.bbox) 
            rect_border = patches.Rectangle((minCol, minRow), maxCol - minCol, maxRow - minRow, edgecolor="red",
                                          linewidth=2, fill=False)
            ax1.add_patch(rect_border)
            name = str(minRow) + str(maxRow) + '.jpg'
            skimage.io.imsave(name,img_as_uint(roi))        

    plt.show()

    # Saving individual creaters
    cars_image = imread(name)
    labelled_plate = measure.label(cars_image)
    cars_image = np.invert(cars_image)
    var = int(cars_image.shape[1]/7)

    for i in range(7):
        name = "j"+ str(i)+".jpg"
        i1 = cars_image[0:cars_image.shape[0],(var*i):var*(i+1)]
        skimage.io.imsave("output/characters/"+name,img_as_uint(i1))

    print("Character Segmentation Performed")
    
    #Reading individual characters using OCR
    path = "output/characters"
    licenseplate = []

    num_files = len(glob(path + '/*'))

    for i in range(num_files):   
        text = pytesseract.image_to_string(Image.open(os.path.join(path,"j"+str(i)+".jpg")), config='--psm 8 oem 3')
        licenseplate.append(text)

    lic_plate = "".join(licenseplate)
    print("Detected License Plate Number is: ", lic_plate)
    
    return lic_plate

