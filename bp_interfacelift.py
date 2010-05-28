#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       bp_interfacelift.py
#       
#       Copyright 2010 Bruno Paulin <brunopaulin@bpaulin.net>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

########## SETTINGS
# Resolutions
# 2560x1600, 2560x1440, 2560x1024, 1920x1200, 1920x1080, 1680x1050, 1600x1200
# 1600x900, 1440x900, 1400x1050, 1280x1024, 1280x960, 1280x800, 1280x720
# 1024x1024, 1024x768, 1024x600, 800x480, 640x960, 480x272, 320x480, 320x240
# resolutions = ('1680x1050','1280x1024','1024x768')
Resolutions = ('1680x1050','1280x1024','1024x768')
SaveTo = 'Images'
########## SETTINGS

from xml.dom.minidom import parse
import os
import urllib


def get_value_tag(name_tag,root_tag):
	tag = root_tag.getElementsByTagName(name_tag)
	if tag:
		tag = tag[0]
		first_child = tag.firstChild
		return None if not first_child else first_child.data
	else:
		return None
#def get_value_tag(name_tag,root_tag):

if __name__ == '__main__':

	# Checking directories
	for reso in Resolutions:
		dir = os.path.join(os.path.expanduser('~'), SaveTo, 'Wallpapers')
		# Making directories
		try:
			os.makedirs(os.path.join(dir,reso))
		except OSError: # Directory exists
			pass

	# Opening xml
	page = urllib.urlopen('http://feeds.feedburner.com/InterfaceliftNewestWallpaper?format=xml')
	doc = parse(page)
	items = doc.getElementsByTagName('item')

	# For each pictures
	for item in items:
		# Checking resolutions
		descri = get_value_tag('description', item)
		if not descri:
		   continue
		check_reso = [reso for reso in Resolutions if reso in descri]#resolutions wanted for this picture
		
		if check_reso:
			# Getting picture's detail
			title = get_value_tag('title', item)#picture title
			guid = get_value_tag('guid', item)#picture's page url
			if not(title and guid):
				continue
			print title
			name = title.lower().replace(' ','').replace('-','').replace('.','')#picture name
			
			# For each resolutions
			for reso in check_reso:
				# Checking if file exists
				filename = '%s_%s_%s.jpg' %( [node for node in guid.split('/') if node][-1].rjust(5, '0'),
										 name,
										  reso)
				file_path_save = os.path.join(dir,reso,filename)
				if not os.path.isfile(file_path_save):
					# Downloading picture
					print u"Downloading %s for resolution %s" %(filename, reso)
					url = 'http://interfacelift.com/wallpaper_beta/grab/%s' % filename
					img_obj = urllib.urlopen(url)
					img_data = img_obj.read()	
					# Saving picture
					if img_data :
					   file_obj = open(file_path_save, 'w')
					   file_obj.write(img_data)
					   file_obj.close()
