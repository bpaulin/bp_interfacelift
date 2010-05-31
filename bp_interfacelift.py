#!/usr/bin/env python
# -*- coding: utf-8 -*-
#	   bp_interfacelift.py
#	   
#	   Copyright 2010 Bruno Paulin <brunopaulin@bpaulin.net>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.


########## SETTINGS
# Resolutions to choose among this list
# 2560x1600, 2560x1440, 2560x1024, 1920x1200, 1920x1080, 1680x1050, 1600x1200
# 1600x900, 1440x900, 1400x1050, 1280x1024, 1280x960, 1280x800, 1280x720
# 1024x1024, 1024x768, 1024x600, 800x480, 640x960, 480x272, 320x480, 320x240
Resolutions = ('1680x1050','1280x1024','1024x768')
# Directory in which the 'wallpapers' directory will be
SaveTo = 'Images'
# interfacelift feed url
UrlXml = 'http://feeds.feedburner.com/InterfaceliftNewestWallpaper?format=xml'
# Picture url (%s will be the picture name)
UrlPicture = 'http://interfacelift.com/wallpaper_beta/grab/%s'
#
UrlDirPreview = 'http://interfacelift.com/wallpaper_beta/previews/'
########## SETTINGS


from xml.dom.minidom import parse
import os
import urllib
import getopt, sys


def GetValueTag(name_tag,root_tag):#############################################
	tag = root_tag.getElementsByTagName(name_tag)
	if tag:
		tag = tag[0]
		first_child = tag.firstChild
		return None if not first_child else first_child.data
	else:
		return None
#############################################def GetValueTag(name_tag,root_tag):


def GetImage(url, path_save):##################################################
	print u"Downloading %s" % (path_save)
	img_obj = urllib.urlopen(url)
	img_data = img_obj.read()
	
	# Saving picture
	if img_data :
		file_obj = open(path_save, 'w')
		file_obj.write(img_data)
		file_obj.close()
#######################################################def GetImage(url, name):


def CheckDir():#################################################################
	for reso in Resolutions:
		dir = os.path.join(os.path.expanduser('~'), SaveTo, 'Wallpapers')
		# Making directories
		try:
			os.makedirs(os.path.join(dir,reso))
		except OSError: # Directory exists
			pass
	return dir
#################################################################def CheckDir():


def Download():#################################################################
	# Checking directories
	dir = CheckDir()

	# Opening xml
	page = urllib.urlopen(UrlXml)
	doc = parse(page)
	items = doc.getElementsByTagName('item')

	# For each pictures
	for item in items:
		# Checking resolutions
		descri = GetValueTag('description', item)
		if not descri:
		   continue
		check_reso = [reso for reso in Resolutions if reso in descri]#resolutions wanted for this picture
		
		if check_reso:
			# Getting picture's details
			title = GetValueTag('title', item)#picture title
			guid = GetValueTag('guid', item)#picture's page url
			if not(title and guid):
				continue
			print title
			name = [preview for preview in descri.split(' ') if preview.count('src="%s'%UrlDirPreview)][0]\
					.replace('src="%s'%UrlDirPreview,'').replace('.jpg"', '')
			
			# For each resolutions
			for reso in check_reso:
				# Checking if file exists
				filename = '%s_%s.jpg' %( name, reso)
				file_path_save = os.path.join(dir,reso,filename)
				if not os.path.isfile(file_path_save):
					
					# Downloading picture
					url = UrlPicture % filename
					GetImage(url, file_path_save)
#################################################################def Download():


def Synchro():##################################################################
	print u"Synchro"
	dir = CheckDir()
	# Getting pictures list
	images = list()
	for reso in Resolutions:
		liste = os.listdir(os.path.join(dir,reso))
		liste = [os.path.splitext(item)[0].rstrip(reso) for item in liste]
		images.extend(liste)
	images = list(set(images))
	images.sort()
	# Downloading missing pictures
	for item in images:
		for reso in Resolutions:
			filename = '%s%s.jpg' %( item, reso)
			file_path_save = os.path.join(dir,reso,filename)
			if not os.path.isfile(file_path_save):
				
				# Downloading picture
				url = UrlPicture % filename
				GetImage(url, file_path_save)		
##################################################################def Synchro():


def Help(problem):##############################################################
	print """
bp_interfacelift comes with ABSOLUTELY NO WARRANTY.  This is free software, and you are welcome to redistribute it under certain conditions.  See the GNU
General Public Licence for details.

bp_interfacelift is a wallpaper download program for several resolutions. Pictures are downloaded from http://www.interfacelift.com

Options
-d --download   Download new pictures
-s --synchro    Download pictures missing for some resolution
-h --help       Print this message
"""
	sys.exit(problem)
##############################################################def Help(problem):


def Arguments():################################################################
	download = False
	synchro = False
	help = False
	problem = False
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hds", ["help", "download", "synchro"])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		problem = True
	else:
		for o, a in opts:
			if o in ("-h", "--help"):
				help = True
			elif o in ("-s", "--synchro"):
				synchro = True
			elif o in ("-d", "--download"):
				download = True	
	return (problem, download, synchro, help)
################################################################def Arguments():


if __name__ == '__main__':
	(problem, download, synchro, help) = Arguments()
	if problem:
		Help(1)
	elif help:
		Help(0)
	else:
		if (not synchro or download):
			Download()
		if synchro:
			Synchro()
