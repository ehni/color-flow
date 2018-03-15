# Import
import sys
import time
try:
    import cv2
except ImportError:
    sys.exit("""You need opencv-python!
                install it from https://github.com/skvark/opencv-python
                or run pip install opencv-python.""")
try:
    import argparse
except ImportError:
    sys.exit("""You need cv2!
                install it from web
                or run pip install argparse.""")
try:
    import numpy as np
except ImportError:
    sys.exit("""You need numpy!
                install it from the web
                or run pip install numpy.""")



# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = 'X' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if __name__== "__main__":
    print("== Starting Color-Flow ==")
    print("==> Reading arguments")
    arguments = argparse.ArgumentParser()
    arguments.add_argument("--pathIn", help="path to video")
    arguments.add_argument("--pathOut", help="path to save the image")
    arguments.add_argument("--maxWidth", help="maximum width of the output image")
    arguments.add_argument("--maxHeight", help="maximum height of the output image")
    arguments.add_argument("--takeFrames", help="Use every frame (True) or just take a frame every second (False, Default)")
    args = arguments.parse_args()
    pathIn = args.pathIn
    pathOut = args.pathOut
    takeFrames = args.takeFrames
    maxHeight = args.maxHeight
    maxWidth = args.maxWidth
    # Set up variables
    frameCount = 0
    count = 0
    colors = []

    if maxWidth == None:
        maxWidth = 2000
        print("maxWidth not set. Setting to default value %d" % maxWidth)

    if maxHeight == None:
        maxHeight = 4000
        print("maxHeight not set. Setting to default value %d" % maxHeight)

    if takeFrames == None:
        takeFrames = False
        print("takeFrames not set. Setting to default value %s. Using a frame every second now!" % takeFrames)
    elif takeFrames == "True" or takeFrames == "true":
        takeFrames = True
    elif takeFrames == "False" or takeFrames == "false":
        takeFrames = False
    else:
        print("Could not read the ’takeFrames' argument! Please enter a valid value. Using the standard value")
        takeFrames = False
        print("takeFrames not set. Setting to %s. Using a frame every second now!" % takeFrames)


    if pathIn == None:
        print("pathIn not set. Exiting...")
        sys.exit("""You must specify a input video with --pathIn=/path/to/video.mp4""")

    if pathOut == None:
        print("pathOut not set. Exiting...")
        sys.exit("""You must specify a place to save the output picture with --pathOut=/path/to/dir/""")


    print("==> Reading video from %s" % pathIn)
    vidcap = cv2.VideoCapture(pathIn)
    numberOfFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    actualFrames = 0
    success, image = vidcap.read()
    success = True
    step = 1

    if takeFrames == True:
        actualFrames = numberOfFrames
    else:
        actualFrames = int(numberOfFrames/24)

    # Calculate number of frames to read and ouput picture width and height
    if actualFrames > maxHeight:
        step = int(actualFrames / maxHeight)
        actualFrames = maxHeight
        #print("==> Actually reading %s frames with a step value of %s" % (maxHeight, step))

    picture_height = actualFrames
    picture_width = int(actualFrames * 0.5)
    print("==> Setting output picture dimension to %s x %s" % (picture_width, picture_height))

    print("==> Reading %d frames" % actualFrames)
    start_time = time.time()
    print_progress(0, actualFrames, prefix ='Progress:', suffix ='Complete', bar_length = 50)
    while success:
        if frameCount >= actualFrames:
            break
        if takeFrames == True:
            # Read every frame
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
        else:
            # Read frame every second
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
        success, image = vidcap.read()
        if success:
            avg_color_per_row = np.average(image, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            colors.append(avg_color)

            print_progress(frameCount, actualFrames, prefix='Progress:', suffix='Complete', bar_length=50)
            count = count + step
            frameCount = frameCount + 1

    print_progress(actualFrames, actualFrames, prefix='Progress:', suffix='Complete', bar_length=50)

    print("==> %s frames read in %.2f seconds " % (actualFrames, time.time() - start_time))

    print("==> Generating new image")

    # Create new picture
    picture = np.ones((picture_height,picture_width,3), np.uint8)

    # Reset counter
    print_progress(0, picture_height, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
    start_time = time.time()
    count = 0
    # Loop through each row
    for i in range(0, picture_height-1):
        # Loop through each column
        for j in range(0, picture_width-1):
            # Set color
            color = colors[count]
            picture[i, j] = color

        count = count + 1
        print_progress(i, picture_height, prefix='Progress:', suffix='Complete', bar_length=50)

    print_progress(picture_height, picture_height, prefix='Progress:', suffix='Complete', bar_length=50)

    print("==> Picture generated in  %.2f seconds" % (time.time() - start_time))

    print("==> Saving new picture to %s" % pathOut)

    cv2.imwrite(pathOut + "/colored.png", picture)

    print("==> Done!")
