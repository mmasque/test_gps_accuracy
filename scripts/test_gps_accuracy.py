#!/usr/bin/env python

"""
This script tests the accuracy of a GPS sensor.

Usage:
	Run script at point A when a GPS has a confirmed fix.
	When instructed by terminal output, walk to point B in a straight line
	Input anything into command line when at B.

Author: Marcel Masque (marcel.masques@gmail.com)
Last modified: 18/10/19

Subscribes: ant_gps

"""
import rospy
from sensor_msgs.msg import NavSatFix

class AveragePoint():
	def __init__(self):
		self.total_lat = 0
		self.total_long = 0
		self.count = 0
		self.avg_lat = 0
		self.avg_long = 0
		self.locs = []
	def set_averages(self):
		self.avg_lat = self.total_lat/self.count
		self.avg_long = self.total_long/self.count
	
	def test_gps_accuracy(self, data):
		"Takes in gps message data and tests accuracy when walking along a line"
		self.locs.append((data.latitude, data.longitude))
		self.total_lat += data.latitude
		self.total_long += data.longitude
		self.count += 1
		self.set_averages()

	def listen_gps_data(self, topic_name, point):
		rospy.init_node('gps_listener', disable_signals=True)
		rospy.Subscriber(topic_name, NavSatFix, self.test_gps_accuracy)
		rate = rospy.Rate(1)
		while not (rospy.is_shutdown()):
			rospy.loginfo(self.count)
			
			if self.count > 60:
				return
			rate.sleep()			
class PointList():
	def __init__(self):
		self.locs = []
		self.count = 0
	def test_gps_accuracy(self, data):
		"Takes in gps message data and tests accuracy when walking along a line"
		self.locs.append((data.latitude, data.longitude))
		self.count += 1
	def listen_gps_data(self, topic_name, point):
		rospy.init_node('gps_listener', disable_signals=True)
		rospy.Subscriber(topic_name, NavSatFix, self.test_gps_accuracy)
		rate = rospy.Rate(1)
		while not (rospy.is_shutdown()):
			rospy.loginfo(self.count)
			if self.count > 60:
				return
			rate.sleep()
		

def get_average_point():
	point = AveragePoint()
	point.listen_gps_data('ant_gps', point)
	avg = point.avg_lat, point.avg_long
	rospy.loginfo(avg)
	return avg
def get_list_of_points():
	points = PointList()
	points.listen_gps_data('ant_gps', points)
	lst = points.locs
	rospy.loginfo(lst)
	return lst

A = get_average_point()
raw_input("press anything to continue when at point B: ")
B= get_average_point()
raw_input("press anything to begin walk: ")
points_along_BA = get_list_of_points()
