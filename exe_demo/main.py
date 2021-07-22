from helper import *
from psychopy import visual, data
import os

# set current directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# assign location of data files to ./data and name it according to the date and time
filename = _thisDir + os.sep + u'data' + os.sep + '%s' % (data.getDateStr())

# create an ExperimentHandler -- normally this and a TrialHandler would be used
# to manage experiment flow (see PsychoPy docs), but for the purposes of this demo
# this is only created so that a data file is created at the end of the experiment
exp_h = data.ExperimentHandler(dataFileName=filename)

# initialize the window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    color='white', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')

# main experiment code -- in this demo, only shows one starting screen and one shape-conjunction task
start_screen(win)
response(win, (-400, 0), make_outer_shapes(win, pos1=(-400, 0)), circle_stims(win, pos1=(-400, 0), test_core_radius=10))

# add dummy data and saves data file
exp_h.addData('date', data.getDateStr())
exp_h.addData('age', 18)
exp_h.addData('sex', 'M')
exp_h.close()