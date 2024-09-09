import numpy as np
import skimage as sk
import cv2

def largest_smaller_power_of_2(larger):
    x = 2
    while x * 2 < larger:
        x *= 2
    return x

def shift_image_vertically(im, num_pixels):
    return np.roll(im, num_pixels, axis=0)

def shift_image_horizontally(im, num_pixels):
    return np.roll(im, num_pixels, axis=1)
    
# horizontal shift
# pseudocode
# if is small enough,
    # naively search in entire image
# else,
    # get center of search from the recursive call
    # do a search within some range of the center thing
    
# resize to power of 2

def find_shift(img_to_align, target_img, search_center_x, search_center_y):
    best_x_shift = -1
    best_y_shift = -1
    max_similarity = 0
    
    for i in range(search_center_y - 10, search_center_y + 10):
        for j in range(search_center_x - 10, search_center_x + 10):
            # apply 2D shift
            shifted_img = shift_image_vertically(img_to_align, i) 
            shifted_img = shift_image_horizontally(shifted_img, j)
            
            # calculate similarity
            similarity = sk.metrics.structural_similarity(shifted_img, target_img, data_range=1)
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_x_shift = j
                best_y_shift = i
        
    return best_x_shift, best_y_shift

def construct_pyramid(img):
    images = [img]
    
    MIN_IMG_SIZE = 64
    
    # while image length is larger than a certain quantity
    resized_img = images[-1]
    while len(resized_img) > MIN_IMG_SIZE:
        height = len(resized_img)
        width = len(resized_img)
        
        resized_img = cv2.resize(resized_img, (height // 2, width // 2))
        images.append(resized_img)
    
    return images

def find_optimal_shift(shift_images, target_images):
    estimate_x = 0
    estimate_y = 0
    
    print("num images", len(shift_images))
    
    for i in range(len(shift_images) - 1, -1, -1):
        print(i)
        image_to_shift = shift_images[i]
        image_to_target = target_images[i]
        updated_estimate_x, updated_estimate_y = estimate_x * 2, estimate_y * 2
        
        estimate_x, estimate_y = find_shift(image_to_shift, image_to_target, updated_estimate_x, updated_estimate_y)
    
    return estimate_x, estimate_y



def align(shift_pyramid, target_pyramid):
    # get shift values
    opt_x, opt_y = find_optimal_shift(shift_pyramid, target_pyramid)
    
    # shift image
    final_shifted_image = shift_image_vertically(shift_image_horizontally(shift_pyramid[0], opt_x), opt_y)
    return opt_x, opt_y, final_shifted_image