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
    arguments = argparse.ArgumentParser(description="Tool for creating a color palette picture from a .mp4 video")
    arguments.add_argument("pathIn", help="path to video")
    arguments.add_argument("pathOut", help="path to save the image")
    arguments.add_argument("--maxWidth", type=int, default=2000, help="maximum width of the output image, default=2000")
    arguments.add_argument("--maxHeight", type=int, default=4000, help="maximum height of the output image, default=4000")
    arguments.add_argument("--takeFrames", type=bool, default=False, help="Use every frame (True) or just take a frame every second (False, Default)")
    args = arguments.parse_args()
    print("== Starting Color-Flow ==")
    print("==> Reading arguments")
    pathIn = args.pathIn
    pathOut = args.pathOut
    takeFrames = args.takeFrames
    maxHeight = int(args.maxHeight)
    maxWidth = int(args.maxWidth)

    # Set up variables
    frameCount = 0
    count = 0
    colors = []

    # Check arguments
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

    if pathIn == None:
        print("pathIn not set. Exiting...")
        sys.exit("""You must specify a input video with --pathIn=/path/to/video.mp4""")

    if pathOut == None:
        print("pathOut not set. Exiting...")
        sys.exit("""You must specify a place to save the output picture with --pathOut=/path/to/dir/""")


    print("==> Reading video from %s" % pathIn)
    vidcap = cv2.VideoCapture(pathIn)
    numberOfFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    actualFrames = 0
    success, image = vidcap.read()
    success = True
    step = 1
    print("Frames: %d" % numberOfFrames)
    print("FPS: %d" % fps)

    if takeFrames == True:
        actualFrames = numberOfFrames
    else:
        actualFrames = int(numberOfFrames/fps)

    # Calculate number of frames to read and ouput picture width and height
    if actualFrames > maxHeight:
        step = int(actualFrames / maxHeight)
        actualFrames = maxHeight
        #print("==> Actually reading %s frames with a step value of %s" % (maxHeight, step))

    picture_height = int(actualFrames)
    picture_width = int(actualFrames * 2/3)
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

    pictureName = "colored_{}x{}.png".format(picture_width,picture_height)

    print("==> Saving new picture {} to {}".format(pictureName, pathOut))

    cv2.imwrite(pathOut + "/" + pictureName, picture)

    print("==> Done!")
