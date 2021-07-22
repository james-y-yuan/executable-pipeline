# Stimulus Generator

This code pre-generates image files for [VCS/CIELAB shape-color objects](https://osf.io/d9gyf/), for use in continuous visual precision experiments. See contents of `generated_stim` for examples. 
* `vcs_stim` and `ZL_colors.mat` are data files used in the code.
* `generate_stims.py` is the main code. You will need the Python packages `pillow`, `numpy`, `scipy`, and `imageio`.
* `generated_stim` contains the pre-generated image files created by `generate_stims.py`.

`generate_stims.py` is currently set to generate 60 sets of 10 stimuli (i.e. stimuli for 60 trials), for a total of 600 pre-generated images. Each trial set consists of 10 stimuli whose shapes and colors are distributed as 10 equally spaced points on the VCS space and the CIELAB space, respectively. If you use fewer than 10 stimuli per trial, you can select a random subset of each set of 10 per trial. You can also generate more or fewer trials by changing the `trial_num` parameter in `trial_matrix()`.
