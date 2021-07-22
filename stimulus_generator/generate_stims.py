import os
import shutil
from PIL import Image
import numpy as np
from numpy.random import randint
import scipy.io
import imageio


# takes an image file path and returns the 3D numpy array representing it
def get_image_array(path):
    image = Image.open(path)
    ans = np.asarray(image)
    image.close()
    return ans

def replace_mask_colour (study_image, ZL_colour):
    ZL_file = scipy.io.loadmat('ZL_colors.mat') # load the ZL_colors file

    # access the RGB fields:
    ZL_red = ZL_file['ZL_colors'][0][0][0][0][int(ZL_colour - 1)]
    ZL_green = ZL_file['ZL_colors'][0][0][1][0][int(ZL_colour - 1)]
    ZL_blue = ZL_file['ZL_colors'][0][0][2][0][int(ZL_colour - 1)]

    # specify the mask colors to be replaced
    colour_file_data = get_image_array('vcs_stim\\shapecolourv4_colour.jpg')
    
    # the +-1 is to capture visual artifacts in the image while assigning new values
    # maybe this can be moved somewhere cleanly so that it doesn't have to process every time, 
    # but this is pretty fast to begin with, and time accuracy hasn't been an issue
    mask_colours = np.empty([3, 3])
    mask_colours[0][0] = colour_file_data[0][0][0]
    mask_colours[0][1] = mask_colours[0][0] - 1
    mask_colours[0][2] = mask_colours[0][0] + 1

    mask_colours[1][0] = colour_file_data[0][0][1]
    mask_colours[1][1] = mask_colours[1][0] - 1
    mask_colours[1][2] = mask_colours[1][0] + 1

    mask_colours[2][0] = colour_file_data[0][0][2]
    mask_colours[2][1] = mask_colours[2][0] - 1
    mask_colours[2][2] = mask_colours[2][0] + 1

    # now access the color data of the study image file:
    red_channel = np.array(study_image[:, :, 0])
    green_channel = np.array(study_image[:, :, 1])
    blue_channel = np.array(study_image[:, :, 2])

    # replace the mask-valued colors with the specified ZL color
    red_channel[red_channel == mask_colours[0][0]] = ZL_red
    red_channel[red_channel == mask_colours[0][1]] = ZL_red
    red_channel[red_channel == mask_colours[0][2]] = ZL_red
    red_channel[red_channel == mask_colours[0][0] + 2] = ZL_red
    red_channel[red_channel == mask_colours[0][0] - 2] = ZL_red
    green_channel[green_channel == mask_colours[1][0]] = ZL_green
    green_channel[green_channel == mask_colours[1][1]] = ZL_green
    green_channel[green_channel == mask_colours[1][2]] = ZL_green
    green_channel[green_channel == mask_colours[0][0] + 2] = ZL_green
    green_channel[green_channel == mask_colours[0][0] - 2] = ZL_green
    blue_channel[blue_channel == mask_colours[2][0]] = ZL_blue
    blue_channel[blue_channel == mask_colours[2][0]] = ZL_blue
    blue_channel[blue_channel == mask_colours[2][0]] = ZL_blue
    blue_channel[blue_channel == mask_colours[0][0] + 2] = ZL_blue
    blue_channel[blue_channel == mask_colours[0][0] - 2] = ZL_blue
    
    return np.dstack((red_channel, green_channel, blue_channel)) # re-combine the three channels

# generates a list of dictionaries for use with TrialHandler, one dictionary of trial params per trial
# keys: 'condition' (either 1, 2, or 3), 'shape_1' (VCS 1 - 360), 'shape_2' (VCS 1 - 360), 'shape_3' (VCS 1 - 360),
#       'colour_1' (ZL 1 - 180), 'colour_2' (ZL 1 - 180), 'colour_3' (ZL 1 - 180), 'study_shape', 'study_colour',
#       'shape_jitter' (note: same for every trial), 'colour_jitter' (unique per trial)
def trial_matrix(trial_num=60):
    trial_lists = []
    for i in range(trial_num):
        rand_shape = randint(1, 361)
        rand_colour = randint(1, 181)

        shape_list = [rand_shape + i * 36 for i in range(1, 11)]
        for shape in shape_list:
            if shape > 360:
                shape_list[shape_list.index(shape)] = shape - 360
        
        colour_list = [rand_colour + i * 18 for i in range(1, 11)]
        for colour in colour_list:
            if colour > 180:
                colour_list[colour_list.index(colour)] = colour - 180
        
        trial_list = [(shape_list[i], colour_list[i]) for i in range(10)]
        trial_lists.append(trial_list)

    if os.path.exists('generated_stim'):
        shutil.rmtree('generated_stim')
    os.makedirs('generated_stim')

    for i, trial in enumerate(trial_lists):
        for j in range(10):
            shape_path = f'vcs_stim\\shapecolourv4_{trial[j][0]}.jpg'
            filepath = f'generated_stim\\t{i+1}_{j+1}.jpg'
            imageio.imsave(filepath, replace_mask_colour(get_image_array(shape_path), trial[j][1]))

trial_matrix()