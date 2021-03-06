import time
import jetson.inference
import jetson.utils
import os
import datetime
import argparse
import sys
import cv2
import math

import numpy as np

# Side-view angles

def squat_right_knee_angle(pose):
    print("---------------------") 

    # Distance formula = abs sqrt((x2-x1)^2 + (y2-y1)^2)

    # Right upper leg distance
    right_knee_idx = pose.FindKeypoint(14)
    right_hip_idx = pose.FindKeypoint(12)

    if (right_knee_idx < 0 or right_hip_idx < 0):
        return
    
    right_knee = pose.Keypoints[right_knee_idx]
    right_hip = pose.Keypoints[right_hip_idx]

    # right_upper_leg_distance = abs(math.sqrt((right_hip.x - right_knee.x)^2 + (right_hip.y - right_knee.y)^2))
    right_upper_leg_slope = abs(calcSlope(right_knee, right_hip))
    print("Right Upper Leg Slope: " + str(right_upper_leg_slope))

    # Right lower leg distance
    right_ankle_idx = pose.FindKeypoint(16)

    if (right_ankle_idx < 0):
        return

    right_ankle = pose.Keypoints[right_ankle_idx]

    # right_lower_leg_distance = abs(math.sqrt((right_ankle.x - right_knee.x)^2 + (right_ankle.y - right_knee.y)^2))
    right_lower_leg_slope = abs((right_ankle.y - right_knee.y)/(right_ankle.x - right_knee.x))
    print("Right Lower Leg Slope: " + str(right_lower_leg_slope))
   
    # Calculate knee angle of right knee 
    right_knee_angle = calcAngle(right_upper_leg_slope, right_lower_leg_slope)
    #if right_knee_angle < 0:
    #    right_knee_angle += 180

    print("Right knee angle = " + str(right_knee_angle))

    # Desired angle is 180-125 = 55 degrees
    print("     Off by " + str(right_knee_angle - (180-125)) + " degrees")
    print("---------------------") 
    return right_knee_angle

def squat_left_knee_angle(pose):
    print("---------------------") 

    # Distance formula = abs sqrt((x2-x1)^2 + (y2-y1)^2)
    
    # Left upper leg distance
    left_knee_idx = pose.FindKeypoint(13)
    left_hip_idx = pose.FindKeypoint(11)

    if (left_knee_idx < 0 or left_hip_idx < 0):
        return

    left_knee = pose.Keypoints[left_knee_idx]
    left_hip = pose.Keypoints[left_hip_idx]

    # left_upper_leg_distance = abs(math.sqrt((left_hip.x - left_knee.x)^2 + (left_hip.y - left_knee.y)^2))
    left_upper_leg_slope = abs(calcSlope(left_knee, left_hip))
    print("Left Upper Leg Slope: " + str(left_upper_leg_slope))

    # Left lower leg distance
    left_ankle_idx = pose.FindKeypoint(15)

    if (left_ankle_idx < 0):
        return

    left_ankle = pose.Keypoints[left_ankle_idx]

    # left_lower_leg_distance = abs(math.sqrt((left_ankle.x - left_knee.x)^2 + (left_ankle.y - left_knee.y)^2))
    left_lower_leg_slope = abs(calcSlope(left_knee, left_ankle))

    print("Left Lower Leg Slope: " + str(left_lower_leg_slope))
   
    # Calculate knee angle of left knee 
    left_knee_angle = calcAngle(left_upper_leg_slope, left_lower_leg_slope)
    #if right_knee_angle < 0:
    #    right_knee_angle += 180

    print("Left knee angle = " + str(left_knee_angle))

    # Desired angle is 180-125 = 55 degrees
    print("     Off by " + str(left_knee_angle - (180-125)) + " degrees")
    print("-----------------------")
    return left_knee_angle

def squat_right_back_angle(pose):
    print("---------------------") 

    # Distance formula = abs sqrt((x2-x1)^2 + (y2-y1)^2)

    # Right back distance
    neck_idx = pose.FindKeypoint(17)
    right_hip_idx = pose.FindKeypoint(12)

    if (neck_idx < 0 or right_hip_idx < 0):
        return
    
    neck = pose.Keypoints[neck_idx]
    right_hip = pose.Keypoints[right_hip_idx]

    # right_upper_leg_distance = abs(math.sqrt((right_hip.x - right_knee.x)^2 + (right_hip.y - right_knee.y)^2))
    right_back_slope = abs(calcSlope(neck, right_hip))
    print("Right Back Slope: " + str(right_back_slope))

    # Right upper leg distance
    right_knee_idx = pose.FindKeypoint(14)

    if (right_knee_idx < 0):
        return

    right_knee = pose.Keypoints[right_knee_idx]

    # right_lower_leg_distance = abs(math.sqrt((right_ankle.x - right_knee.x)^2 + (right_ankle.y - right_knee.y)^2))
    right_upper_leg_slope = abs(calcSlope(right_hip, right_knee))
    print("Right Upper Leg Slope: " + str(right_upper_leg_slope))
   
    # Calculate knee angle of right knee 
    back_angle = calcAngle(right_upper_leg_slope, right_back_slope)
    #if right_knee_angle < 0:
    #    right_knee_angle += 180

    print("Hip angle = " + str(back_angle))

    # Desired angle is 55 degrees
    angle_difference = back_angle - 55
    print("     Off by " + str(angle_difference) + " degrees")

    print("---------------------") 
    return back_angle

def squat_left_back_angle(pose):
    print("---------------------") 

    # Distance formula = abs sqrt((x2-x1)^2 + (y2-y1)^2)
    
    # Left upper leg distance
    neck_idx = pose.FindKeypoint(17)
    left_hip_idx = pose.FindKeypoint(11)

    if (neck_idx < 0 or left_hip_idx < 0):
        return
    
    neck = pose.Keypoints[neck_idx]
    left_hip = pose.Keypoints[left_hip_idx]

    # right_upper_leg_distance = abs(math.sqrt((right_hip.x - right_knee.x)^2 + (right_hip.y - right_knee.y)^2))
    left_back_slope = abs(calcSlope(neck, left_hip))
    print("Left Back Slope: " + str(left_back_slope))

    # Left upper leg distance
    left_knee_idx = pose.FindKeypoint(13)

    if (left_knee_idx < 0):
        return

    left_knee = pose.Keypoints[left_knee_idx]

    # right_lower_leg_distance = abs(math.sqrt((right_ankle.x - right_knee.x)^2 + (right_ankle.y - right_knee.y)^2))
    left_upper_leg_slope = abs(calcSlope(left_hip, left_knee))
    print("Left Upper Leg Slope: " + str(left_upper_leg_slope))
   
    # Calculate knee angle of right knee 
    back_angle = calcAngle(left_upper_leg_slope, left_back_slope)
    #if right_knee_angle < 0:
    #    right_knee_angle += 180

    print("Back angle = " + str(back_angle))

    # Desired angle is 55 degrees
    print("     Off by " + str(back_angle - 55) + " degrees")
    print("---------------------") 
    return back_angle

# Percentage correctness calculation based on the angle
def squat_scoring(knee_angle, back_angle):
    print("####################")

    # Anything below the range is 100% and above the range is 0%
    min_range = 5.0
    max_range = 35.0
    range = min_range - max_range

    perfect_knee_angle = float(55.0)
    perfect_back_angle = float(55.0)

    # Positive Difference
    knee_angle_difference = abs(perfect_knee_angle - knee_angle)
    back_angle_difference = abs(perfect_back_angle - back_angle)

    # % = (value - min)/(max - min)
    if knee_angle_difference <= max_range and knee_angle_difference >= min_range:
        knee_score = abs(100*((knee_angle_difference - max_range) / range))
    else:
        knee_score = 0.0

    if back_angle_difference <= max_range and knee_angle_difference >= min_range:
        back_score = abs(100*((back_angle_difference - max_range) / range))
    else:
        back_score = 0.0

    final_score = (knee_score + back_score) / 2
    
    # Uses +/- difference instead of +
    knee_angle_difference = perfect_knee_angle - knee_angle
    if knee_angle_difference < -1 * min_range:
        print("Lower hips to break parallel and have hip joint below the knee. Score = {:.3f}%".format(knee_score))
    elif knee_angle_difference > min_range:
        print("Squat is too deep. Raise hips to have the hip joint parallel to knee. Score = {:.3f}%".format(knee_score))
    else:
        print("Great hip angle!")

    back_angle_difference = perfect_back_angle - back_angle
    if back_angle_difference < -1 * min_range:
        print("Lean forward to prevent excessive stress on the lower back. Score = {:.3f}%".format(back_score))
    elif back_angle_difference > min_range:
        print("Keep chest upward and look straight ahead. Score = {:.3f}%".format(back_score))
    else:
        print("Great back angle!")

    return final_score

# Calculates the slope of a line based on 2 points
def calcSlope(point1, point2):  # point1 and point2 refers to 2 points in the resnet model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    return (point2.y-point1.y)/(point2.x-point1.x)

# Calculate the distance of a line based on 2 points
def calcDistance(point1, point2):
    return abs(math.sqrt((point1.x-point2.x)^2 + (point1.y-point2.y)^2))

# Calculates the angle in degress of two intersecting lines given the slope
def calcAngle(slope1, slope2): 
    angle = (math.degrees(abs(math.atan((slope1-slope2)/(1 + slope1*slope2)))))
    #return angle if angle < 0 else angle+180
    return angle