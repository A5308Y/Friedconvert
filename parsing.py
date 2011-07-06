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
    #self.text = ''
    self.refs = ''

  def handle_starttag(self, tag, attributes):
    if tag == 'i':
      self.starttag = u'!!?i?!!'
      self.endtag = u'!!?/i?!!'
    else:
      self.starttag = u''
      self.endtag = u''

  def handle_entityref(self, name):
    if name in ["shy", "nbsp"]: #All the problematic charrefs
      pass
    else:
      self.snipdic["snipsecdict"][self.section] = self.snipdic["snipsecdict"][self.section] + u"&"+name+";"
      self.snipdic["sniplist"][-1]+= u"&"+name+";"

  def handle_data(self, text):
    snipsecdict = self.snipdic["snipsecdict"]
    tagtext = repr(self.get_starttag_text())
    if tagtext.count("BODY") == 1:
      self.active = True

    if self.active:
      if text != '':   
        snippet = unicode(text)
        
        self.snipdic["sniptext"] += snippet
        snippet = self.starttag+snippet+self.endtag

        #Determine the caption by the given key words and some thoughts about how captions show up in
        #the text. This works a lot better than the alternative methods with headings, but some keywords
        #show up in the same form somewhere else in the text. Needs less work in the rawdocs than
        #the alternative though.

        seccodes = ["Grammatik","Wortschatz", u"Übungen"]#"Fragen", "Aufgaben", "Aufgabe",
        sec = sanitize_snippet(text)
        if sec !=  '':
          if sec in seccodes or (sec[0:4] == "Text" and sec[4:8].replace(" ","").isdigit() and len(sec) <= 9 and not ":" in sec):
            caption = sec
            self.section = sanitize_snippet(snippet)
            self.snipdic["captionlist"].append(caption)
            snipsecdict[self.section] = ''
            return

      #Alternative way of determining the captions via the Headings (kind of works, but the Headings,
      #are used very inconsistently. So this would require quite some work in the raw documents by
      #hand.
      
      #for i in range(1,7):
        #if sanitize_snippet(text) !=  '':
          #if tagtext.count("H"+str(i)) == 1 :
            #caption = sanitize_snippet(text)
            #self.section = sanitize_snippet(snippet)
            #self.snipdic["captionlist"].append(caption)
            #snipsecdict[self.section] = ''
            #return

      
      snipsecdict[self.section] = snipsecdict[self.section] + snippet
      self.snipdic["sniplist"].append(snippet)
##################### //PARSER #######################