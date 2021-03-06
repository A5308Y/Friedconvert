#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from helpers import *

#################### WRITER ########################

class Writer(object):
  def __init__(self, dehasher, PATH, HTMLRES_PATH, colordic, merkdic):
    self.output = ''
    self.dehasher = dehasher
    self.lesson_nr = dehasher.lesson_nr
    self.PATH = PATH
    self.HTMLRES_PATH = HTMLRES_PATH
    self.colordic = colordic
    self.merkdic = merkdic

  def create_header(self, lektitle):
  #Write the Header
    #Read the lines of the different templates

    text = read_html(self.HTMLRES_PATH +"/Head.txt")
    text = text.replace("###LEKNR###", 'Lektion '+str(self.lesson_nr))
    text = text.replace("###LEKTITLE###", htmlize(lektitle))

    self.output += text

  def create_html(self, snipdic, OutsourceTXT = False):
    snipsecdict = snipdic["snipsecdict"]
    captionlist = snipdic["captionlist"]
    lektitle = captionlist[0]  #Hier muss noch was getan werden
    self.create_header(lektitle)
    self.create_content(captionlist, snipsecdict, OutsourceTXT)
    self.create_footer()

  def create_content(self, captionlist, snipsecdict, OutsourceTXT):
    #write the content
    for section in captionlist:
      if section == u"Übungen":
        pass
      else:
        content = snipsecdict[section]
        dehashed_dict = self.dehasher.dehash(content)
        content = self.dehasher.rebuild(dehashed_dict, section)
        content = htmlize(content)
        try:
          san_section= section.replace('/','')
          f = open(self.PATH+"lek"+str(self.lesson_nr)+"_"+san_section+".txt")
          content = f.read()
        except IOError:
          if OutsourceTXT:
            self.write_sec_txt(content, section)
        self.create_body(content, section)

  def create_body(self, content, section):
    text = read_html(self.HTMLRES_PATH +"/Body.txt")
    text = text.replace("###TEXT###", content)
    text = text.replace("###TITLE###", htmlize(section))
    if "Text" in section:
      text = text.replace("###COLOR###", self.colordic["Text"])
      text = text.replace("###MERKFILE###", self.merkdic["Text"])
      text = text.replace("###SECTION###", "Text")
    else:
      try:
        text = text.replace("###COLOR###", self.colordic[section])
        text = text.replace("###MERKFILE###", self.merkdic[section])
        text = text.replace("###SECTION###", section)
      except:
        text = text.replace("###SECTION###", "Text")
    self.output += text

  def create_footer(self):
  #Write the Footer
    text = read_html(self.HTMLRES_PATH +"/Foot.txt")
    self.output += text

  def write_xml(self, xmlfile, LL_dict):
    ##This is how an entry in the XML should look like:
    ##'<label index="label_lesson14_item1">phrases before the statement</label>'
    output = ''
    text = read_html(self.HTMLRES_PATH +"/XML-head.txt")
    output += text +"\n"

    for lang in LL_dict.iterkeys():
      output += '    <languageKey index="'+lang+'" type="array">\n'
      for lesson_nr in LL_dict[lang].iterkeys():
        sniplist = LL_dict[lang][lesson_nr]
        for item_nr in range(len(sniplist)):
          snippet = sanitize_snippet(sniplist[item_nr])
          snippet = xmlize(snippet)
          label = 'label_lesson_'+str(lesson_nr)+'_item'+str(item_nr+1)
          output += '      <label index="'+label+'">'+snippet+'</label>\n'
      output += '    </languageKey>\n'
    text = read_html(self.HTMLRES_PATH +"/XML-foot.txt")
    output += text

    output_file = codecs.open(xmlfile, 'w', "utf-8")
    output_file.write(output)
    output_file.close()

  def write_sec_txt(self, content, section):
    section = section.replace('/', '')
    output_file = codecs.open(self.PATH+"lektion"+str(self.lesson_nr)+"_"+section+".txt", 'w', "utf-8")
    output_file.write(content)
    output_file.close()

  def write_html(self, filename):
    outfile = codecs.open(filename, 'w', "utf-8")
    outfile.write(self.output)
    outfile.close()
################### //WRITER #######################