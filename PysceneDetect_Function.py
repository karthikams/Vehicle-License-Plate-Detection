
# coding: utf-8

# In[1]:


from __future__ import print_function
import os
import scenedetect
# Standard PySceneDetect imports:
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
# For caching detection metrics and saving/loading to a stats file
from scenedetect.stats_manager import StatsManager


# In[2]:


def pyscenedetect(path,output_csv_file):
    # For content-aware scene detection:
    from scenedetect.detectors.content_detector import ContentDetector

    video_manager = VideoManager([path])
    stats_manager = StatsManager()
    # Construct our SceneManager and pass it our StatsManager.
    scene_manager = SceneManager(stats_manager)
    # Add ContentDetector algorithm (each detector's constructor
    # takes detector options, e.g. threshold).
    scene_manager.add_detector(ContentDetector(threshold = 12))
    base_timecode = video_manager.get_base_timecode()

    scene_list = []
    # Set downscale factor to improve processing speed.
    video_manager.set_downscale_factor()

    # Start video_manager.
    video_manager.start()

    # Perform scene detection on video_manager.
    scene_manager.detect_scenes(frame_source=video_manager)

    # Obtain list of detected scenes.
    scene_list = scene_manager.get_scene_list(base_timecode)
    # Each scene is a tuple of (start, end) FrameTimecodes.

    print('List of scenes obtained:')
    for i, scene in enumerate(scene_list):
        print(
            'Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
            i+1,
            scene[0].get_timecode(), scene[0].get_frames(),
            scene[1].get_timecode(), scene[1].get_frames(),))
        
    #writing scene list to .csv file
    f = open(output_csv_file, "w+")
    scenedetect.scene_manager.write_scene_list(f, scene_list, cut_list=None)

