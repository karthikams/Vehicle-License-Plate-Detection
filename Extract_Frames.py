
# coding: utf-8

# In[5]:


import cv2


# In[6]:


def extract_frames(path):
    vc = cv2.VideoCapture(path)
    while True:
        c = 1

        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False

        if rval != True:
            break

        while rval:
            rval, frame = vc.read()
            cv2.imwrite('output/video_back_license_plate/' + str(c).zfill(7) + '.jpg', frame)
            c = c + 1  
        vc.release()    


#  
# 
# 
