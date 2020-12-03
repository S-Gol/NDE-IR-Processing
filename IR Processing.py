import cv2
import numpy as np

#File config
imagePath = "C:/College/Senior 1/NDE/IR/images/"
videoOutPath = "C:/College/Senior 1/NDE/IR/IR_out.mp4"
video = cv2.VideoCapture(readPath)

#Debug config
show_grayscale = False
show_dt = False


#Input video data
frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height  = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
framerate = video.get(cv2.CAP_PROP_FPS)

print("Video loaded. Resolution: " + str(width) + "x" + str(height) + " frames: " + str(frames))

#calculate the derivative of color at each point in the image with respect to the previous and next image
def timeDerivative(array):
    dtArray = []
    #Calculate the time derivatives
    for f in np.arange(1, len(array)-1):
        dtArray.append(array[f-1]-array[f+1])
        if(show_dt):
            cv2.imshow("Time derivative " + str(f) + "/" + str(frames), dtArray[f])
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
    return dtArray

#Write the videos and image array to a file
def writeVideo(array):
    outputVideo = cv2.VideoWriter(videoOutPath, cv2.VideoWriter_fourcc('M','P','E','G'), framerate, (width, height))
    for f in np.arange(0, len(array)):
        outputVideo.write(cv2.cvtColor(array[f]*f,cv2.COLOR_GRAY2BGR))
        cv2.imwrite(imagePath+str(f)+".png",array[f])
    outputVideo.release()

    
grayscaleArray = []

#Convert to a list of NDArrays
while(True):
    ret, frame = video.read()
    if(ret):
        grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayscaleArray.append(grayscaleFrame)        
        if(show_grayscale):
            cv2.imshow("Grayscale " + str(frameCount) + "/" + str(frames), grayscaleFrame)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
        frameCount+=1

    else:
        break

#Smooth the video to (attempt) to remove the artefacting present after derivative calculations
def blur(array):
    blurArray=[]
    for f in np.arange(0,len(array)):
        blurArray.append(cv2.bilateralFilter(array[f], 9,75,75))
    return blurArray
video.release()

#writeVideo(grayscaleArray)
writeVideo(timeDerivative(timeDerivative(grayscaleArray)))

print("done")