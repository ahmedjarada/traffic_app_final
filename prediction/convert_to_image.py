import cv2


def get_frame(input_video, sec, count):
    vidcap = cv2.VideoCapture(input_video)

    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        cv2.imwrite("image" + str(count) + ".jpg", image)  # save frame as JPG file
    return hasFrames


def convert(input_video):
    sec = 0
    frameRate = 1  # //it will capture image in each 1 second
    count = 1
    success = get_frame(input_video=input_video, sec=sec, count=count)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = get_frame(input_video=input_video, sec=sec, count=count)
