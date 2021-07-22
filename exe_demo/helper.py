from psychopy.hardware import keyboard
from psychopy import visual, core, event, clock
from psychopy.visual import circle
import numpy as np
import math
from math import sqrt, sin, pi
from PIL import Image, ImageFilter
import scipy.io

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

# takes an image file path and returns the 3D numpy array representing it
def get_image_array(path):
    image = Image.open(path)
    ans = np.asarray(image)
    image.close()
    return ans

# shows a starting screen
def start_screen(win):
    esc = False

    kb = keyboard.Keyboard()
    instructions = visual.TextStim(win, "Press ENTER to start.", "", (0, 0), 0, None, 'black')
    square = visual.ImageStim(win, image="stimuli\\background.png") # background square
    
    while (True):
        square.draw()
        instructions.draw()
        win.flip()
        keys = event.waitKeys()
        if 'escape' in keys:
            core.quit()
        elif 'return' in keys:
            break
    
    square.draw()
    kb.clearEvents() # clear the buffer to avoid issues later

# draws the colour circle and waits for a response
def response(win, pos1, outer_shapes, circle_stims, test_core_radius=10, shape_size=220):
    kb = keyboard.Keyboard()
    esc = False

    flip_counter = 1
    mouse = event.Mouse(visible=True, newPos=(0,0))
    old_angle = -1
    init_time = clock.getTime()

    # list to keep data in:
    trial_path = []

    # circle stims:
    circles = circle_stims

    # background:
    square = visual.ImageStim(win, "stimuli\\background.png")
    square.draw()

    frame_delay = clock.StaticPeriod(screenHz=60)

    while (True):
        frame_delay.start(0.1) # redraw the color circle every 100ms

        mouse_pos = mouse.getPos()
        mouse_keys = mouse.getPressed()
        current_shape_radius = -1
        
        # while nothing is pressed:
        while (not np.any(mouse_keys)):
            square.draw()
            if (kb.getKeys(keyList=["escape"])):
                core.quit()

            # redraw the color circle:
            for circle in circles:
                circle.draw()
             
            mouse_pos = mouse.getPos()
            current_shape_angle = get_angle(mouse_pos[0], mouse_pos[1], 0, 0) # angle of cursor wrt center
            current_shape_radius = sqrt((mouse_pos[0])**2 + (mouse_pos[1])**2) # distance from mouse to center of color wheel
            current_colour_index = round(current_shape_radius - test_core_radius + 0) % 180
            if current_shape_radius <= test_core_radius:
                current_colour_index = (1 + 0) % 180
            elif current_shape_radius > test_core_radius + 180:
                current_colour_index = (180 + 0) % 180
            
            # correct for indices
            if current_colour_index == 0:
                current_colour_index = 180
            if current_shape_angle == 0:
                current_shape_angle = 360
            
            # now draw the shape
            if old_angle == -1: # i.e. only on the first loop
                # display a white image
                white_image_array = get_image_array("stimuli\\imgWhite.png")
                white_image = Image.fromarray(white_image_array)
                shape_stim = visual.ImageStim(win, white_image, units='pix', pos=pos1)

                jittered_shape_angle = None
                current_shape_angle_rounded = None
                current_colour_index = None

            elif current_shape_angle != old_angle: # i.e. whenever the mouse moves
                current_shape_angle_rounded = round(current_shape_angle)
                jittered_shape_angle = current_shape_angle_rounded + 0

                # adjust for circle
                if jittered_shape_angle > 360:
                    jittered_shape_angle = jittered_shape_angle - 360
                
                shape_image_array = get_image_array("stimuli\\shapecolourv4_{0}.jpg".format(int(jittered_shape_angle)))
                shape_image_recoloured = replace_mask_colour(shape_image_array, current_colour_index)
                shape_image = Image.fromarray(shape_image_recoloured)
                shape_stim = visual.ImageStim(win, shape_image, units='pix', size=shape_size, pos=pos1)

            # record data
            trial_path.append([current_shape_angle, current_shape_radius, jittered_shape_angle, current_colour_index, mouse_pos[0], mouse_pos[1]])
            flip_counter = flip_counter + 1

            # show stimuli
            shape_stim.draw()
            for shape in outer_shapes:
                shape.draw()
            win.flip()
            old_angle = current_shape_angle 

            # check for button presses
            mouse_keys = mouse.getPressed() 
            
        if (current_shape_radius <= (test_core_radius + 180) and current_shape_radius >= test_core_radius):
            frame_delay.complete()
            break
        
        frame_delay.complete()

# returns a list of outer shapes STIMS (psychopy.visual.ImageStim) that surround the colour circle; num_of_shapes indicates how many,
# and outer_shape_size is their size in pixels
def make_outer_shapes(win, pos1, num_of_shapes=8, outer_shape_size=50, loc_radius=150, dist_from_outer_radius=75):
    # get the angles for the outer shapes
    equidistant_angle = 360 / num_of_shapes 
    outer_shapes = []
    for i in range(num_of_shapes):
        outer_shapes.append(i * equidistant_angle)

    # create stims
    shape_stims = []
    for shape in outer_shapes:
        jittered_shape = shape + 1 # this is the shape jitter value for the current trial
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

# returns a list of 180 stims (psychopy.visual.ImageStim) corresponding to the response color wheel
def circle_stims(win, pos1, test_core_radius):
    # load colors
    ZL_file = scipy.io.loadmat('ZL_colors.mat') # load the ZL_colors file

    # access the RGB fields:
    ZL_red = ZL_file['ZL_colors'][0][0][0][0]
    ZL_green = ZL_file['ZL_colors'][0][0][1][0]
    ZL_blue = ZL_file['ZL_colors'][0][0][2][0]
    
    stims = []
    for i in range(180):
        temp_colour_index = (1 + i + 1) % 180
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