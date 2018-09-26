 
# Catherine Huang - yanzhenh - TP D1 Artifacts
# cited from https://github.com/LBPeraza/112-PyKinect/blob/master/PyKinectGame.py and 
             https://github.com/Kinect/PyKinect2/blob/master/examples/PyKinectBodyGame.py
 

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
from pygame.locals import *
import sys
import time

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]

class Struct: pass
Joints = Struct()

Joints.head = PyKinectV2.JointType_Head
Joints.neck = PyKinectV2.JointType_Neck
Joints.spineTop = PyKinectV2.JointType_SpineShoulder
Joints.spineMid = PyKinectV2.JointType_SpineMid
Joints.spineLow = PyKinectV2.JointType_SpineBase

Joints.leftShoulder = PyKinectV2.JointType_ShoulderLeft
Joints.rightShoulder = PyKinectV2.JointType_ShoulderRight

Joints.leftWrist = PyKinectV2.JointType_WristLeft
Joints.rightWrist = PyKinectV2.JointType_WristRight

Joints.leftHip = PyKinectV2.JointType_HipLeft
Joints.rightHip = PyKinectV2.JointType_HipRight

Joints.rightElbow = PyKinectV2.JointType_ElbowRight
Joints.leftElbow = PyKinectV2.JointType_ElbowLeft

Joints.leftHand = PyKinectV2.JointType_HandLeft
Joints.rightHand = PyKinectV2.JointType_HandRight

Joints.leftHandTip = PyKinectV2.JointType_HandTipLeft
Joints.rightHandTip = PyKinectV2.JointType_HandTipRight

Joints.leftThumb = PyKinectV2.JointType_ThumbLeft
Joints.rightThumb = PyKinectV2.JointType_ThumbRight

Joints.leftKnee = PyKinectV2.JointType_KneeLeft
Joints.rightKnee = PyKinectV2.JointType_KneeRight

Joints.leftAnkle = PyKinectV2.JointType_AnkleLeft
Joints.rightAnkle = PyKinectV2.JointType_AnkleRight

Joints.leftFoot = PyKinectV2.JointType_FootLeft
Joints.rightFoot = PyKinectV2.JointType_FootRight

def swap(lst, i, j):
    (lst[i], lst[j]) = (lst[j], lst[i])

class Dictionary(object):
    def __init__(self, vocab):
        self.vocab = vocab  # list
    
    def add(self, word): # return None
        assert type(word) == Word
        for w in self.vocab:
            if w == word:
                return None
        self.vocab.append(word)
    def remove(self, word):  # return None
        for w in self.vocab:
            if w == word:
                self.vocab.remove(w)

    def refresh(self):
        for start_index in range(len(self.vocab)):
            mini_index = start_index
            for j in range(start_index, len(self.vocab)):
                if self.vocab[j].name < self.vocab[mini_index].name:
                    mini_index = j
            swap(self.vocab, start_index, mini_index)
        for i in range(len(self.vocab)-1):
            if self.vocab[i] == self.vocab[i+1]:
                self.remove(self.vocab[i+1])

    def __repr__(self):
        pass


class Word(object):
    def __init__(self, name, frames):
        self.name = name
        self.frames = frames # frames is a list of 4 Frame(s), each Frame contains the displacement of all related joints relevant to certain body parts
                             # [start, mid1, mid2, end]
                             # [ [list of JointPos], [], [], ...]
    def __eq__(self, other):
        if len(self.frames) != len(other.frames) or self.name != other.name:
            return False
        else:
            for i in range(len(self.frames)):
                if self.frames[i] != other.frames[i]:
                    return False
            else:
                return True
  


class Frame(object):
# a frame is a tuple that contains the current positions of all the key joints (JointPos's)
    def __init__(self, index, content):
        # has a sequence number and JointPos's
        self.index = index
        self.content = content # content being a tuple of JointPos's


    def __eq__(self, other):
        if len(self.content) != len(other.content):
            return False
        else:
            for i in range(len(self.content)):
                if self.content[i] != other.content[j]:
                    return False
            return True



class JointPos(object):
    def __init__(self, joint_int, relative_joint_int, vector):
        self.joint_int = joint_int
        self.relative_joint_int = relative_joint_int
        self.vector = vector  # vector being a list [dx, dy] pointing from rela. to joint.
                              # or [dx, dy, dz]

    def __eq__(self, other):
        if self.joint_int == other.joint_int and self.relative_joint_int == other.relative_joint_int and self.vector == other.vector:
            return True
        else:
            return False


    


vocab = list()
dictionary = Dictionary(vocab)
#  # Word   -->    Word.name   |   Word.frames   -->   frames = [Frame0, Frame1, Frame2 ...]   -->    [JointPos0, JointPos1, JointPos2...]


dictionary.add(Word("hello", [Frame(0, [JointPos (JointType_HandRight, JointType_ShoulderRight, [1, 20]  ) ]),       # calculate the motion vector and multiply the values by a fix number, say 2000, and use almost equal to compare 
                              Frame(1, [JointPos (JointType_HandRight, JointType_ShoulderRight, [4, 17]  ) ]), 
                              Frame(2, [JointPos (JointType_HandRight, JointType_ShoulderRight, [13, 19]  ) ]), 
                              Frame(3, [JointPos (JointType_HandRight, JointType_ShoulderRight, [22, 20]  ) ])]))

dictionary.add(Word("day",  [Frame(0, [JointPos(JointType_HandRight, JointType_ShoulderRight, [-8.6, 5]),  
                                       JointPos(JointType_HandLeft, JointType_ShoulderLeft, [18, -20])]),
                           Frame(1, [JointPos(JointType_HandRight, JointType_ShoulderRight, [-16.7, 3.3]),  
                                     JointPos(JointType_HandLeft, JointType_ShoulderLeft, [18, -18])]),
                           Frame(2, [JointPos(JointType_HandRight, JointType_ShoulderRight, [-20, -7.5]),  
                                     JointPos(JointType_HandLeft, JointType_ShoulderLeft, [18, -18])]),
                           Frame(3, [JointPos(JointType_HandRight, JointType_ShoulderRight, [-20, -10]),  
                                     JointPos(JointType_HandLeft, JointType_ShoulderLeft, [18, -18])])]))

dictionary.add(Word("morning", [Frame(0, [JointPos(JointType_HandRight, JointType_ShoulderRight, [-20, -10]),  
                                          JointPos(JointType_HandLeft, JointType_ShoulderLeft, [18, -18])]),
                                Frame(1, [JointPos(JointType_HandRight, JointType_ShoulderRight, [-20, -7.5]),  
                                          JointPos(JointType_HandLeft, JointType_ShoulderLeft, [18, -18])]),
                                Frame(2, [JointPos(JointType_HandRight, JointType_ShoulderRight, [-16.7, 3.3]),  
                                          JointPos(JointType_HandLeft, JointType_ShoulderLeft, [18, -18])]),
                                Frame(3, [JointPos(JointType_HandRight, JointType_ShoulderRight, [-8.6, 5]),  
                                          JointPos(JointType_HandLeft, JointType_ShoulderLeft, [18, -20])])]))

dictionary.add(Word("year", [Frame(0, [JointPos(JointType_HandLeft, JointType_HandRight, [1, 1])]),
                             Frame(1, [JointPos(JointType_HandLeft, JointType_HandRight, [0, 0])]),
                             Frame(2, [JointPos(JointType_HandLeft, JointType_HandRight, [0, -15])]),
                             Frame(3, [JointPos(JointType_HandLeft, JointType_HandRight, [0, 1])])]))

dictionary.add(Word("love", [Frame(0, [JointPos(JointType_HandLeft, JointType_ElbowRight, [0, 12]), 
                                       JointPos(JointType_HandRight, JointType_ElbowLeft, [0, 12])]),
                             Frame(1, [JointPos(JointType_HandLeft, JointType_ElbowRight, [0, 12]), 
                                       JointPos(JointType_HandRight, JointType_ElbowLeft, [0, 12])]),
                             Frame(2, [JointPos(JointType_HandLeft, JointType_ElbowRight, [0, 12]), 
                                       JointPos(JointType_HandRight, JointType_ElbowLeft, [0, 12])]),
                             Frame(3, [JointPos(JointType_HandLeft, JointType_ElbowRight, [0, 12]), 
                                       JointPos(JointType_HandRight, JointType_ElbowLeft, [0, 12])])]))



class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # When the first frame of a word is detected --> True
        self._action_started = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None

        # count the time passed
        self._counter = None

        self.goal = [False] * 4

        # Wait until user clicks "START"
        self._camera_on = False

        # store the detected word
        self.result = None

    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()
    
    # display the START button at the middle of the bottom of the screen
    def draw_start_button(self):
        print("drawing...")
        self.font = pygame.font.SysFont("Arial",70)
        self.text = self.font.render("START", 1, [128,0,0])
        self._frame_surface.blit(self.text,(self._screen.get_width()/2 + 50, self._screen.get_height()))
    
    # display the detected word in the middle of the screen       
    def draw_result(self, result):
        self.font1 = pygame.font.SysFont("Calibri", 300)
        self.text1 = self.font1.render(result, 1, [255,255,255])
        self._frame_surface.blit(self.text1,(10,10))

    

    def almostEquals(self, a, b):  # (dx,dy,dz), (dm,dn,do)
        # compares two vectors
        print("compare: ", a)
        print("with vector: ", b)
        for i in range(len(a)):
            if abs(100 * a[i] - b[i])  >= 10:
                return False
        return True
     
    def checkJoints(self, frame1, joints):
                        for i in range(len(frame1.content)):      # loop through all the jointPos's
                            if len(frame1.content[i].vector) == 2:                 
                                if not self.almostEquals((joints[frame1.content[i].joint_int].Position.x - 
                                                          joints[frame1.content[i].relative_joint_int].Position.x, 
                                                          joints[frame1.content[i].joint_int].Position.y - 
                                                          joints[frame1.content[i].relative_joint_int].Position.y), 
                                                         frame1.content[i].vector): 
                                    return False
                            elif len(frame1.content[i].vector) == 3:
                                if not self.almostEquals((joints[frame1.content[i].joint_int].Position.x - 
                                                          joints[frame1.content[i].relative_joint_int].Position.x, 
                                                          joints[frame1.content[i].joint_int].Position.y - 
                                                          joints[frame1.content[i].relative_joint_int].Position.y,
                                                          joints[frame1.content[i].joint_int].Position.y - 
                                                          joints[frame1.content[i].relative_joint_int].Position.z), 
                                                         frame1.content[i].vector): 
                                    return False
                        return True

    def run(self):
        # -------- Main Program Loop -----------
        while not self._done: 
            # --- Main event loop
            print("CAMERA ", self._camera_on)
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
            

            # --- Game logic should go here

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()
                
            # --- draw skeletons to _frame_surface
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i] 
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])
                    if not self._camera_on:
                        print("Displaying START button.")
                        self.draw_start_button()


                    

                    temp = dictionary.vocab

                    ############################################################## %% TEST

                    # Testing "hello"
                    #print("x: rightHand - rightshoulder = ", joints[JointType_HandRight].Position.x, " - ", joints[JointType_ShoulderRight].Position.x, 
                          #" = ", joints[JointType_HandRight].Position.x - joints[JointType_ShoulderRight].Position.x)
                    ##print("y: rightHand - rightshoulder = ", joints[JointType_HandRight].Position.y, " - ", joints[JointType_ShoulderRight].Position.y, 
                          #" = ", joints[JointType_HandRight].Position.y - joints[JointType_ShoulderRight].Position.y)
                    

                    # Testing "day": 
                    #print("Testing...\"day\"")
                    # ShoulderRight --> HandRight
                    #print("x: rightHand - rightShoulder = ", joints[JointType_HandRight].Position.x, " - ", joints[JointType_ShoulderRight].Position.x, 
                          #" = ", joints[JointType_HandRight].Position.x - joints[JointType_ShoulderRight].Position.x)
                    #print("y: rightHand - rightShoulder = ", joints[JointType_HandRight].Position.y, " - ", joints[JointType_ShoulderRight].Position.y, 
                          #" = ", joints[JointType_HandRight].Position.y - joints[JointType_ShoulderRight].Position.y)
                    #print("z: rightHand - rightShoulder = ", joints[JointType_HandRight].Position.z, " - ", joints[JointType_ShoulderRight].Position.z, 
                          #" = ", joints[JointType_HandRight].Position.z - joints[JointType_ShoulderRight].Position.z)
                         
                    # ShoulderLeft --> HandLeft
                    #print("x: leftHand - ShoulderLeft = ", joints[JointType_HandLeft].Position.x, " - ", joints[JointType_ShoulderLeft].Position.x, 
                          #" = ", joints[JointType_HandLeft].Position.x - joints[JointType_ShoulderLeft].Position.x)
                    #print("y: leftHand - ShoulderLeft = ", joints[JointType_HandLeft].Position.y, " - ", joints[JointType_ShoulderLeft].Position.y, 
                          #" = ", joints[JointType_HandLeft].Position.y - joints[JointType_ShoulderLeft].Position.y)
                    #print("z: leftHand - ShoulderLeft = ", joints[JointType_HandLeft].Position.z, " - ", joints[JointType_ShoulderLeft].Position.z, 
                          #" = ", joints[JointType_HandLeft].Position.z - joints[JointType_ShoulderLeft].Position.z)
                
                
                    # Testing "year":  
                    #print("Testing...\"year\"")
                    # HandLeft --> HandRight 
                    #print("x: leftHand - rightHand = ", joints[JointType_HandLeft].Position.x, " - ", joints[JointType_HandRight].Position.x, 
                          #" = ", joints[JointType_HandLeft].Position.x - joints[JointType_HandRight].Position.x)
                    #print("y: leftHand - rightHand = ", joints[JointType_HandLeft].Position.y, " - ", joints[JointType_HandRight].Position.y, 
                          #" = ", joints[JointType_HandLeft].Position.y - joints[JointType_HandRight].Position.y)
                    #print("z: leftHand - rightHand = ", joints[JointType_HandLeft].Position.z, " - ", joints[JointType_HandRight].Position.z, 
                          #" = ", joints[JointType_HandLeft].Position.z - joints[JointType_HandRight].Position.z)

                    #Testing "love":
                    #print("Testing...\"love\"")
                    #print("x: leftHand - rightElbow = ", joints[JointType_HandLeft].Position.x, " - ", joints[JointType_ElbowRight].Position.x, 
                    #      " = ", joints[JointType_HandLeft].Position.x - joints[JointType_ElbowRight].Position.x)
                    #print("y: leftHand - rightElbow = ", joints[JointType_HandLeft].Position.y, " - ", joints[JointType_ElbowRight].Position.y, 
                    #      " = ", joints[JointType_HandLeft].Position.y - joints[JointType_ElbowRight].Position.y)
                    #print("x: rightHand - leftElbow = ", joints[JointType_HandRight].Position.x, " - ", joints[JointType_ElbowLeft].Position.x, 
                    #      " = ", joints[JointType_HandRight].Position.x - joints[JointType_ElbowLeft].Position.x)
                    #print("y: rightHand - leftElbow = ", joints[JointType_HandRight].Position.y, " - ", joints[JointType_ElbowLeft].Position.y, 
                    #      " = ", joints[JointType_HandRight].Position.y - joints[JointType_ElbowLeft].Position.y)

                    ############################################################## %% TEST
                    


                    print(pygame.mouse.get_pos())
                    if pygame.mouse.get_pressed()[0]: 
                        print("Mouse clicked!")

                    if (800 <= pygame.mouse.get_pos()[0] <= 970 and 
                        900 <= pygame.mouse.get_pos()[1] <= 954):
                       print("Mouse in START area!") 
                       if pygame.mouse.get_pressed()[0]:
                           print("START button clicked.")
                           self._camera_on = True
                           self.result = None
                    else: 
                        print("Mouse OUT!")


                    
                    # dict includes: hello, day, morning, year, love  
                    
                    # display the previous detected word
                    if self.result != None:
                        self.draw_result(self.result)

                    # once the START button is clicked, code begins to "function"
                    if self._camera_on == True: 
                                                 
                        # comparison starts once it detects the beginning of a sign   
                        if not self._action_started:
                            for word in temp:
                                print("trying this word: ", word.name)
                                # See if all joints on first frame matches
                                if not self.checkJoints(word.frames[0], joints):
                                    print("still trying...")
                                    continue
                                # if matches, program starts
                                else:
                                    print("found one!")
                                    self._action_started = True
                                    self.startTime = time.time()
                                    self.goal[0] = True
                                    self.currWord = word
                                    print("first step completed!")
                                    break # oder keep looking in all the words and add potentially matching ones into a list
                        # detects if the rest of the same word matches within a certain time limit
                        else:
                            if time.time() - self.startTime > 15:
                                print("Time out!")
                                self._action_started = False
                                self._camera_on = False
                                self.currWord = None
                            elif self.goal[-1] == True:
                                print("result: ", self.currWord.name)
                                self.result = self.currWord.name
                                self.goal = [False] * 4
                                self._camera_on = False
                                self._action_started = False
                            else:
                                currentTestFrame = self.goal.index(False)
                                if self.checkJoints(word.frames[currentTestFrame], joints):
                                    print("Frame #", currentTestFrame, " matches!")
                                    self.goal[currentTestFrame] = True
 
                   


                    # -------------------------------------------------------------------------

                   
                    
                   

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))

            surface_to_draw = None
            pygame.display.update()
            
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            #self.timerfired()

            self._clock.tick(60)
            if self._counter != None:
                self._counter += 1


        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.font.quit()
        pygame.quit()


__main__ = "Kinect v2 Body Game"
game = BodyGameRuntime();
game.run();