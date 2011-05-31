#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import codecs

lesson_nr = 15

PATH = "../lek"+str(lesson_nr)+"/"

OUTFILE = PATH+"lek"+str(lesson_nr)+"_LL.html"
SRCFILE = PATH+"lek"+str(lesson_nr)+".html"
XMLFILE = PATH+"lek"+str(lesson_nr)+".xml"

HTMLRES_Path = "HTMLRES"

colordic = {"Title":"#000066", "Text": "#0099cc"}
colordic["Vocs"] = "#99ffcc"
colordic["Grammar"] ="#ff6699"

def read_html(html_file):
  input_file = codecs.open(html_file, 'r', "utf-8")
  text = ""
  for line in input_file.readlines():
    text = text + line
  input_file.close()
  return text

def sanitize_snippet(snippet, onlytabs):
  if not onlytabs:
    snippet = snippet.replace('\n',' ')
    snippet = snippet.replace('#','')
    snippet = snippet.strip()
  snippet = snippet.replace('\t','')
  return snippet

def capture_caption(html_tag, snippet, captionlist):
  for i in xrange(10):
    snippet = sanitize_snippet(snippet, False)
    if html_tag.count("H"+str(i)) == 1 and snippet!='':
      captionlist.append(snippet)
    elif html_tag.count("H"+str(i)) > 1:
      pass
      #print "SOMETHINGS WRONG!!!! with the Caption tags. Search for \"H"+str(i)+"\" "
       ##Da müssen noch die Style Vorgaben für Hx ausgeblendet werden...

def snippetize(text):
  # Seperating the html_tags and the actual text. Then recreate the whole text without formatting
  # and store the captions and tags.
  snippettext = ''
  captionlist = []
  htmltaglist = []
  snippetlist = []
  for i in xrange(text.count("<")+1):
    htmltag = text.split("<")[i].split(">")[0]
    htmltaglist.append(htmltag)
    
    snippet = text.split(">")[i].split("<")[0]
    snippetlist.append(snippet)
    capture_caption(htmltag, snippet, captionlist)
    snippettext = snippettext + snippet
    
  if snippettext.count("#")%(2) != 0:
    print "Odd number of '#'-Symbols. That's not good!"
    
  returndict = {"sniptext": snippettext, "sniplist": snippetlist,}
  returndict["captionlist"] = captionlist
  returndict["taglist"] = htmltaglist

  return returndict
     
    
def dehash(sniptext):
  ###Search for the text in between the "#"'s (every odd snippet), clear the formatting
  ###and store all snippets in a list.
  insnips = []
  outsnips = []
  for i in xrange((sniptext.count("#"))/2):
    insnippet = sniptext.split("#")[2*i+1]
    insnippet = sanitize_snippet(insnippet, False)
    
    outsnippet = sniptext.split("#")[2*i]
    outsnippet = sanitize_snippet(outsnippet, True)
    
    if insnippet != '':
      insnips.append(insnippet)
    if outsnippet !='':
      outsnips.append(outsnippet)
      
  return {"outsnips": outsnips, "insnips":insnips}

### THIS WAS A TRY TO CONSERVE THE LIBREOFFICE GENERATED HTML CODE. NOW THE HTML IS COMPLETELY
### CREATED ANEW

##Nur noch Zeilenumbrüche scheinen das Problem zu sein!

#### -> Problem: Die "#"'en sind in vielen Fällen vom Text durch Tags getrennt.
#### -> Lösungsidee: Snippets und Text einzeln wieder zusammensetzen, wie ich's oben auch auseinandergenommen hab.

#def replacehash(snippetlist, taglist):
#for i in xrange(len(snippetlist)):
#a = 1
#snippetchain_forward = snippetlist[i]
#snippetchain_backward = snippetlist[i]
#while ((snippetchain_forward).count("#") not in [0,2]) and a <= 3:
##print snippetchain_forward, str(snippetchain_forward.count("#"))
#snippetchain_forward = snippetchain_forward + snippetlist[i+a]
#a += 1
###########################

def rebuild(dehashed_dict):
  ins = dehashed_dict["insnips"]
  outs = dehashed_dict["outsnips"]
  new_text = ''
  for i in range(min(len(outs), len(ins))):
    new_text = new_text + outs[i]
    new_text = new_text + "###_LL_LABEL_LESSON"+str(lesson_nr)+"_ITEM"+str(i)+"###"
  return new_text

def write_html(content):
  
  #CONTENTFILE = PATH+"lek15_LLroh.html"
  #OUTFILE = PATH+"lek15_LL.html"
  
  outfile = codecs.open(OUTFILE, 'w', "utf-8")
  
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

  #Read the lines of the different templates
  for vorlage in ["Head.txt", "Body.txt", "Foot.txt"]:
    vorfile = codecs.open(HTMLRES_Path + "/"+vorlage, 'r', "utf-8")
    lines = vorfile.readlines()
    vorfile.close()
    #And write them in the new file, replacing ###TEXT### with the content
    for line in lines:
      line = line.replace("###TEXT###", content)
      line = line.replace("###COLOR###", colordic["Grammar"])

      outfile.write(line)
  outfile.close()


def write_xml(sniplist):
  ##This is how an entry in the XML should look like:
  ##'<label index="label_lesson14_item1">phrases before the statement</label>'
  output_file = codecs.open(XMLFILE, 'w', "utf-8")
  for item_nr in range(1, len(sniplist)):
    output_file.write('<label index="label_lesson_'+str(lesson_nr)+'_item'+str(item_nr)+'">'+sniplist[item_nr]+'</label>\n')
  output_file.close()



snipdic = snippetize(read_html(SRCFILE))
dehashed_dict = dehash(snipdic["sniptext"])
write_html(rebuild(dehashed_dict))
write_xml(snipdic["sniplist"])