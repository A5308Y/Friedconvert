#!/usr/bin/env python2
# -*- coding: utf-8 -*-

SRCFILE = "E-lek-14-infinitiv.html"
XMLFILE = "test.xml"
lesson_nr = 14

def read_html(html_file):
  input_file = open(html_file, 'r')
  text = ""
  for line in input_file.readlines():
    text = text + line
  input_file.close()
  return text

def sanitize_snippet(snippet):
  snippet = snippet.replace('\n',' ')
  snippet = snippet.replace('\t','')
  snippet = snippet.replace('#','')
  snippet = snippet.strip()
  return snippet

def capture_caption(html_tag, snippet, captionlist):
  for i in xrange(10):
    snippet = sanitize_snippet(snippet)
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

def replacehash(snippetlist, taglist):
  for i in xrange(len(snippetlist)):
    a = 1
    snippetchain_forward = snippetlist[i]
    snippetchain_backward = snippetlist[i]
    while ((snippetchain_forward).count("#") not in [0,2]) and a <= 3: 
      #print snippetchain_forward, str(snippetchain_forward.count("#"))
      snippetchain_forward = snippetchain_forward + snippetlist[i+a]
      a += 1
    if a != 1:
      if a == 3:
        print snippetchain_forward
      else:
        print "Problem solved"
     
    
def dehash(sniptext):
  ###Search for the text in between the "#"'s (every odd snippet), clear the formatting
  ###and store all snippets in a list.
  snippetlist = []
  for i in xrange((sniptext.count("#"))/2):
    snippet = sniptext.split("#")[2*i+1]
    snippet = sanitize_snippet(snippet)
    if snippet != '':
      snippetlist.append(snippet)
  return snippetlist


snipdic = snippetize(read_html(SRCFILE))
#dehash(snippetlist)
replacehash(snipdic["sniplist"], snipdic["taglist"])


#labellist = []
#for i in xrange(len(snippetlist)+1):
  #labellist.append("###_LL_LABEL_LESSON14_ITEM"+str(i)+"###")

#def 
#i=1
#new_text = snippet_text
#for snippet in snippetlist:
  #print "Replacing \""+  snippet  + "\" with "+ "###_LL_LABEL_LESSON14_ITEM"+str(i)+"###" +" at "+ str(text.find(snippet))
  #new_text = new_text.replace("#"+snippet+"#", "###_LL_LABEL_LESSON14_ITEM"+str(i)+"###", 1)
  #i += 1

##Nur noch Zeilenumbrüche scheinen das Problem zu sein!

#### -> Problem: Die "#"'en sind in vielen Fällen vom Text durch Tags getrennt.
#### -> Lösungsidee: Snippets und Text einzeln wieder zusammensetzen, wie ich's oben auch auseinandergenommen hab.

#html_file = open("lek14.html", 'w')
#html_file.write(new_text)
#html_file.close()

#output_file = open(XMLFILE, 'w')
#for item_nr in range(len(snippetlist)):
  #output_file.write('<label index="label_lesson_'+str(lesson_nr)+'_item'+str(item_nr)+'">'+snippetlist[item_nr]+'</label>\n')
#output_file.close()

##This is how an entry in the XML should look like:
##'<label index="label_lesson14_item1">phrases before the statement</label>'