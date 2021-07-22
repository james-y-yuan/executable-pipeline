# Source Files

These files are Python/PsychoPy source code for the experiment used in our paper. 

* `visual_memory_precision.py` calls the main code function. You will need the following Python packages: `ctypes`, `pathlib`, `numpy`, `scipy`, `psychopy`, `pillow`, `pyglet`, `dropbox`, `requests`.
* `logic.py` contains all of the main logical functions.
* `helper.py` contains auxiliary functions, used in `logic.py`.
* `visual_memory_precision.spec` is a specifier file for PyInstaller. Use it when compiling an .exe from `visual_memory_precision.py`. See Step C of the demo for details.
* `python_server.py` is an HTTP server. `python_server.py` would normally be running on our lab's Linux server, with its IP and port set to our server's settings to receive HTTP traffic, and `upload_http()` in `helper.py` configured to send data to that server. However, these have been modified here to use IP `localhost` and port `8000`, which sends data only to a server running on the same computer. For more info, see Step B of the demo.
* `ZL_colors.mat` is a database file used by `helper.py` to calculate in the CIELAB space.
* `freetype.dll` and `matplotlibrc` are used by `visual_memory_precision.spec`; see Step C.
