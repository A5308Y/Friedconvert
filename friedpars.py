#!/usr/bin/env python2
# -*- coding: utf-8 -*-

################### CONFIG ############################
#HTML Templates and Colorcodes to use in the write_html function
HTMLRES_Path = "HTMLRES"

colordic = {"Header":"#000066", "Text": "#0099cc"}
colordic["Wortschatz"] = "#99ffcc"
colordic["Grammatik"] ="#ff6699"
colordic[u'\xdcbungen'] = "#0099cc"
colordic[u'Fragen'] = "#0099cc"
colordic[u'Aufgaben'] = "#0099cc"

merkdic = {"Header":"merkzeichen-l.jpg", "Text": "merkzeichen-t.jpg"}
merkdic["Wortschatz"] = "merkzeichen-w.jpg"
merkdic["Grammatik"] ="merkzeichen-g.jpg"
merkdic[u'\xdcbungen'] = "merkzeichen-t.jpg"
merkdic[u'Fragen'] = "merkzeichen-t.jpg"
merkdic[u'Aufgaben'] = "merkzeichen-t.jpg"

###############################################################

import codecs, os, glob, cgi
from HTMLParser import HTMLParser

global label_nr

label_nr = 1

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
        if sanitize_snippet(text, False) !=  '':
          if tagtext.count("H"+str(i)) == 1 :
            caption = sanitize_snippet(text, False)
            self.section = sanitize_snippet(snippet, False)
            self.snipdic["captionlist"].append(caption)
            snipsecdict[self.section] = ''
            return

      snipsecdict[self.section] = snipsecdict[self.section] + snippet
      self.snipdic["sniplist"].append(snippet)
##################### //PARSER #######################

##################### DEHASHER #######################

class Dehasher(object):
  def __init__(self, lesson_nr):
    self.inlist = []
    self.lesson_nr = lesson_nr

  def dehash(self, string):
    outsnips = []
    insnips = []
    i = 0
    for snippet in string.split("#"):
      sanitize_snippet(snippet, False) ##### Hier snippet = san... ???
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
    ins = dehashed_dict["insnips"]
    self.inlist.extend(ins)
    outs = dehashed_dict["outsnips"]
    new_text = ''
    i=1
    for snip in outs:
      new_text = new_text + snip
      if len(ins) != 0 and i != len(outs):
        new_text = new_text + "###_LL_LABEL_LESSON_"+str(self.lesson_nr)+"_ITEM"+str(label_nr)+"###"
        i+=1
        label_nr +=1
    return new_text

#################### //DEHASHER ####################

#################### WRITER ########################

class Writer(object):
  def __init__(self, dehasher, PATH):
    self.output = ''
    self.dehasher = dehasher
    self.lesson_nr = dehasher.lesson_nr
    self.PATH = PATH

  def create_header(self, lektitle):
  #Write the Header
    #Read the lines of the different templates

    text = read_html(HTMLRES_Path +"/Head.txt")
    text = text.replace("###COLOR###", colordic["Header"])
    text = text.replace("###LEKNR###", 'Lektion '+str(self.lesson_nr))
    text = text.replace("###LEKTITLE###", htmlize(lektitle))
    
    self.output += text

  def create_html(self, snipdic, OutsourceTXT = False):
    snipsecdict = snipdic["snipsecdict"]
    captionlist = snipdic["captionlist"]
    try:
      lektitle = captionlist[0]
    except IndexError:
      message("Problem with finding captions. Probably no Hx-tags in the file.")
      return
    captionlist = captionlist[1:len(captionlist)]
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
        self.create_sec_title(section)
        self.create_body(content, section)

  def create_sec_title(self, section):
    #Create a section heading in the HTML document
    text = read_html(HTMLRES_Path +"/SectionTitle.txt")        
    text = text.replace("###TITLE###", htmlize(section))
    if "Text" in section:
      text = text.replace("###COLOR###", colordic["Text"])
      text = text.replace("###MERKFILE###", merkdic["Text"])
    else:
      try:
        text = text.replace("###COLOR###", colordic[section])
        text = text.replace("###MERKFILE###", merkdic[section])
      except:
        text = text.replace("###COLOR###", "#000066")
        text = text.replace("###MERKFILE###", "merkzeichen-w.jpg")
    self.output += text

  def create_body(self, content, section):
    text = read_html(HTMLRES_Path +"/Body.txt")
    text = text.replace("###TEXT###", content) #content.decode('utf-8', errors='ignore')#CODEC PROBLEM!!!
    if "Text" in section:
      text = text.replace("###COLOR###", colordic["Text"])
    else:
      try:
        text = text.replace("###COLOR###", colordic[section])
      except:
        text = text.replace("###COLOR###", "#000066")
    self.output += text

  def create_footer(self):
  #Write the Footer
    text = read_html(HTMLRES_Path +"/Foot.txt")
    self.output += text

  def write_xml(self, xmlfile, LL_dict):
    ##This is how an entry in the XML should look like:
    ##'<label index="label_lesson14_item1">phrases before the statement</label>'
    output = ''
    text = read_html(HTMLRES_Path +"/XML-head.txt")
    output += text
    
    for lang in LL_dict.iterkeys():
      #output_file.write('<languageKey index="'+lang+'" type="array">\n')
      output += '    <languageKey index="'+lang+'" type="array">\n'
      for lesson_nr in LL_dict[lang].iterkeys():
        sniplist = LL_dict[lang][lesson_nr]
        for item_nr in range(len(sniplist)):
          snippet = sanitize_snippet(sniplist[item_nr], False)
          snippet = htmlize(snippet)
          label = 'label_lesson_'+str(lesson_nr)+'_item'+str(item_nr+1)
          #output_file.write('  <label index="'+label+'">'+snippet+'</label>\n')
          output += '      <label index="'+label+'">'+snippet+'</label>\n'
      #output_file.write('</languageKey>\n')
      output += '    </languageKey>\n'
    text = read_html(HTMLRES_Path +"/XML-foot.txt")
    output += text

    output_file = codecs.open(xmlfile, 'w', "utf-8")
    output_file.write(output)
    output_file.close()

  def write_sec_txt(self, content, section):
    section = section.replace('/', '')
    output_file = codecs.open(self.PATH+"lek"+str(self.lesson_nr)+"_"+section+".txt", 'w', "utf-8")
    output_file.write(content)
    output_file.close()

  def write_html(self, filename):
    outfile = codecs.open(filename, 'w', "utf-8")
    outfile.write(self.output)
    outfile.close()
################### //WRITER #######################

#################### GLOBAL FUNCTIONS ##############

def message(text):
  print text

def create_directories(leclist):
  for lesson_nr in leclist:
    lekpath = "../lections/lek"+str(lesson_nr)+'/'
    os.system("mkdir " +lekpath)

def convert_to_html(lesson_list):
  ###Uses open office to convert all given doc-files to HTML
  message('converting raw docs to HTML')
  os.system('soffice -accept="socket,port=8100;urp;"')
  for lang in ["en", "sp"]:
    path = "../rawdocs/"+lang
    for lesson_nr in lesson_list:
      lekpath = "../lections/lek"+str(lesson_nr)+'/'
      for infile in glob.glob(os.path.join(path, "*lek-"+str(lesson_nr)+"-*.doc")):        
        message('converting '+ infile)
        os.system('python DocumentConverter.py ' +infile +' ' +lekpath+'lek'+str(lesson_nr)+'_'+lang+'.html') 

def isodd(number):
  if number%2 ==0:
    return False
  else:
    return True

def read_html(html_file):
  #Reads the content of the given file and returns it as a string.
  #Was at first only used for html-files.
  input_file = codecs.open(html_file, 'r', "utf-8")
  text = ""
  for line in input_file.readlines():
    text = text + line
  input_file.close()
  return text

def sanitize_snippet(snippet, onlytabs):
  #Clears a line of HTML of some annoying symbols.
  if not onlytabs:
    snippet = snippet.replace('\n',' ')
    snippet = snippet.replace('#','')
    snippet = snippet.strip()
  snippet = snippet.replace('\t','')
  return snippet

def htmlize(content):
  #translates the content from utf-8 to html
  return cgi.escape(content).encode('ascii', 'xmlcharrefreplace')

def run(leclist):
  languages = ["en", "sp"]
  #create_directories(leclist)
  convert_to_html(leclist)
  
  LL_dict = {}
  for lang in languages:
    LL_dict[lang] = {}
  for lesson_nr in leclist:
    PATH = "../lections/lek"+str(lesson_nr)+"/"
    OUTFILE = PATH+"lek"+str(lesson_nr)+"_LL.html"
    path = "../lections/lek" + str(lesson_nr)
    for infile in glob.glob(os.path.join(path, "*lek"+str(lesson_nr)+"*.html")):
      lang = infile[-7:-5]
      if lang != "LL":
        message("processing "+infile)

        parser = MyHTMLParser()
        dehasher = Dehasher(lesson_nr)
        writer = Writer(dehasher, PATH)

        dehasher.inlist = []
        lekpath = "../lections/lek"+str(lesson_nr)+'/'
        parser.feed(read_html(infile))
        snipdic = parser.snipdic

        if lang == 'en':
          writer.create_html(snipdic, OutsourceTXT = True)
          writer.write_html(lekpath+"lek"+str(lesson_nr)+"_LL.html")
        else:
          writer.create_html(snipdic)

        LL_dict[lang][dehasher.lesson_nr]=dehasher.inlist

  len_dict = {}
  for lesson_nr in leclist:
    len_dict[lesson_nr] = {}
    for lang in languages:
      len_dict[lesson_nr][lang] = len(LL_dict[lang][lesson_nr])
    len_dict[lesson_nr].values().sort()
    len_sort = len_dict[lesson_nr].values()
    if len_sort[0] != len_sort[-1]:
      message("Different number of foreign language snippets in lection" + str(lesson_nr))
      message(len_dict[lesson_nr])
      
  writer.write_xml("locallang.xml", LL_dict)

if __name__ == '__main__':
  run(range(1,31))
  #run([1,2])