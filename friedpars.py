#!/usr/bin/env python2
# -*- coding: utf-8 -*-

################### CONFIG ############################

lesson_nr = 15

global label_nr
global inlist

inlist = []
label_nr = 1

PATH = "../lek"+str(lesson_nr)+"/"

OUTFILE = PATH+"lek"+str(lesson_nr)+"_LL.html"
SRCFILE = PATH+"lek"+str(lesson_nr)+".html"
XMLFILE = PATH+"lek"+str(lesson_nr)+".xml"

#HTML Templates and Colorcodes to use in the write_html function
HTMLRES_Path = "HTMLRES"

colordic = {"Header":"#000066", "Text": "#0099cc"}
colordic["Wortschatz"] = "#99ffcc"
colordic["Grammatik"] ="#ff6699"
colordic[u'\xdcbungen'] = "#0099cc"
colordic[u'Fragen'] = "#0099cc"
colordic[u'Aufgaben'] = "#0099cc"

merkdic = {"Header":"merkzeichen-w.jpg", "Text": "merkzeichen-w.jpg"}
merkdic["Wortschatz"] = "merkzeichen-w.jpg"
merkdic["Grammatik"] ="merkzeichen-w.jpg"
merkdic[u'\xdcbungen'] = "merkzeichen-w.jpg"
merkdic[u'Fragen'] = "merkzeichen-w.jpg"
merkdic[u'Aufgaben'] = "merkzeichen-w.jpg"



###############################################################


import codecs, os
from HTMLParser import HTMLParser

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

  def handle_data(self, text):
    snipsecdict = self.snipdic["snipsecdict"]
    tagtext = repr(self.get_starttag_text())
    if tagtext.count("BODY") == 1:
      self.active = True
      
    if self.active:
      snippet = unicode(text)
      self.snipdic["sniptext"] += snippet

      for i in range(1,7):
        if sanitize_snippet(text, False) !=  '':
          if tagtext.count("H"+str(i)) == 1 :
            caption = sanitize_snippet(text, False)
            self.section = sanitize_snippet(snippet, False)
            self.snipdic["captionlist"].append(caption)
            snipsecdict[self.section] = ''
            return

      snipsecdict[self.section] = snipsecdict[self.section] + snippet
      self.snipdic["sniplist"].append(snippet)

class Dehasher(object):
  def __init__(self):
    pass


  def dehash(self, string):
    outsnips = []
    insnips = []
    i = 0
    for snippet in string.split("#"):
      sanitize_snippet(snippet, False)
      if snippet != '':
        if isodd(i):
          insnips.append(snippet)
        else:
          outsnips.append(snippet)
      i+=1
    return {"outsnips": outsnips, "insnips":insnips}


  def rebuild(self, dehashed_dict, section):
    ##rebuilds a string from an outsnips-insnips dictionary, replacing the insnips with
    ##a Label.
    global label_nr
    global inlist
    ins = dehashed_dict["insnips"]
    inlist.extend(ins)
    outs = dehashed_dict["outsnips"]
    new_text = ''
    i=1
    for snip in outs:
      new_text = new_text + snip
      if len(ins) != 0 and i != len(outs):
        #new_text = new_text + "###_LL_LABEL_LESSON"+str(lesson_nr)+"_SECTION_"+section[0:3]+"_ITEM"+str(i)+"###"
        new_text = new_text + "###_LL_LABEL_LESSON"+str(lesson_nr)+"_ITEM"+str(label_nr)+"###"
        i+=1
        label_nr +=1
    return new_text  


#reads the Libre-Office-generated html and returns the whole text in utf-8


def isodd(number):
  if number%2 ==0:
    return False
  else:
    return True

def read_html(html_file):
  input_file = codecs.open(html_file, 'r', "utf-8")
  text = ""
  for line in input_file.readlines():
    text = text + line
  input_file.close()
  return text

def write_sec_txt(content, section):
  output_file = codecs.open(PATH+"lek"+str(lesson_nr)+"_"+section+".txt", 'w', "utf-8")
  output_file.write(content)
  output_file.close()
    


#Clears a line of HTML of some annoying symbols.

def sanitize_snippet(snippet, onlytabs):
  if not onlytabs:
    snippet = snippet.replace('\n',' ')
    snippet = snippet.replace('#','')
    snippet = snippet.strip()
  snippet = snippet.replace('\t','')
  return snippet

#Checks if a snippet is a Heading by searching its HTML_Tag for H#
#stores it in a given list and returns the caption

def capture_caption(html_tag, snippet):
  for i in xrange(10):
    snippet = sanitize_snippet(snippet, False)
    if html_tag.count("H"+str(i)) == 1 and snippet!='':
      caption = snippet
      return caption
    elif html_tag.count("H"+str(i)) > 1:
      pass
      #print "SOMETHINGS WRONG!!!! with the Caption tags. Search for \"H"+str(i)+"\" "
       ##Da müssen noch die Style Vorgaben für Hx ausgeblendet werden...     


def htmlize(content):
  #translates the content from utf-8 to html
  #There's probably a better way...
  
  content = content.replace("\n", "<br>")
  content = content.replace(unichr(252), "&uuml;")
  content = content.replace(unichr(246), "&ouml;")
  content = content.replace(unichr(214), "&Ouml;")
  content = content.replace(unichr(220), "&Uuml;")
  content = content.replace(unichr(223), "&szlig;")
  content = content.replace(unichr(228), "&auml;")
  content = content.replace(unichr(196), "&Auml;")
  content = content.replace(unichr(8222), "\"")
  content = content.replace(unichr(8221), "\"")
  content = content.replace(unichr(8220), "\"")
  
  content = content.replace(unichr(8211), "-")
  content = content.replace(unichr(8212), "-")

  return content

def write_html(snipdic):
  #TODO: Hier noch die snapseclist benutzen für die
  #automatische Erstellung von verschiedenen Abschnitten

  snipsecdict = snipdic["snipsecdict"]
  captionlist = snipdic["captionlist"]
  lektitle = captionlist[0]
  captionlist = captionlist[1:len(captionlist)]
  outfile = codecs.open(OUTFILE, 'w', "utf-8")

#Write the Header
  #Read the lines of the different templates
  for vorlage in ["Head.txt"]:
    vorfile = codecs.open(HTMLRES_Path + "/"+vorlage, 'r', "utf-8")
    lines = vorfile.readlines()
    vorfile.close()
    #And write them in the new file, replacing ###TEXT### with the content
    for line in lines:
      line = line.replace("###COLOR###", colordic["Header"])
      line = line.replace("###LEKNR###", 'Lektion '+str(lesson_nr))
      line = line.replace("###LEKTITLE###", lektitle)
      outfile.write(line)


#write the content
  for section in captionlist:
    #if osPATH+"lek"+str(lesson_nr)+"_"+section+".txt":

    try:
      f = open(PATH+"lek"+str(lesson_nr)+"_"+section+".txt")
      content = f.read()
    except IOError:
      content = snipsecdict[section]
      dehasher = Dehasher()
      dehashed_dict = dehasher.dehash(content)
      content = dehasher.rebuild(dehashed_dict, section)
      content = htmlize(content)
      write_sec_txt(content, section)

    for vorlage in ["SectionTitle.txt"]:
      vorfile = codecs.open(HTMLRES_Path + "/"+vorlage, 'r', "utf-8")
      lines = vorfile.readlines()
      vorfile.close()
        #And write them in the new file, replacing ###TEXT### with the content
      for line in lines:
        line = line.replace("###TITLE###", htmlize(section))
        if "Text" in section:
          line = line.replace("###COLOR###", colordic["Text"])
          line = line.replace("###MERKFILE###", merkdic["Text"])
        else:
          try:
            line = line.replace("###COLOR###", colordic[section])
            line = line.replace("###MERKFILE###", merkdic[section])
          except:
            line = line.replace("###COLOR###", "#000066")
            line = line.replace("###MERKFILE###", "merkzeichen-w.jpg")
            
        outfile.write(line)

    for vorlage in ["Body.txt"]:
      vorfile = codecs.open(HTMLRES_Path + "/"+vorlage, 'r', "utf-8")
      lines = vorfile.readlines()
      vorfile.close()
        #And write them in the new file, replacing ###TEXT### with the content
      for line in lines:
        line = line.replace("###TEXT###", content)
        if "Text" in section:
          line = line.replace("###COLOR###", colordic["Text"])
        else:
          try:
            line = line.replace("###COLOR###", colordic[section])
          except:
            line = line.replace("###COLOR###", "#000066")
          
        outfile.write(line)

#Write the Footer       
  for vorlage in ["Foot.txt"]:
    vorfile = codecs.open(HTMLRES_Path + "/"+vorlage, 'r', "utf-8")
    lines = vorfile.readlines()
    vorfile.close()
    for line in lines:
      outfile.write(line)
      
  outfile.close()


def write_xml(sniplist):
  ##This is how an entry in the XML should look like:
  ##'<label index="label_lesson14_item1">phrases before the statement</label>'
  output_file = codecs.open(XMLFILE, 'w', "utf-8")
  for item_nr in range(len(sniplist)):
    output_file.write('<label index="label_lesson_'+str(lesson_nr)+'_item'+str(item_nr+1)+'">'+sniplist[item_nr]+'</label>\n')
  output_file.close()

os.system('soffice -accept="socket,port=8100;urp;"')
os.system('python DocumentConverter.py E-lek-'+str(lesson_nr)+'* lek'+str(lesson_nr)+'.html')

parser = MyHTMLParser()
dehasher = Dehasher()

parser.feed(read_html(SRCFILE))
snipdic = parser.snipdic
write_html(snipdic)
write_xml(inlist)