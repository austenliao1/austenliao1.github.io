# CS180 (CS280A): Project 1 starter Python code

# these are just some suggested libraries
# instead of scikit-image you could use matplotlib and opencv to read, write, and display images

import numpy as np
import skimage as sk
import skimage.io as skio
import time

from utils import construct_pyramid, align

# name of the input file
filenames = [
    "cathedral.jpg",
    "church.tif",
    "emir.tif",
    "harvesters.tif",
    "icon.tif",
    "lady.tif",
    "melons.tif",
    "monastery.jpg",
    "onion_church.tif",
    "sculpture.tif",
    "self_portrait.tif",
    "three_generations.tif",
    "tobolsk.jpg",
    "train.tif"
]

for imname in filenames:
    pic_name = imname.split(".")[0]

    # read in the image
    im = skio.imread(f"data/{imname}")

    # convert to double (might want to do this later on to save memory)    
    im = sk.img_as_float(im)
        
    # compute the height of each part (just 1/3 of total)
    height = np.floor(im.shape[0] / 3.0).astype(np.int64)

    # separate color channels
    b = im[:height]
    g = im[height: 2*height]
    r = im[2*height: 3*height]

    # align the images
    # functions that might be useful for aligning the images include:
    # np.roll, np.sum, sk.transform.rescale (for multiscale)

    # crop borders
    img_height = len(b)
    img_width = len(b[0])

    b = b[int(img_height*0.15):int(img_height*0.85), int(img_width*0.15):int(img_width*0.85)]
    g = g[int(img_height*0.15):int(img_height*0.85), int(img_width*0.15):int(img_width*0.85)]
    r = r[int(img_height*0.15):int(img_height*0.85), int(img_width*0.15):int(img_width*0.85)]
        
    # start timer
    start_time = time.time()
    
    # construct pyramids
    b_pyramid = construct_pyramid(b)
    g_pyramid = construct_pyramid(g)
    r_pyramid = construct_pyramid(r)

    # align images
    g_opt_x, g_opt_y, ag = align(g_pyramid, b_pyramid)
    r_opt_x, r_opt_y, ar = align(r_pyramid, b_pyramid)
    
    # assert g_opt_x == r_opt_x
    # assert g_opt_y == r_opt_y
    
    # create a color image
    im_out = np.dstack([ar, ag, b])

    # save the image
    fname = f'../outputs/{pic_name}.jpg'
    im_out_uint8 = sk.img_as_ubyte(im_out)
    
    with open("../outputs/shifts.txt", "a") as log_file:
        log_file.write(f"{fname}, green: {g_opt_x} {g_opt_y}, red: {r_opt_x} {r_opt_y} \n")

    end_time = time.time()

    print("duration: ", end_time - start_time)

    skio.imsave(fname, im_out_uint8)

    # display the image
    # skio.imshow(im_out_uint8)
    # skio.show()