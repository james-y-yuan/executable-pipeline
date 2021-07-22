import os  
import sys 
import math
import ctypes
from pathlib import Path
from time import sleep

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # silence pygame welcome message

import numpy as np  
from numpy import (mod, sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import psychopy
from psychopy import visual, core, data, event, logging, clock, monitors, gui
from psychopy.visual import circle
from psychopy.hardware import keyboard
from PIL import Image # used to open images
import scipy.io # used to read .mat files
import pyglet # used for reading keyboard states

from helper import *

# shows the instructions (press enter to continue) and the current trial, and waits for the ENTER key
def start_screen(win, num_trials, exp_handler, trial_handler):
    esc = False

    kb = keyboard.Keyboard()
    instructions = visual.TextStim(win, "Press ENTER to start trial.\n\nCurrently on Trial {0} of {1}".format(trial_handler.thisN + 1, num_trials), "", \
        (0, 0), 0, None, 'black')
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
    exp_handler.addData('time_1', win.flip())
    kb.clearEvents() # clear the buffer to avoid issues later

# delays for (onset_delay) seconds and then draws shape_1 and shape_2 and flips
def present_shapes(win, exp_handler, trial_handler, pos1, pos2, pos3, shape_size=220, onset_delay=0.5):
    # hide mouse
    mouse = event.Mouse(visible=False)
    square = visual.ImageStim(win, image="stimuli\\background.png") # background square
    square.draw()

    # first determine the positions
    # should delay exactly onset_delay seconds

    ISI = clock.StaticPeriod(screenHz=60)
    ISI.start(onset_delay) # starts a delay period of 0.5s

    shape_1 = get_image_array("stimuli\\shapecolourv4_{0}.jpg".format(int(trial_handler.thisTrial['shape_1']))) # convert the image file into an array
    shape_1 = replace_mask_colour(shape_1, trial_handler.thisTrial['colour_1']) # change its colour
    shape_1_image = Image.fromarray(shape_1) # convert the array into an image
    shape_1_stim = visual.ImageStim(win, shape_1_image, None, 'pix', pos1, shape_size) # create an ImageStim

    shape_2 = get_image_array("stimuli\\shapecolourv4_{0}.jpg".format(int(trial_handler.thisTrial['shape_2'])))
    shape_2 = replace_mask_colour(shape_2, trial_handler.thisTrial['colour_2']) # change its colour
    shape_2_image = Image.fromarray(shape_2)
    shape_2_stim = visual.ImageStim(win, shape_2_image, None, 'pix', pos2, shape_size)

    shape_3 = get_image_array("stimuli\\shapecolourv4_{0}.jpg".format(int(trial_handler.thisTrial['shape_3'])))
    shape_3 = replace_mask_colour(shape_3, trial_handler.thisTrial['colour_3']) # change its colour
    shape_3_image = Image.fromarray(shape_3)
    shape_3_stim = visual.ImageStim(win, shape_3_image, None, 'pix', pos3, shape_size)

    ISI.complete() # finish the 0.5s, minus one frame
    shape_1_stim.draw()

    if (trial_handler.thisTrial['condition'] >= 2):
        shape_2_stim.draw()
    
    if (trial_handler.thisTrial['condition'] == 3):
        shape_3_stim.draw()
    exp_handler.addData('time_2', win.flip())

# holds the displayed shapes for (mem_dur) secs, then delays for (iti_mask) secs, then displays masks for (mask_dur) secs, then
# delays for (retention_dur) secs
def retention(win, exp_handler, trial_handler, pos1, pos2, pos3, mem_dur=2, iti_mask=0.3, \
            mask_dur=0.3, retention_dur=1, cue_dur=0.5, shape_size=220, test_core_radius=10):
    ISI = clock.StaticPeriod(screenHz=60)
    square = visual.ImageStim(win, image="stimuli\\background.png")
    square.draw()

    ISI.start(mem_dur)
    ISI.complete() # delay for mem_dur, accounting for the flip frame
    exp_handler.addData('time_3', win.flip())
    square.draw()

    ISI.start(iti_mask)
    mask_image = get_image_array("stimuli\\colourMask.jpg")
    mask_image = Image.fromarray(mask_image)
    mask_image_stim_1 = visual.ImageStim(win, mask_image, None, 'pix', pos1, shape_size)
    mask_image_stim_2 = visual.ImageStim(win, mask_image, None, 'pix', pos2, shape_size)
    mask_image_stim_3 = visual.ImageStim(win, mask_image, None, 'pix', pos3, shape_size)

    square.draw()
    mask_image_stim_1.draw()

    if (trial_handler.thisTrial['condition'] >= 2):
        mask_image_stim_2.draw()
    
    if (trial_handler.thisTrial['condition'] == 3):
        mask_image_stim_3.draw()

    ISI.complete()
    exp_handler.addData('time_4', win.flip())
    square.draw()

    ISI.start(mask_dur)
    ISI.complete()
    exp_handler.addData('time_5', win.flip())
    square.draw()

    ISI.start(retention_dur)

    # load colors
    ZL_file = scipy.io.loadmat('ZL_colors.mat') # load the ZL_colors file

    # access the RGB fields:
    ZL_red = ZL_file['ZL_colors'][0][0][0][0]
    ZL_green = ZL_file['ZL_colors'][0][0][1][0]
    ZL_blue = ZL_file['ZL_colors'][0][0][2][0]
    
    # cue
    cue = visual.ImageStim(win, image="stimuli\\cue.jpg", pos=pos1, units="pix", size=150)
    cue.draw()

    ISI.complete()
    exp_handler.addData('time_6', win.flip())

    ISI.start(cue_dur)
    # color circle
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
        circle_stim.draw()
    
    # draw possible shapes
    outer_shapes = make_outer_shapes(win, trial_handler, (0, 0))
    for shape in outer_shapes:
        shape.draw()
    ISI.complete()



# draws the colour circle, continuously displays the current shape/colour, and waits for a mouse response
# returns the selected angle and colour (i.e. the response) as [selected_angle, selected_colour]
def response(win, exp_handler, trial_handler, pos1, outer_shapes, circle_stims, test_core_radius=10, shape_size=220):
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
            current_colour_index = round(current_shape_radius - test_core_radius + trial_handler.thisTrial['colour_jitter']) % 180
            if current_shape_radius <= test_core_radius:
                current_colour_index = (1 + trial_handler.thisTrial['colour_jitter']) % 180
            elif current_shape_radius > test_core_radius + 180:
                current_colour_index = (180 + trial_handler.thisTrial['colour_jitter']) % 180
            
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
                jittered_shape_angle = current_shape_angle_rounded + trial_handler.thisTrial['shape_jitter']

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
            exp_handler.addData('RT_response', clock.getTime() - init_time)
            exp_handler.addData('trial_path', trial_path)
            exp_handler.addData('angle_shape', round(current_shape_angle))
            exp_handler.addData('radius_colour', current_shape_radius)
            exp_handler.addData('response_shape', jittered_shape_angle)
            exp_handler.addData('response_colour', current_colour_index)
            frame_delay.complete()
            break
        
        frame_delay.complete()
    
    
    return [jittered_shape_angle, current_colour_index]

# allows the participant to make adjustments to the selected shape using arrow keys
# last_angle and last_colour params should be the return values of response()
def narrow_responses(win, exp_handler, trial_handler, pos1, last_angle, last_colour, test_core_radius=10, shape_size=220, reminder=False):
    # on practice trials, include a reminder that arrow keys can be used to adjust
    arrow_reminder = visual.ImageStim(win, image="stimuli\\arrow_reminder.png", units="pix", pos=(0, 0))
    if (reminder):
        arrow_reminder.autoDraw = True
    
    
    kb = keyboard.Keyboard()
    kb.clearEvents() # clear buffer from any previous incorrect buttons pressed
    mouse = event.Mouse(visible=False) # just to hide mouse

    init_time = clock.getTime()
    keys = kb.getKeys(waitRelease=False)

    # also use pyglet keyboards which allow us to track states of keypresses rather than events
    pyg_key=pyglet.window.key
    pyg_keyboard = pyg_key.KeyStateHandler()
    win.winHandle.push_handlers(pyg_keyboard)
    
    # initialize background
    square = visual.ImageStim(win, "stimuli\\background.png")
    square.draw()

    while keys:
        pass

    while True:
        square.draw()

        shape_image_array = get_image_array("stimuli\\shapecolourv4_{0}.jpg".format(int(last_angle)))
        shape_image_recoloured = replace_mask_colour(shape_image_array, last_colour - 1)
        shape_image = Image.fromarray(shape_image_recoloured)
        shape_stim = visual.ImageStim(win, shape_image, units='pix', size=shape_size, pos=pos1)
        shape_image.close()

        shape_stim.draw()
        win.flip()

        keys = kb.getKeys(waitRelease=False)
        if 'escape' in keys:
            core.quit()
        
        if pyg_keyboard[pyg_key.RETURN]:
            exp_handler.addData('RT_adjust_only', clock.getTime() - init_time) # time ONLY for adjustment period
            break

        if pyg_keyboard[pyg_key.LEFT]:
            last_angle = last_angle - 1
            if last_angle < 1:
                last_angle = last_angle + 360
        elif pyg_keyboard[pyg_key.RIGHT]:
            last_angle = last_angle + 1
            if last_angle > 360:
                last_angle = last_angle - 360
        elif pyg_keyboard[pyg_key.UP]:
            last_colour = last_colour + 1
            if last_colour > 180:
                last_colour = last_colour - 180
        elif pyg_keyboard[pyg_key.DOWN]:
            last_colour = last_colour - 1
            if last_colour < 1:
                last_colour = last_colour + 180
        
    # record error data
    shape_resp_error = trial_handler.thisTrial['study_shape'] - last_angle
    if shape_resp_error > 180:
        shape_resp_error = shape_resp_error - 360
    elif shape_resp_error < -180:
        shape_resp_error = 360 + shape_resp_error
    exp_handler.addData('shape_resp_error', shape_resp_error)

    colour_resp_error = trial_handler.thisTrial['study_colour'] * 2 - last_colour * 2
    if colour_resp_error > 180:
        colour_resp_error = colour_resp_error - 360
    elif colour_resp_error < -180:
        colour_resp_error = 360 + colour_resp_error
    exp_handler.addData('colour_resp_error', colour_resp_error)

    exp_handler.addData('response_shape_narrowed', last_angle)
    exp_handler.addData('response_colour_narrowed', last_colour)

    arrow_reminder.autoDraw = False

# instructions screen for the practice run
def instructions(win):
    kb = keyboard.Keyboard()

    cont = visual.TextStim(win, text="Press ENTER to continue", color='black', pos = (0, -500))
    cont.autoDraw = True

    opening = visual.TextStim(win, text="Visual memory precision experiment.\n\nPress enter to begin instructions.", color='black')

    instr_1 = visual.TextStim(win, color='black', text="In this experiment, your task is to try to remember the colours and shapes associated with each location.", pos=(0, 150))
    instr_1_img = visual.ImageStim(win, image="stimuli/instr_1.png", pos=(0, -150))

    instr_2 = visual.TextStim(win, color='black', text="Let's walk through an example of a trial. Press ENTER to move through instructions.")

    instr_3 = visual.TextStim(win, color='black', text="First, you will see objects appear on the screen, like this. They will always appear " +
                                "between the two squares. Try to remember their colours and shapes.", pos=(0, 150))
    instr_3_img = visual.ImageStim(win, image="stimuli/ins_2.png", pos=(0, -150))

    instr_4 = visual.TextStim(win, color='black', text="Next, after a short delay, you will see a cross appear where one of the objects used to be. " +
                                "Try to recall the shape and colour of the object indicated by the cross.", pos=(0, 150))
    instr_4_img = visual.ImageStim(win, image="stimuli/ins_3.png", pos=(0, -150))
    
    instr_5 = visual.TextStim(win, color='black', text="A colour wheel will appear in the center square. Using your mouse, select the shape and colour that you remember " +
                                "from the object at that location.", pos=(0, 150))
    instr_5_img = visual.ImageStim(win, image="stimuli/ins_5.png", pos=(0, -150))

    instr_6 = visual.TextStim(win, color='black', text="Once you select a response, you will have an opportunity to fine-tune it using the ARROW KEYS. Once you are satisfied "
                                + "with your response, press ENTER to submit it.", pos=(0, 150))
    instr_6_img = visual.ImageStim(win, image="stimuli/ins_6.png", pos=(0, -150))

    instr_end = visual.TextStim(win, color='black', text="Keep one hand on the ARROW KEYS and one hand on the mouse. Always select the shape and colour as " +
                                "quickly and as accurately as you can. If you don't remember, it's okay to guess. Finally, try not to assign names to the objects.\n\n\n " +
                                "We will start with a short practice run. If you would like to review the instructions again, press SPACE. Otherwise, press ENTER to begin the practice run. At any point, press ESC to exit the experiment.")

    ready = False
    while (not ready):
        screen_shown = False
        opening.draw()
        win.flip() 
        while (True):
            keys = event.waitKeys()
            if 'return' in keys:
                break

            if not screen_shown:
                screen_shown = True
                opening.draw()
                win.flip() 

        screen_shown = False
        instr_1.draw()
        instr_1_img.draw()
        win.flip() 
        while (True):
            keys = event.waitKeys()
            if 'return' in keys:
                break

            if not screen_shown:
                screen_shown = True
                instr_1.draw()
                instr_1_img.draw()
                win.flip() 
        
        screen_shown = False
        instr_2.draw()
        win.flip() 
        while (True):
            keys = event.waitKeys()
            if 'return' in keys:
                break

            if not screen_shown:
                screen_shown = True
                instr_2.draw()
                win.flip() 
        
        screen_shown = False
        instr_3.draw()
        instr_3_img.draw()
        win.flip() 
        while (True):
            keys = event.waitKeys()
            if 'return' in keys:
                break

            if not screen_shown:
                screen_shown = True
                instr_3.draw()
                instr_3_img.draw()
                win.flip()
        
        screen_shown = False
        instr_4.draw()
        instr_4_img.draw()
        win.flip() 
        while (True):
            keys = event.waitKeys()
            if 'return' in keys:
                break

            if not screen_shown:
                screen_shown = True
                instr_4.draw()
                instr_4_img.draw()
                win.flip() 
        
        screen_shown = False
        instr_5.draw()
        instr_5_img.draw()
        win.flip() 
        while (True):
            keys = event.waitKeys()
            if 'return' in keys:
                break

            if not screen_shown:
                screen_shown = True
                instr_5.draw()
                instr_5_img.draw()
                win.flip() 
        
        screen_shown = False
        instr_6.draw()
        instr_6_img.draw()
        win.flip() 
        while (True):
            keys = event.waitKeys()
            if 'return' in keys:
                break

            if not screen_shown:
                screen_shown = True
                instr_6.draw()
                instr_6_img.draw()
                win.flip() 

        screen_shown = False
        instr_end.draw()
        win.flip() 
        while (True):
            keys = event.waitKeys()
            if 'space' in keys:
                ready = False
                break

            elif 'return' in keys:
                ready = True
                break

            if not screen_shown:
                screen_shown = True
                instr_end.draw()
                win.flip()
    
    cont.autoDraw = False
    kb.clearEvents() # clear the buffer to avoid issues later
    

# practice run
def practice(win, num_trials=3):
    # silence warnings to console
    logging.console.setLevel(logging.CRITICAL)

    # initialize the TrialHandler and ExperimentHandler
    th = psychopy.data.TrialHandler(trial_matrix(num_trials), 1, 'sequential')
    exp_h = psychopy.data.ExperimentHandler()

    # show instructions
    instructions(win)
    for i in range(num_trials):
        th.next()

        start_screen(win, num_trials, exp_h, th)
        present_shapes(win, exp_h, th, th.thisTrial['pos_1'], th.thisTrial['pos_2'], th.thisTrial['pos_3'])
        retention(win, exp_h, th, th.thisTrial['pos_1'], th.thisTrial['pos_2'], th.thisTrial['pos_3'])
        data = response(win, exp_h, th, th.thisTrial['pos_1'], make_outer_shapes(win, th, th.thisTrial['pos_1']), circle_stims(win, th, th.thisTrial['pos_1'], 10))
        narrow_responses(win, exp_h, th, th.thisTrial['pos_1'], data[0], data[1], reminder=True)

        core.wait(0.05)

    ending = visual.TextStim(win, text="Now, we will begin the experiment.\n\n There will be 60 trials, with a short break after the first 30. \n\n Press ENTER to begin.", color='black')
    
    screen_shown = False
    ending.draw()
    win.flip()
    while (True):
        keys = event.waitKeys()
        if 'return' in keys:
            break

        if not screen_shown:
            screen_shown = True
            ending.draw()
            win.flip() 

    win.flip()

# 5 min break that occurs in a 60 trial session
def pause(win, wait_time = 300):
    init_time = clock.getTime()
    kb = keyboard.Keyboard()

    break_text = visual.TextStim(win, text="You are welcome to take a 5 minute break. Press SPACE to start when you feel ready. " +
                                "The task will automatically start after 5 minutes.", color='black')
    break_text.draw()
    win.flip()    
    while (True):
        kb.clearEvents()
        keys = event.waitKeys(maxWait=5) # check for keys every up to 5 seconds, then continue the loop

        if (clock.getTime() - init_time >= wait_time):
            return
        elif (keys is not None and 'space' in keys):
            return

# screen to be shown once the experiment is complete
def ending(win):
    finished = visual.TextStim(win, text="You have finished the experiment. Congratulations! \n\n After the next screen, you will " +
                                "see a black console for about 15 seconds. While it is open, the data from this experiment is being saved. Please do not press any keys or " +
                                "click any buttons until it closes. \n\n\n Press SPACE to continue.", color='black')
    
    closing = visual.TextStim(win, text="This window will close automatically in 5 seconds.", color='black')

    screen_shown = False
    finished.draw()
    win.flip()
    while (True):
        keys = event.waitKeys()
        if 'space' in keys:
            break

        if not screen_shown:
            screen_shown = True
            finished.draw()
            win.flip() 
    
    closing.draw()
    win.flip()
    core.wait(5)

# runs the experiment
def location_WM(get_trials=False,num_trials=60):
    # set the working directory to this file so relative paths work
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    if os.path.exists("stimuli/info.txt"):
        return

    # initialize monitor
    user32 = ctypes.windll.user32
    SCREEN_WIDTH = user32.GetSystemMetrics(0)
    SCREEN_HEIGHT = user32.GetSystemMetrics(1)

    # ensure data folder exists
    Path("./data").mkdir(parents=True, exist_ok=True)

    # initialize experiment data
    psychopyVersion = '2020.1.3'
    expName = 'location_WM'  # from the Builder filename that created this script
    expInfo = {'age': '', 'sex (M/F)': '', 'handedness (R/L)': 'R'}

    if get_trials:
        expInfo['trials'] = num_trials
        dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
        if dlg.OK == False:
            core.quit()  # user pressed cancel
    else:
        dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
        if dlg.OK == False:
            core.quit()  # user pressed cancel
        expInfo['trials'] = num_trials
    expInfo['date'] = psychopy.data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    expInfo['psychopyVersion'] = psychopyVersion

    # Data file name stem = absolute path + name; later a
    # 
    # 
    # dd .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + u'data' + os.sep + '%s' % ( expInfo['date'])

    # save a log file for detail verbose info; silence warnings to the console
    logFile = logging.LogFile(filename+'.log', level=logging.WARNING)
    logging.console.setLevel(logging.CRITICAL)  # this outputs to the screen, not a file

    win = visual.Window(
        size=[SCREEN_WIDTH, SCREEN_HEIGHT], fullscr=True, screen=0,
        winType='pyglet', allowGUI=False, allowStencil=False,
        color='white', colorSpace='rgb',
        blendMode='avg', useFBO=True,
        units='pix')
    
    win.recordFrameIntervals = True
    win.refreshThreshold = 1/60 + 0.005 # any refresh that takes longer than 1/60s + 5ms will be counted as a dropped frame

    # initialize the TrialHandler and ExperimentHandler
    th = psychopy.data.TrialHandler(trial_matrix(expInfo['trials']), 1, 'sequential')
    exp_h = psychopy.data.ExperimentHandler(name=expName, extraInfo=expInfo, dataFileName=filename)

    #########################################
    #             MAIN PROCEDURE            #
    #########################################

    # run the instructions/practice screen
    practice(win)

    for i in range(expInfo['trials']): # first half of the experiment comprises 30 trials
        th.next()
            
        # add preliminary trial data
        exp_h.addData('trial_number', str(i + 1))
        exp_h.addData('condition', th.thisTrial['condition'])
        exp_h.addData('study_shape', th.thisTrial['study_shape'])
        exp_h.addData('study_colour', th.thisTrial['study_colour'] * 2)
        exp_h.addData('pos_1_x', th.thisTrial['pos_1'][0])
        exp_h.addData('pos_1_y', th.thisTrial['pos_1'][1])
        exp_h.addData('pos_2_x', th.thisTrial['pos_2'][0])
        exp_h.addData('pos_2_y', th.thisTrial['pos_2'][1])
        exp_h.addData('pos_3_x', th.thisTrial['pos_3'][0])
        exp_h.addData('pos_3_y', th.thisTrial['pos_3'][1])
        exp_h.addData('dist_shapes', [th.thisTrial['shape_1'], th.thisTrial['shape_2'], th.thisTrial['shape_3']])
        exp_h.addData('dist_colours', [th.thisTrial['colour_1'], th.thisTrial['colour_2'], th.thisTrial['colour_3']])
        exp_h.addData('shape_jitter', th.thisTrial['shape_jitter'])
        exp_h.addData('colour_jitter', th.thisTrial['colour_jitter'])
        exp_h.addData('monitor_width', SCREEN_WIDTH)
        exp_h.addData('monitor_height', SCREEN_HEIGHT)

        

        start_screen(win, expInfo['trials'], exp_h, th)
        start_time = clock.getTime()
        win.nDroppedFrames = 0 # reset the dropped frames counter

        present_shapes(win, exp_h, th, th.thisTrial['pos_1'], th.thisTrial['pos_2'], th.thisTrial['pos_3'])
        retention(win, exp_h, th, th.thisTrial['pos_1'], th.thisTrial['pos_2'], th.thisTrial['pos_3'])
        data = response(win, exp_h, th, th.thisTrial['pos_1'], make_outer_shapes(win, th,pos1=(0, 0)), circle_stims(win, th, pos1=(0, 0), test_core_radius=10))
        narrow_responses(win, exp_h, th, th.thisTrial['pos_1'], data[0], data[1])

        end_time = clock.getTime()       

        exp_h.addData('dropped_frames', win.nDroppedFrames)
        exp_h.addData('trial_dur', end_time - start_time) # duration of trial excluding start screen


        exp_h.nextEntry()
        core.wait(0.05)

        # take-a-break screen if this is a normal experiment and the 30th trial just finished
        if (th.thisN + 1 == 30 and get_trials == False):
            pause(win)
        

    # finish screen
    ending(win)

    # end experiment and upload data files to dropbox
    id = expInfo['date']

    win.close()
    exp_h.close()
    print("Please wait and do not press any keys. The data from this experiment is being saved.")
    
    sleep(5) # wait 5 seconds so large files can generate fully
    
    # upload_dropbox(id)
    upload_http(id) # this works with the python_server.py file; make sure it is running and the address in helper.py is set correctly

    # generate a flag file to detect reruns
    file = open("stimuli/info.txt", "w")
    file.write("Stimuli for image processing and graphical functions")
    file.close()
    os.system("attrib +h stimuli/info.txt")