from datetime import timedelta
import cv2
import numpy as np
import os

SAVING_FRAMES_PER_SECOND=1

def frame_duration(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def main(video_file,p):
    filepath='path/to/location/to/save/frames'
    if not os.path.isdir(filepath):
        os.mkdir(filepath)

    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    frames_durations = frame_duration(cap, saving_frames_per_second)
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            
            break
        
        frame_duration = count / fps
        try:
            closest_duration = frames_durations[0]
        except IndexError:
            break
        if frame_duration >= closest_duration:
            c=str(p)+'_'+str(count)
            cv2.imwrite(os.path.join(filepath, f"{c}.jpg"), frame) 
            try:
                frames_durations.pop(0)
            except IndexError:
                pass
        count += 1
        
if __name__ == "__main__":
 dir_path='path/of/dataset/DROZY/videos_i8/'
 for x in os.listdir(dir_path):
     file = os.path.join(dir_path, x)
     print(file)
     main(file,x[:-6])