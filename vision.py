import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os

DO_DISPLAY = False


def display(img_defs):
    """ Show images on a plot """
    plt.figure(figsize=(10, 10))
    horiz = len(img_defs) / 2 + 1
    for idx, i in enumerate(img_defs):
        plt.subplot(horiz, 2, idx + 1)
        plt.imshow(i['image'], cmap='gray')
        plt.title(i['title']), plt.xticks([]), plt.yticks([])

    # close plot if you hit any key from terminal
    plt.draw()
    plt.pause(1)  # <-------
    raw_input("<Hit Enter To Close>")
    plt.close()


def normalize_colors(I):
    """ Because images are taken in different light, we need to normalize the
    color balance """
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
    threshold = 130  # TODO: May need to adjust. 115 result in all-black
    GRAY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    BW = cv2.threshold(GRAY, threshold, 255, cv2.THRESH_BINARY)[1]
    return np.invert(BW)


def detect_count(img_bw):
    BWt = img_bw.copy()
    cntrs, hircy = cv2.findContours(BWt,
                                    cv2.RETR_EXTERNAL,    # cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
    F = np.zeros(img_bw.shape, dtype=np.uint8)
    MASK = np.zeros(img_bw.shape, dtype=np.uint8)
    areas = [cv2.contourArea(cnt) for cnt in cntrs]
    t = np.mean(filter(lambda x: x > 50, areas))
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

    # cv2.imshow('Count', F)
    # cv2.imshow('Mask', self.MASK)
    cntrs, hircy = cv2.findContours(F,
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    amount = len(cntrs)
    return amount, MASK, MASKrect, MASKcnt


def cut_masks(img, img_bw, img_mask, mask_rect):
    rect = [0, 0, 0, 0]
    rect[0] = mask_rect[0] - 5
    rect[1] = mask_rect[1] - 5
    rect[2] = mask_rect[0] + mask_rect[2] + 5
    rect[3] = mask_rect[1] + mask_rect[3] + 5
    CutI = img[rect[1]:rect[3], rect[0]:rect[2]]
    CutBW = img_bw[rect[1]:rect[3], rect[0]:rect[2]]
    CutM = img_mask[rect[1]:rect[3], rect[0]:rect[2]]
    return CutI, CutBW, CutM


def find_shading(cut_bw, cut_mask):
    S = cv2.bitwise_and(cut_bw, cut_mask)
    E = cv2.Canny(S, 90, 200, apertureSize=3)
    # cv2.imshow('Edge', E)
    nE = np.count_nonzero(E)
    nM = np.count_nonzero(cut_mask)
    dEM = float(nE) / float(nM)
    # print "Mask %d, Edge %d, div %f" % (nM, nE, dEM)
    shading = ""
    if (dEM < 0.08):
        shading = 'full'  # solid
    elif (dEM > 0.17):
        shading = 'striped'
    else:
        shading = 'open'
    return shading


def find_shading2(img):
    # edges = cv2.Canny(img,100,200)
    edges = cv2.Canny(img, 100, 200, apertureSize=3)
    nE = np.count_nonzero(edges)
    print "non-zero edges", nE


def find_color(img, cut_i, cut_bw, cut_m):
    S = cv2.bitwise_and(cut_bw, cut_m)
    S = cv2.bitwise_and(cut_i, cut_i, mask=S)
    # cv2.imshow('VS', S)
    # ShowHist(S, self.cardInfo['color'])
    HSV = cv2.cvtColor(S, cv2.COLOR_BGR2HSV)
    H = HSV[:, :, 0]
    nG = np.count_nonzero(cv2.inRange(H, 25, 90))
    nP = np.count_nonzero(cv2.inRange(H, 140, 170))
    nR = np.count_nonzero(cv2.inRange(H, 170, 255))
    C = ['red', 'green', 'purple']
    nC = [nR, nG, nP]
    i = np.argmax(nC)
    return C[i]


def find_shape(mask_cnt):
    cnt = mask_cnt
    mmnts = cv2.moments(cnt)
    hu = cv2.HuMoments(mmnts)
    # print cv2.contourArea(cnt)
    symbol = ""
    if (hu[0] < 0.207):
        symbol = 'oval'
    elif (hu[0] > 0.23):
        symbol = 'squiggle'
    else:
        symbol = 'diamond'

    return symbol

# ----------------------------------------------
# Run the analysis and interpret its results
# ----------------------------------------------


def analyze(image_path, expected=None):
    # if not expected or expected.get('shading') != 'open':
        # return

    print "Analyzing", image_path
    img = cv2.imread(image_path)  # load in color
    edges = cv2.Canny(img, 100, 200)
    edgesAperture = cv2.Canny(img, 90, 200, apertureSize=3)
    normalized = normalize_colors(img)
    normalized_edges = cv2.Canny(normalized, 100, 200)
    img_bw = to_bw(img)
    bw_edges = cv2.Canny(img_bw, 100, 200)

    # find count
    # TODO: separate mask creation from counting?
    # TODO: Determine why 'detect_count' is failing to return masks in some
    # cases -> happens if no `areas` found in `detect_count`
    count, img_mask, mask_rect, mask_cnt = detect_count(img_bw)
    cut_i, cut_bw, cut_m = cut_masks(img, img_bw, img_mask, mask_rect)

    shading = find_shading(cut_bw, cut_m)
    color = find_color(img, cut_i, cut_bw, cut_m)
    shape = find_shape(mask_cnt)
    actual = dict(color=color, shading=shading, shape=shape, count=count)

    # Compare actual results VS expected results
    if expected:
        for k, v in expected.iteritems():
            if actual.get(k) != v:
                tmpl = "\t{}: actual = {} (expected = {})"
                print tmpl.format(k, actual[k], expected[k])

    print ""

    # Print out images to debug the computer vision steps
    if DO_DISPLAY:
        defs = [
            dict(title='original', image=img),
            dict(title='normalized', image=normalized),
            dict(title='edges', image=edges),
            dict(title='edges (normalized)', image=normalized_edges),
            dict(title='edges with apertureSize', image=edgesAperture),
            dict(title='bw', image=img_bw),
            dict(title='bw_edges', image=bw_edges),
            dict(title='mask', image=img_mask),
            dict(title='cut_i', image=cut_i),
            dict(title='cut_bw', image=cut_bw),
            dict(title='cut_m', image=cut_m),
        ]

        # Open CV image display
        display(defs)

    return actual


def determine_expected(filename):
    name, ext = filename.split('.')
    color, shading, shape, count = name.split('-')
    count = int(count)
    return dict(color=color, shading=shading, shape=shape, count=count)


COLOR_LIST = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 0, 255)
]


def findCards(fullpath):
    """ Given a filepath to a photo containing set cards,
    return a list of rectangles that outline each card """
    threshold = 115
    defs = []
    I = cv2.imread(fullpath)
    defs.append(dict(title='original', image=I))

    # expected dimensions before: 2000px x 3000px
    I = cv2.resize(np.rot90(I), (0, 0,), fx=0.5, fy=0.5)
    defs.append(dict(title='rotated', image=I))

    GRAY = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    defs.append(dict(title='gray', image=GRAY))

    BW = cv2.threshold(GRAY, threshold, 255, cv2.THRESH_BINARY)[1]

    defs.append(dict(title='bw', image=BW))

    # BW = np.invert(BW)
    BWt = BW.copy()
    cntrs, hircy = cv2.findContours(BWt,
                                    cv2.RETR_EXTERNAL,    # cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
    F = np.zeros(BW.shape, dtype=np.uint8)
    # MASK = np.zeros(BW.shape, dtype=np.uint8)
    areas = [cv2.contourArea(cnt) for cnt in cntrs]
    t = np.mean(filter(lambda x: x > 50, areas))
    t = t * 0.50  # decreasing from .9 to .5 works better with a tilted image
    # MASKrect = None
    # MASKcnt = None
    # wasMasked = False
    defs = []
    cardRects = []
    croppedCards = []
    for idx, cnt in enumerate(cntrs):
        if (areas[idx] > t):
            # thickness -1 will fill the conntours
            cv2.drawContours(F, [cnt], 0, (255), thickness=-1)
            rect = cv2.boundingRect(cnt)
            cardRects.append(rect)
            print "RECT", rect
            cv2.rectangle(
                I,
                (rect[0],
                 rect[1]),
                (rect[2] +
                 rect[0],
                    rect[3] +
                    rect[1]),
                COLOR_LIST[
                    idx %
                    6],
                thickness=2)
            y1, y2 = rect[1], rect[1] + rect[3]
            x1, x2 = rect[0], rect[0] + rect[2]

            cropped = I[y1:y2, x1:x2]
            croppedCards.append(cropped)
            # defs.append(cropped)
    print "Number rects found = ", len(cardRects)

#   for i, c in enumerate(croppedCards):
#     cv2.imshow('Image'+str(i), c)
#   cv2.waitKey(0)
#   cv2.destroyAllWindows()
    # defs.append(dict(title='f', image=F))
    # defs.append(dict(title='outlines', image=I))
    # display(defs)
    # return 12 sliced images, to pass to single card analysis
    return cardRects


if __name__ == "__main__":
    # TODO: take args to:
    #   - do run of single cards vs mutliple cards ('game')
    #   - display analysis in separate window
    SINGLE = False
    if SINGLE:
        # single card analysis
        dirname = './images/single-card/'
        for filename in os.listdir(dirname):
            if not filename.endswith('.png'):
                continue
            fullpath = os.path.join(dirname, filename)
            expected = determine_expected(filename)
            analyze(fullpath, expected)
    else:
        dirname = './images/game/'
        # multi card analysis -- split into single cards
        for i in [1, 2, 3]:
            fullpath = os.path.join(dirname, "game00{}.jpg".format(i))
            findCards(fullpath)
