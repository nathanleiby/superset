import numpy as np
import numpy
import cv2
from matplotlib import pyplot as plt
import os

# Show images on a plot
def display(img_defs):
  fig = plt.figure()
  for idx, i in enumerate(img_defs):
    plt.subplot(4,2,idx+1)
    plt.imshow(i['image'],cmap = 'gray')
    plt.title(i['title']), plt.xticks([]), plt.yticks([])

  # close plot if you hit any key from terminal
  plt.draw()
  plt.pause(1) # <-------
  raw_input("<Hit Enter To Close>")
  plt.close()

def normalize_colors(I):
  In = I.astype(float)
  II = In ** 2
  II = np.sum(II, axis=2)
  II = np.sqrt(II)
  II = II[..., np.newaxis]
  II = np.ma.concatenate((II, II, II), axis=2)
  C = np.divide(I, II)
  C = cv2.normalize(C, alpha=0, beta=255,
                    norm_type=cv2.NORM_MINMAX)
  IC = np.uint8(C)
  return IC

def to_bw(img):
  threshold = 130 # TODO: May need to adjust. 115 result in all-black
  GRAY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  BW = cv2.threshold(GRAY, threshold, 255, cv2.THRESH_BINARY)[1]
  return numpy.invert(BW)

def detect_count(img_bw):
  BWt = img_bw.copy()
  cntrs, hircy = cv2.findContours(BWt,
                                  cv2.RETR_EXTERNAL,    # cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)
  F = numpy.zeros(img_bw.shape, dtype=numpy.uint8)
  MASK = numpy.zeros(img_bw.shape, dtype=numpy.uint8)
  areas = [cv2.contourArea(cnt) for cnt in cntrs]
  t = numpy.mean(filter(lambda x: x > 50, areas))
  t = t * 0.9
  MASKrect = None
  MASKcnt = None
  wasMasked = False
  for idx, cnt in enumerate(cntrs):
    if (areas[idx] > t):
      # thickness -1 will fill the conntours
      cv2.drawContours(F, [cnt], 0, (255), thickness=-1)
      if (not wasMasked):
        wasMasked = True
        cv2.drawContours(MASK, [cnt], 0, (255), thickness=-1)
        MASKcnt = cnt
        MASKrect = cv2.boundingRect(cnt)

  #cv2.imshow('Count', F)
  #cv2.imshow('Mask', self.MASK)
  cntrs, hircy = cv2.findContours(F,
                                  cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)

  amount = len(cntrs)
  return amount

def analyze(image_path, expected=None):
  print "Analyzing", image_path
  img = cv2.imread(image_path) # load in color
  edges = cv2.Canny(img,100,200)
  normalized = normalize_colors(img)
  normalized_edges = cv2.Canny(normalized,100,200)
  bw = to_bw(img)

  # non images
  count = detect_count(bw)
  # print "Count = ", count
  shading = None
  shape = None
  color = None

  actual = dict(color=color, shading=shading, shape=shape, count=count)

  # Print out images to debug the computer vision steps
  debug = False
  if debug:
    defs = [
      dict(title='original', image=img),
      dict(title='edges', image=edges),
      dict(title='normalized', image=normalized),
      dict(title='normalized edges', image=normalized_edges),
      dict(title='bw', image=bw),
    ]
    display(defs)

  # Compare actual results VS expected results
  if expected:
    error = False
    for k, v in expected.iteritems():
      if actual.get(k) != v:
        print "\t{}: actual = {} (expected = {})".format(k, actual[k], expected[k])

  print ""

def determine_expected(filename):
  name, ext = filename.split('.')
  color, shading, shape, count = name.split('-')
  count = int(count)
  return dict(color=color, shading=shading, shape=shape, count=count)

dirname='./images/single-card/'
for filename in os.listdir(dirname):
  fullpath = os.path.join(dirname, filename)
  expected = determine_expected(filename)
  analyze(fullpath, expected)
  # analyze("images/single-card/green-oval.png")

## only closes plot from GUI
#plt.show()

## Open CV image display
# win = cv2.namedWindow('normalized')
# cv2.imshow('normalized', normalized)
# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
  # cv2.destroyAllWindows()


