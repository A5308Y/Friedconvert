# -*- coding: utf-8 -*-

class Tabificator:
	def __init__(self):
		self.table = u""

	def parse(self, string):
		rowlist = string.split(u"\n")
		for row in rowlist:
			columnlist = row.split(u"\t")
			self.table = self. table + u"<tr>"
			for column in columnlist:
				self.table = self. table + u"<td>" + column + u"</td>"
			self.table = self. table + u"</tr>"
		return self.table