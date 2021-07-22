import os
import math
from math import sqrt
import ctypes
from datetime import datetime
import random

from psychopy import visual
from psychopy.visual import circle
from PIL import Image
from PIL import ImageFilter
import numpy as np
from numpy.random import randint, normal, shuffle
from numpy import (mod, sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray)
import scipy
import dropbox
import requests


# returns the angle defined by the point (x, y) with respect to the circle centered at (center_x, center_y)
def get_angle (x, y, center_x, center_y):
    delta_x = x - center_x
    delta_y = y - center_y 
    radius = sqrt(delta_x**2 + delta_y**2)

    # determine the angle using cosine
    if radius != 0:
        angle = math.acos(delta_x / radius) * 180 / math.pi  # in degrees
    
    # correct edge cases:
    if (delta_x == 0 and delta_y > 0):
        return 90
    elif (delta_x == 0 and delta_y < 0):
        return 270
    elif (delta_x > 0 and delta_y == 0):
        return 0
    elif (delta_x < 0 and delta_y == 0):
        return 180
    elif (delta_x < 0 and delta_y < 0):
        angle = 360 - angle
    elif (delta_x > 0 and delta_y < 0):
        angle = 360 - angle

    if radius == 0:
        return 0 # is there a better way of doing this?

    return angle

# takes an image file path and returns the 3D numpy array representing it
def get_image_array(path):
    image = Image.open(path)
    ans = np.asarray(image)
    image.close()
    return ans

# returns a list of 180 stims (psychopy.visual.ImageStim) corresponding to the response color wheel
def circle_stims(win, trial_handler, pos1, test_core_radius):
    # load colors
    ZL_file = scipy.io.loadmat('ZL_colors.mat') # load the ZL_colors file

    # access the RGB fields:
    ZL_red = ZL_file['ZL_colors'][0][0][0][0]
    ZL_green = ZL_file['ZL_colors'][0][0][1][0]
    ZL_blue = ZL_file['ZL_colors'][0][0][2][0]
    
    stims = []
    for i in range(180):
        temp_colour_index = (trial_handler.thisTrial['colour_jitter'] + i + 1) % 180
        if temp_colour_index == 0:
             temp_colour_index == 180
                
        circle_stim = circle.Circle(win)
        circle_stim.pos = (0, 0)
        circle_stim.radius = test_core_radius + i
        circle_stim.units = 'pix'
        circle_stim.lineWidth = 2
        circle_stim.setLineColor((ZL_red[temp_colour_index], ZL_green[temp_colour_index], ZL_blue[temp_colour_index]), colorSpace='rgb255') # must include color space
        stims.append(circle_stim)
    
    return stims

def distance(pos_1, pos_2):
    return math.sqrt((pos_2[0] - pos_1[0])**2 + (pos_2[1] - pos_1[1])**2)

# generates a list of dictionaries for use with TrialHandler, one dictionary of trial params per trial
# keys: 'condition' (either 1, 2, or 3), 'shape_1' (VCS 1 - 360), 'shape_2' (VCS 1 - 360), 'shape_3' (VCS 1 - 360),
#       'colour_1' (ZL 1 - 180), 'colour_2' (ZL 1 - 180), 'colour_3' (ZL 1 - 180), 'study_shape', 'study_colour',
#       'shape_jitter' (note: same for every trial), 'colour_jitter' (unique per trial)
def trial_matrix(trial_num=60):
    # temp lists to store values, later added to dict
    conditions = []
    trial_info = []
    
    # column 1: condition number (1 or 2)
    if (trial_num % 3 != 0):
        raise ValueError('Number of trials must be divisible by 3')

    conditions = np.tile([1, 2, 3], int(trial_num/3))
    np.random.shuffle(conditions)
    conditions = conditions.tolist()
    
    rand_jitter = randint(1, 361) # value used for shape jitter
    for i in range(trial_num): 
        # column 2 and 3: indices of shape 1 and shape 2
        sample_shape = randint(1, 361)
        shape1 = sample_shape
        shape2 = sample_shape + 60
        shape3 = sample_shape + 120
        shape4 = sample_shape + 180
        shape5 = sample_shape + 240
        shape6 = sample_shape + 300

        shape_list = [shape1, shape2, shape3, shape4, shape5, shape6]
        for j in range(6):
            if shape_list[j] > 360:
                shape_list[j] = shape_list[j] - 360

        np.random.shuffle(shape_list)
        shape_1_index = shape_list[0]
        shape_2_index = shape_list[1]
        shape_3_index = shape_list[2]
         
        # column 4 and 5: indices of colour 1 and 2
        sample_colour = randint(1, 181)
        colour1 = sample_colour 
        colour2 = sample_colour + 30
        colour3 = sample_colour + 60
        colour4 = sample_colour + 90
        colour5 = sample_colour + 120
        colour6 = sample_colour + 150

        colour_list = [colour1, colour2, colour3, colour4, colour5, colour6]
        for j in range(6):
            if colour_list[j] > 180:
                colour_list[j] = colour_list[j] - 180
        
        colour_1_index = colour_list[0]
        colour_2_index = colour_list[1]
        colour_3_index = colour_list[2]

        # column 6 and 7: study shape and study colour
        '''
        if conditions[i] == 1:
            study_shape = shape_1_index
            study_colour = colour_1_index
        elif conditions[i] == 2:
            study_shape = shape_2_index
            study_colour = colour_2_index
        elif conditions[i] == 3:
            study_shape = shape_3_index
            study_colour = colour_3_index
        '''
        # for this experiment, shape 1 is always the study shape (since they are randomized, so no diff)
        study_shape = shape_1_index
        study_colour = colour_1_index

        # shape jitter
        shape_jitter = rand_jitter

        # colour jitter
        colour_jitter = randint(1, 181)

        # determine the positions of shapes. the given bounds are determined so that the shapes never intersect with the background image
        # and so that they never intersect each other

        pos1 = (0, 0)
        pos2 = (0, 0)
        pos3 = (0, 0)

        while True:
            pos1 = (randint(-420, 420), randint(-420, 420))
            if (-420 <= pos1[1] <= -386 or 385 <= pos1[1] <= 419 or -420 <= pos1[0] <= -386 or 385 <= pos1[0] <= 419):
                break
        
        while True:
            pos2 = (randint(-420, 420), randint(-420, 420))
            if (distance(pos1, pos2) >= 312 and (-420 <= pos2[1] <= -386 or 385 <= pos2[1] <= 419 or -420 <= pos2[0] <= -386 or 385 <= pos2[0] <= 419)):
                break
        
        while True:
            pos3 = (randint(-420, 420), randint(-420, 420))
            if (distance(pos1, pos3) >= 312 and distance(pos2, pos3) >= 312 and (-420 <= pos3[1] <= -386 or 385 <= pos3[1] <= 419 or -420 <= pos3[0] <= -386 or 385 <= pos3[0] <= 419)):
                break
        
        trial_info.append({'condition':conditions[i], 'shape_1':shape_1_index, \
        'shape_2':shape_2_index, 'shape_3':shape_3_index, 'colour_1':colour_1_index, 'colour_2':colour_2_index, \
        'colour_3':colour_3_index, 'pos_1':pos1, 'pos_2':pos2, 'pos_3':pos3, 'study_shape':study_shape,\
        'study_colour':study_colour, 'shape_jitter':shape_jitter, \
        'colour_jitter':colour_jitter})

    return trial_info


# replaces the mask colour in a given study_image with the colour indexed by ZL_colour in ZL_colors
# study_image param should be a 3D numpy array of the image data, and 1 <= ZL_colour <= 180
# returns another 3D numpy array
def replace_mask_colour (study_image, ZL_colour):
    ZL_file = scipy.io.loadmat('ZL_colors.mat') # load the ZL_colors file

    # access the RGB fields:
    ZL_red = ZL_file['ZL_colors'][0][0][0][0][int(ZL_colour - 1)]
    ZL_green = ZL_file['ZL_colors'][0][0][1][0][int(ZL_colour - 1)]
    ZL_blue = ZL_file['ZL_colors'][0][0][2][0][int(ZL_colour - 1)]

    # specify the mask colors to be replaced
    colour_file_data = get_image_array('stimuli\\shapecolourv4_colour.jpg')
    
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

# returns a list of outer shapes STIMS (psychopy.visual.ImageStim) that surround the colour circle; num_of_shapes indicates how many,
# and outer_shape_size is their size in pixels
def make_outer_shapes(win, trial_handler, pos1, num_of_shapes=8, outer_shape_size=50, loc_radius=150, dist_from_outer_radius=75):
    # get the angles for the outer shapes
    equidistant_angle = 360 / num_of_shapes 
    outer_shapes = []
    for i in range(num_of_shapes):
        outer_shapes.append(i * equidistant_angle)

    # create stims
    shape_stims = []
    for shape in outer_shapes:
        jittered_shape = shape + trial_handler.thisTrial['shape_jitter'] # this is the shape jitter value for the current trial
        if jittered_shape > 360:
            jittered_shape = jittered_shape - 360
        
        shape_image = Image.open("stimuli\\v4shape_{0}.jpg".format((int(jittered_shape))))
        shape_image = shape_image.filter(ImageFilter.BLUR)
        shape_stim = visual.ImageStim(win, shape_image, None, 'pix', (pos1[0], pos1[1]), outer_shape_size) # note: position not yet set
        shape_stims.append(shape_stim)

    # position stims
    diagonal_coord = (loc_radius + dist_from_outer_radius) * sin(pi/4) # the x and y-coord of the diagonal shapes
    shape_stims[1].pos = (diagonal_coord, diagonal_coord)
    shape_stims[2].pos = (0, loc_radius + 75)
    shape_stims[3].pos = (-diagonal_coord, diagonal_coord)
    shape_stims[4].pos = (-loc_radius - 75, 0)
    shape_stims[5].pos = (-diagonal_coord, -diagonal_coord)
    shape_stims[6].pos = (0, -loc_radius - 75)
    shape_stims[7].pos = (diagonal_coord, -diagonal_coord)
    shape_stims[0].pos = (loc_radius + 75, 0)

    return shape_stims

# takes a positional coordinate and determines which 'sector' it falls under dividing the screen like this:
#          left_sector_x   right_sector_x
    ###################################################
    #                #               #                #
    #                #               #                #
    #       1        #       2       #        3       #
    #                #               #                #
    #                #               #                #
    ###################################################
    #                #               #                #
    #                #               #                #
    #       4        #       5       #        6       #
    #                #               #                #
    #                #               #                #
    ###################################################
def get_sector (width, pos):
    left_sector_x = -int(round(width / 6)) # marks the left 1/3 of the screen
    right_sector_x = int(round(width / 6)) # marks the right 1/3 of the screen

    if (pos[1] >= 0): # if in sector 1, 2, or 3
        if (pos[0] <= left_sector_x):
            return 1
        elif (pos[0] > left_sector_x and pos[0] <= right_sector_x):
            return 2
        elif (pos[0] > right_sector_x):
            return 3
    elif (pos[1] < 0): # if in sector 4, 5, or 6
        if (pos[0] <= left_sector_x):
            return 4
        elif (pos[0] > left_sector_x and pos[0] <= right_sector_x):
            return 5
        elif (pos[0] > right_sector_x):
            return 6

# class used to transfer files to dropbox
class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

# uploads all of the contents of the data folder to a dropbox
def upload_dropbox(participant_id):
    data_path = os.path.dirname(os.path.realpath(__file__)) + "\\data"
    access_token = '' # Dropbox OAuth2 token goes here
    transferData = TransferData(access_token)

    for path in os.listdir(data_path):
        file_from = data_path + "\\" + path
        file_to = "/" + str(participant_id) + "/" + path  # The full path to upload the file to, including the file name
        transferData.upload_file(file_from, file_to)
        print ("logged to dropbox: " + path)
        
# uploads all of the contents of the data folder to the specified http server
def upload_http(participant_id):
    data_path = os.path.dirname(os.path.realpath(__file__)) + "\\data" # access data folder
    random.seed(datetime.now())
    id_randomizer = random.randint(1, 1000000)

    for path in os.listdir(data_path): # for each filename in the data folder
        full_file_path = data_path + "\\" + path
        
        path_names = path.split('.') # ['filename', '.ext']
        file_name = path_names[0]
        filetype = path_names[1]

        site = "localhost:8000/uploadresponse?title={0}&path={1}&filetype={2}".format(file_name, participant_id + "_" + str(id_randomizer), filetype) # name, path, extension
        data = ""

        with open(full_file_path, 'rb') as file:
            data = file.read()  

        r = requests.post(url = site, data = data)
        print(r.text)
