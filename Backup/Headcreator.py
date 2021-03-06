### Headcreator

import codecs

#fileObj = codecs.open( "someFile", "r", "utf-8" )
#u = fileObj.read() # Returns a Unicode string from the UTF-8 bytes in the file

PATH = "../lek15/"


CONTENTFILE = PATH+"lek15_LLroh.html"
OUTFILE = PATH+"lek15_LL.html"

HTMLRES_Path = "HTMLRES"


outfile = codecs.open(OUTFILE, 'w', "utf-8")
# -*- coding: utf-8 -*-

contentfile = codecs.open(CONTENTFILE, 'r', "utf-8")
contentlines = contentfile.readlines()
content = ''
for line in contentlines:
  line = line.replace("\n", "<br>")
  line = line.replace(unichr(252), "&uuml;")
  line = line.replace(unichr(246), "&ouml;")
  line = line.replace(unichr(214), "&Ouml;")
  line = line.replace(unichr(220), "&Uuml;")
  line = line.replace(unichr(223), "&szlig;")
  line = line.replace(unichr(228), "&auml;")
  line = line.replace(unichr(196), "&Auml;")
  line = line.replace(unichr(8222), "\"")
  line = line.replace(unichr(8221), "\"")
  line = line.replace(unichr(8220), "\"")
  
  line = line.replace(unichr(8211), "-")
  line = line.replace(unichr(8212), "-")
  content += line


for vorlage in ["Head.txt", "Body.txt", "Foot.txt"]:
  vorfile = codecs.open(HTMLRES_Path + "/"+vorlage, 'r', "utf-8")
  lines = vorfile.readlines()
  vorfile.close()

  for line in lines:
    if "###TEXT###" in line:
      line = line.replace("###TEXT###", content)
    outfile.write(line)

outfile.close()