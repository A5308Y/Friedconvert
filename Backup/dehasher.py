#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from helpers import *

##################### DEHASHER #######################

class Dehasher(object):
  def __init__(self, lesson_nr):
    self.inlist = []
    self.lesson_nr = lesson_nr
    self.label_nr = 1

  def dehash(self, string):
    outsnips = []
    insnips = []
    i = 0
    for snippet in string.split("#"):
      sanitize_snippet(snippet)
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
    ins = dehashed_dict["insnips"]
    self.inlist.extend(ins)
    outs = dehashed_dict["outsnips"]
    new_text = ''
    i=1
    for snip in outs:
      new_text = new_text + snip
      if len(ins) != 0 and i != len(outs):
        new_text = new_text + "###_LL_LABEL_LESSON_"+str(self.lesson_nr)+"_ITEM"+str(self.label_nr)+"###"
        i+=1
        self.label_nr +=1
    return new_text

#################### //DEHASHER ####################