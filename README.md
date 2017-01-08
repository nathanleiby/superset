Superset
====

## Setup

### Python Setup

Make a virtual env.
Install requirements.

```
mkvirtualenv superset
make deps
```

### OpenCV2 Setup

Followed these steps http://www.learnopencv.com/install-opencv-3-on-yosemite-osx-10-10-x/

Install OpenCV 2 on Mac OSX

```
brew tap homebrew/science
brew install opencv
```

Because running in a Python Virtualenv, we need to get access to OpenCV (installed as a system package). This is possible to do by creating a few symlinks.

```
ln /usr/local/lib/python2.7/site-packages/cv.py cv.py
ln /usr/local/lib/python2.7/site-packages/cv2.so cv2.so
```

Alternately, could try setting up a Virtualenv with the `--system-site-packages` flag.

## Tests

```
make test
```

## Running locally

```
make run
```

-----------

## TODOS

- `count` detection is less reliabe for diamonds and shaded

## Ideas to Explore

- Template matching
    - http://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
	- http://docs.opencv.org/3.1.0/d4/dc6/tutorial_py_template_matching.html
	- with scaling - http://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
- Shape Detection
	- http://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
	- http://stackoverflow.com/questions/11424002/how-to-detect-simple-geometric-shapes-using-opencv
- Square detection
	- http://stackoverflow.com/questions/8667818/opencv-c-obj-c-detecting-a-sheet-of-paper-square-detection
	- http://stackoverflow.com/questions/10533233/opencv-c-obj-c-advanced-square-detection
- Circle detection
	- http://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_circle/hough_circle.html#hough-circle
- OpenCV Python examples
	- https://github.com/opencv/opencv/tree/master/samples/python
