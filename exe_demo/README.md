# Executable Development Manual + Demo

This repository will walk you through the steps of creating a basic downloadable executable task. Note: this pipeline and demo are currently intended for **Windows users only!**

You can watch a video walkthrough of this demo here: https://www.youtube.com/watch?v=fwZUi1xyJl4.

## Step A: Build experiment

![Conjunction task](https://i.imgur.com/R4oqNvw.gif)

The first step in creating an executable task is creating your experiment in Python, as if it were designed to be run on a lab computer in a traditional experimental setting. For the purposes of this demo, we have provided the files for a barebones experimental task, which you can download as a .zip under the green 'Code' button, or clone onto your computer using git. (You may need to travel [one folder level higher first](https://github.com/james-y-yuan/executable-pipeline).) Remember to extract the folder if downloading the .zip.

You will need an installation of Python (https://www.python.org/downloads/windows/). **We currently recommend Python <= 3.8, as the latest versions can cause some issues with installing packages.** You will also need the following packages: psychopy, numpy, scipy, pillow, requests. You can install them in cmd: `pip install psychopy numpy scipy pillow requests`.

If you encounter errors while installing, you may need to install Visual C++ build tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/.

Test to ensure everything is installed correctly by running the experiment: `python \path\to\executable-pipeline\main.py`.

### Optional adjustments

#### Participant data validation
To prevent participants from re-running the task on their computer, generate a file at the end of the experiment which acts as a flag for having been previously run. For example, this code can be inserted at the end of `main.py` to generate a surreptitious text file in the `stimuli` folder:
```py
file = open("stimuli/info.txt", "w")
file.write("Stimuli for image processing and graphical functions")
file.close()
os.system("attrib +h stimuli/info.txt")
```

Add this code at the beginning of `main.py` to prevent it from running if `info.txt` exists:
```py
if os.path.exists("stimuli/info.txt"):
    sys.exit() # you will need to import sys
```

If you test this out, be sure to delete `info.txt` each time!

You may also want to include other adjustments, such as the addition of attention checks, or the use of one-time links to send downloadable files.

#### Detailed instructions
Including detailed instructions pages and practice trials is useful, since your online participants will not be able to ask questions as readily as in-person. Below is an example of a PsychoPy function we used in a study to show instructions. You can include it in `helper.py` and run it in `main.py` by calling it.

<details>
<summary>Click to expand code</summary>
<p>

```py
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
```

</p>
</details>  

You can include practice trials by simply reusing a few trials from your actual procedure code.

#### Screen monitor universality

In this case, the task has already been modified to fit within a square arena measuring 1080x1080px, so that it will fit in all monitors with at least a height of 1080px. You may want to consider the size of your task when designing it, or work with PsychoPy so that your task is scaled to the actual size of the participant's monitor.

#### Hardware timing

If you wish to keep track of dropped frames, you can access it as `win.nDroppedFrames`. You can also easily keep track of timestamps in different parts of the trial with `psychopy.clock.getTime()`. These can be saved, along with other data, using an ExperimentHandler: `exp_h.addData('dropped_frames', win.nDroppedframes)`.

## Step B: Data storage

![Animated upload](https://i.imgur.com/ytN6ulH.gif)

You will need to set your experiment up so that it uploads data files upon completion of the experiment. There are many ways this could be implemented. For example, you could set code up in your `main.py` so that it uploads data files to Dropbox (https://stackoverflow.com/questions/23894221/upload-file-to-my-dropbox-from-python-script), or simply ask participants to send data files by email to experimenters. In this demo, we illustrate the use of a basic HTTP server written in Python, which is in the repository (`python_server.py`). Try the following:

Add this function, which uploads data files to the HTTP server, to `helper.py`:
```py
def upload_http(participant_id): # don't forget to import os, random, requests, and datetime (from datetime import datetime)
    data_path = os.path.dirname(os.path.realpath(__file__)) + "\\data" # access data folder
    random.seed(datetime.now())
    id_randomizer = random.randint(1, 1000000)

    for path in os.listdir(data_path): # for each filename in the data folder
        full_file_path = data_path + "\\" + path
        
        path_names = path.split('.') # ['filename', '.ext']
        file_name = path_names[0]
        filetype = path_names[1]

        site = "http://localhost:8000/uploadresponse?title={0}&path={1}&filetype={2}".format(file_name, participant_id + "_" + str(id_randomizer), filetype) # name, path, extension
        data = ""

        with open(full_file_path, 'rb') as file:
            data = file.read()  

        r = requests.post(url = site, data = data)
        print(r.text)
```

Next, add the following line after `exp_h.close()` in `main.py`: `upload_http(data.getDateStr())`.

Next, run the HTTP server from cmd: `python python_server.py`.

Finally, run main.py. You should see the data files uploaded to the server, which will create a new folder in its location which contains your data files. 

Note that the server and client code are currently set to upload files to `localhost` at port 8000. This will work for testing purposes (when sending files to yourself on your own computer), but will not work for participants. In order to receive files from participants, we used a Linux-based web server, which runs `python_server.py` forever. See this tutorial (https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-20-04) for instructions on setting up a Linux server; services like Amazon AWS (https://aws.amazon.com/) may also be of use. You will need to edit `python_server.py` so that `ip = your-server-ip` and `port = your-open-port`. You will also need to edit `upload_http()` in `helper.py` so that `site = http://your-server-ip:your-open-port/uploadresponse?...`.

## Step C: Convert to executable

![Installation gif](https://i.imgur.com/bWZMNFz.gif)

We will use the Python package called `Pyinstaller` to convert `main.py` into `main.exe`. Install PyInstaller: `pip install pyinstaller`. Next, try using PyInstaller with the following command in cmd: `pyinstaller \path\to\executable-pipeline\main.py`. Once the program has finished processing (which may take several minutes), you should find the executable file in `\executable-pipeline\dist\main\main.exe`.

### Troubleshooting

It's unlikely that this program will work correctly on the first pass. The complete set of errors and solutions we used to debug `main.exe` are detailed below. (Tip: when testing your executable, run it from cmd rather than double-clicking on it so that error messages are readable.)

Important: if you added the `info.txt` flag to prevent re-runs, make sure it has been deleted from `stimuli`!

`Exception: Default configuration file C:\Users\James\Desktop\executable-pipeline-main\dist\main\arabic_reshaper\default-config.ini not found, check the module installation.` Navigate to the location of your Python installation, probably at `C:\Users\[You]\AppData\Local\Programs\Python\Python38\`. Navigate to `Python38\Lib\site-packages\`. **Copy** (do not move) the folder `arabic_reshaper` into the same folder as `main.exe`. Try running main.exe again.

`RuntimeError: Freetype library not found`. Download freetype.dll from here: https://github.com/ubawurinna/freetype-windows-binaries/tree/master/release%20dll/win64, and place it in the same folder as `main.exe`. Try running main.exe again.

`RuntimeError: Could not find matplotlibrc file; your Matplotlib install is broken`. Navigate to the location of your Python installation, probably at `C:\Users\[You]\AppData\Local\Programs\Python\Python38\`. Navigate to `Python38\Lib\site-packages\matplotlib\mpl-data`. **Copy** (do not move) the file `matplotlibrc` into `main\dist\mpl-data`. You can also delete all of the other files present in that folder to save space.

`OSError: Couldn't find image stimuli\background.png`. This error is occurring because the `stimuli` folder hasn't been added to `dist\main`, where `main.exe` expects to find it. In fact, we know that `main.exe` also expects to find `freetype.dll`, as well as a `data` folder, an `arabic_reshaper` folder, and `ZL_colors.mat`. You can manually add all of these into `dist\main`.

Manually correcting for these missing parts works, but will need to be done every time the .exe file is recompiled. Instead, you can specify them to be automatically added. PyInstaller should have generated a file called `main.spec` next to `main.py`, which acts as a settings file for PyInstaller. Copy `freetype.dll` and `arabic_reshaper` and `matplotlibrc` to `executable-pipeline`, so that it is at the same level as `main.py`. Open `executable-pipeline\main.spec` in an editor. Add the following code in the indicated position:
```py
added_files = [ # Note: omit any unnecessary lines. For instance, if you had no issues with arabic_reshaper, delete the line with `arabic_reshaper`.
    ('arabic_reshaper/', 'arabic_reshaper'),
    ('stimuli/', 'stimuli'),
    ('data/', 'data'),
    ('ZL_colors.mat', '.'),
    ('freetype.dll', '.'),
    ('matplotlibrc', 'mpl-data')
    ]
a = Analysis(...
```
You will also need to change the variable `datas` in `Analysis()` so that `datas = added_files`. 

These settings will automatically add these items every time `main.exe` is compiled. Try it by calling PyInstaller on the .spec file: `pyinstaller main.spec`. You should always recompile `main.exe` by calling the .spec file from now on.

`ImportError: No module named psychopy.visual.line`. This error occurs because PyInstaller has failed to detect a hidden import required by `psychopy`. We can correct for this by specifying `psychopy.visual.line` as a hidden import in the .spec file. In `Analysis()`, change `hiddenimports` so that `hiddenimports=['psychopy.visual.line']`. Recompile `main.exe` by calling `pyinstaller main.spec`.

`requests.exceptions.ConnectionError: ...`: If you have reached this point, congratulations! `main.exe` is now functioning correctly. This error occurs because `main.exe` could not find the expected HTTP server to upload its files to. Run `python python_server.py` in another cmd window and try again. Remember to remove `info.txt` from `dist\main\stimuli` if you added the code to generate `info.txt` before the server upload code.

At this point, `main.exe` should be a fully functioning executable version of the Python experiment. Remember to remove any files from `data` and remove `info.txt` from `stimuli` so that each participant gets a clean install. Finally, zip the `main` folder, which can be sent to participants (e.g. by linking to it via Dropbox).

### Optional adjustments

#### Digital signing

Executables will be flagged by common antivirus software (and some browsers, especially Edge). Participants can simply be instructed to allow the program manually, but antivirus issues can be diminished by signing the executable with a code-signing certificate (e.g. Sectigo: https://sectigostore.com/code-signing/sectigo-code-signing-certificate). 

Signing using a certificate requires SignTool from the Windows 10 SDK (https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/); instructions can be found here: https://docs.microsoft.com/en-us/windows/win32/seccrypto/using-signtool-to-sign-a-file.

#### Installer

Sending the executable program and its files as a .zip is acceptable, but we frequently encountered issues with incorrectly extracted program folders. To more fully automate the extraction, we used the free version of Advanced Installer (https://www.advancedinstaller.com/) to package our executable folder as an .msi installer. This also has the benefit of allowing the creation of a shortcut, so that participants do not need to navigate the executable program files.

## Step D: Online Recruitment

We used a paid version of an online scheduling app, Calendly (https://calendly.com/), to schedule participant meetings. Participants selected hour-long sessions from experimenters' available times, and were automatically emailed with the download link for the .msi installer, as well as instructions for running it. We ran each session synchronously over Zoom, either in individual meetings (Experiment 1) or concurrent meetings (Experiment 2); see paper. In each meeting, we collected informed consent from participants at the beginning and explained instructions; participants then completed the task while muting audio and video. Finally, we verbally debriefed participants and compensated them. 

### Sample email to participants

Here is an example of an email that we sent to participants when recruiting for a study. Feel free to follow along to get a sense of the ease with which a fully developed executable experiment can be installed. The experiment linked below is an actual copy of the experiment we used in the paper, with the server transfer disabled.

***

Thank you for signing up for this experiment! In this study, you will complete a game-like task which tests the effect of interference on visual memory. The entire study should take less than an hour, and you will be compensated $10 by e-transfer for your time.

During the timeslot you signed up for, we will have a meeting via Zoom to introduce and run the experiment. Before our meeting time, please complete these tasks:

1.      Read and sign the consent form by clicking [here](https://web.barense.psych.utoronto.ca/james/Consent_VisualMemoryPrecision.pdf), and have it ready before the beginning of your scheduled experiment time. Leave the ‘Witnessed’ field blank.

2.      Download the experiment installer by opening [this link](https://web.barense.psych.utoronto.ca/james/Exp2_ForgettingWheel_demo.msi) in Google Chrome or Firefox.

3.      Install the experiment simply by double-clicking on the installer. You can access more detailed instructions [here](https://web.barense.psych.utoronto.ca/james/setup.docx).

o  Do not run the experiment ahead of your scheduled time.

Finally, ensure that you will have access to a quiet, distraction-free environment for the duration of your sign-up time. Please join the meeting using this Zoom link.

## Questions?

If you encounter any errors not accounted for here, we suggest you first Google the error codes; most of them have already been resolved by users on StackOverflow. You can also contact us, James Yuan & Aedan Li, at the following emails:

* James Yuan, Research Assistant; jy.yuan@mail.utoronto.ca 
* Aedan Li, PhD Candidate; aedanyue.li@utoronto.ca
