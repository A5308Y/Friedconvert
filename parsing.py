#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from helpers import *
from HTMLParser import HTMLParser

################## PARSER ##############################

class MyHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.snipdic = {"captionlist" : []}
    self.snipdic["snipsecdict"] = {}
    self.snipdic["sniplist"] = []
    self.section = 'Header'
    self.snipdic["snipsecdict"]['Header']=''
    self.snipdic["sniptext"] = ''
    self.active = False
    self.inlist = []

  def handle_data(self, text):
    snipsecdict = self.snipdic["snipsecdict"]
    tagtext = repr(self.get_starttag_text())
    if tagtext.count("BODY") == 1:
      self.active = True

    if self.active:
      snippet = unicode(text)
      self.snipdic["sniptext"] += snippet

      for i in range(1,7):
        if sanitize_snippet(text) !=  '':
          if tagtext.count("H"+str(i)) == 1 :
            caption = sanitize_snippet(text)
            self.section = sanitize_snippet(snippet)
            self.snipdic["captionlist"].append(caption)
            snipsecdict[self.section] = ''
            return

      snipsecdict[self.section] = snipsecdict[self.section] + snippet
      self.snipdic["sniplist"].append(snippet)
##################### //PARSER #######################