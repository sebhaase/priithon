# The Priithon Platform #

## How to install ##

  * on Linux:
    * extract the tar-archive using "tar xjf Priithon\_25\_Linux.....tbz"
    * move the resulting Priithon\_25\_linux directory where ever you want
    * create a symbolic link from a place, where in your PATH; e.g.
```
cd ~/bin;ln -s ~/Priithon_25_linux/priithon_script priithon
```

  * on Windows (2000/XP/Vista; 32-bit):
    * if you don't have Python 2.5 installed, go to [python.org](http://www.python.org/download/releases/2.5.2/) and download and install the [MSI installer](http://www.python.org/ftp/python/2.5.2/python-2.5.2.msi)
    * extract the zip-archive to your C-drive (`C:\`) -- maybe other places work !?
    * drag the priithon shortcut from the resulting Priithon\_25\_window to your desktop

  * on OS-X:  (10.4+)
    * open the DMG file
    * move the Priithon\_25\_mac directory where ever you want
    * put the priithon\_script into your dock (only works to put it on the right side of it)
    * and/or: create a symbolic link from a place, where in your PATH; e.g.
```
cd ~/bin;ln -s ~/Priithon_25_mac/priithon_script priithon
```


## The Priithon Platform ##

### True statements: ###
  * Priithon is ready to install for Windows, Linux and Mac OS-X
  * OS-X has to be >= 10.4
  * Our linux platform is debian; but RedHat should also work

  * Priithon starts python using the **true division** --> so `1/2==0.5`
  * "Priithon" has two parts:
    1. I have downloaded and compiled multiple python projects from the web
      * this includes: Numpy, SciPy, wxPython, PIL, FFTW(2), Pyro, SWIG
    1. I have wriiten my own code, including:
      * fast, userfriendly and flexible nd-image viewer
      * customized wxPython-pyShell interface
      * SWIG typemaps for (templated) C++ array 

&lt;-&gt;

 ndarray mapping (no memory copying!)
      * some modifications to PIL

  * Lin Shao has helped creating the Py-2.5 based version
  * Shao Lin has always believed in it



---

# comments #

Add your comments here.
> Your text can use common wiki-formatting like this:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages