#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       bp_interfacelift.py
#       
#       Copyright 2010 Bruno Paulin <bruno@Fernand>
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
# Résolutions à télécharger
resolutions = ('1680x1050','1280x1024','1024x768')
########## REGLAGES

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

if __name__ == '__main__':

	#Préparation des dossier
	for reso in resolutions:
		dossier = os.path.join(os.path.expanduser('~'), 'Images', 'Wallpapers')

		try:
			os.makedirs(os.path.join(dossier,reso))
		except OSError:
			pass # les répertoires existent déjà
	page = urllib.urlopen('http://feeds.feedburner.com/InterfaceliftNewestWallpaper?format=xml')
	doc = parse(page)#'Ouverture' du xml
	items = doc.getElementsByTagName('item')
	nb=0

	for item in items:
		descri = get_value_tag('description', item )

		if not descri:
		   continue
		check_reso  = [reso for reso in resolutions if reso in descri]

		if check_reso:
			title = get_value_tag('title', item)
			guid = get_value_tag('guid', item)
			print title

			if not(title and guid):
				continu
			title = title.lower().replace(' ','').replace('-','').replace('.','')
			
			for reso in check_reso:
				filename = '%s_%s_%s.jpg' %( [node for node in guid.split('/') if node][-1].rjust(5, '0'),
										 title,
										  reso)
				file_path_save = os.path.join(dossier,reso,filename)

				if not os.path.isfile(file_path_save):
					print u"Téléchargement de %s pour la résolution %s" %(filename, reso)
					url = 'http://interfacelift.com/wallpaper_beta/grab/%s' % filename
					img_obj = urllib.urlopen(url)
					img_data = img_obj.read()
					
					if img_data :
					   file_obj = open(file_path_save, 'w')
					   file_obj.write(img_data)
					   file_obj.close()
