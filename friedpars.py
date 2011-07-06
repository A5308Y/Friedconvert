#!/usr/bin/env python2
# -*- coding: utf-8 -*-

################### CONFIG ############################

languages = ["en", "sp", "fr", "pl", "ru"]
leclist = range(1,31) #[1,2]
convert = False
upload = False

HTML_OUTPUT_PATH = "/home/marvin/Desktop/Friedländer/lections/"

#HTML Templates and Colorcodes to use for the created html
HTMLRES_PATH = "HTMLRES"

colordic = {"Header":"#000066", "Text": "#0099cc"}
colordic["Wortschatz"] = "#99ffcc"
colordic["Grammatik"] ="#ff6699"
colordic[u'\xdcbungen'] = "#0099cc"
colordic[u'Fragen'] = "#0099cc"
colordic[u'Aufgaben'] = "#0099cc"

server_pictuer_path = "fileadmin/deutschkurs/"
merkdic = {"Header": server_pictuer_path+"merkzeichen-l.jpg", "Text": server_pictuer_path+"merkzeichen-t.jpg"}
merkdic["Wortschatz"] = server_pictuer_path+"merkzeichen-w.jpg"
merkdic["Grammatik"] =server_pictuer_path+"merkzeichen-g.jpg"
merkdic[u'\xdcbungen'] = server_pictuer_path+"merkzeichen-t.jpg"
merkdic[u'Fragen'] = server_pictuer_path+"merkzeichen-t.jpg"
merkdic[u'Aufgaben'] = server_pictuer_path+"merkzeichen-t.jpg"

###############################################################

import os, glob, hashing, writing, parsing
from helpers import message, read_html, create_directories, convert_to_html

###############################################################

def run(languages, leclist, convert = False):
  if convert:
    create_directories(leclist)
    convert_to_html(languages, leclist)
  
  LL_dict = {}
  for lang in languages:
    LL_dict[lang] = {}
  for lesson_nr in leclist:
    PATH = "../lections/lek"+str(lesson_nr)+"/"
    OUTFILE = PATH+"lek"+str(lesson_nr)+"_LL.html"
    path = "../lections/lek" + str(lesson_nr)
    
    for infile in glob.glob(os.path.join(path, "*lek"+str(lesson_nr)+"*.html")):
      lang = infile[-7:-5]
      if lang != "LL" and lang in languages:
        message("processing "+infile)

        parser = parsing.MyHTMLParser()
        dehasher = hashing.Dehasher(lesson_nr)
        writer = writing.Writer(dehasher, PATH, HTMLRES_PATH, colordic, merkdic)

        dehasher.inlist = []
        parser.feed(read_html(infile))
        snipdic = parser.snipdic

        if lang == 'en':
          writer.create_html(snipdic, OutsourceTXT = True)
          writer.write_html(HTML_OUTPUT_PATH+"lektion"+str(lesson_nr)+".tmpl")
        else:
          writer.create_html(snipdic)

        LL_dict[lang][dehasher.lesson_nr]=dehasher.inlist

  len_dict = {}
  for lesson_nr in leclist:
    len_dict[lesson_nr] = {}
    for lang in languages:
      len_dict[lesson_nr][lang] = len(LL_dict[lang][lesson_nr])
    len_sort = len_dict[lesson_nr].values()
    len_sort.sort()
    if len_sort[0] != len_sort[-1]:
      message("Different number of foreign language snippets in lection" + str(lesson_nr))
      message(len_dict[lesson_nr])
      
  writer.write_xml(HTML_OUTPUT_PATH+"locallang_deutschkurs.xml", LL_dict)
  
  #if upload:
    #os.system

###############################################################

if __name__ == '__main__':
  run(languages, leclist, convert)
