# -*- coding: utf-8 -*-

import unittest
from tabificator import *

class TabificatorTest(unittest.TestCase):
	def setUp(self):
		self.tabificator = Tabificator()
	
	def test_return_type_string(self):
		assert type(self.tabificator.parse(u'string')) is unicode
		
	def test_tablessstring_returns_td_enclosed(self):
		self.assertEqual(u'<tr><td>lkj</td></tr>', self.tabificator.parse('lkj'))
			
	def test_tab_enclosed_returns_td_enclosed(self):
		self.assertEqual(u'<tr><td>cell_1</td><td>cell_2</td><td>cell_3</td></tr>',
		 				 self.tabificator.parse(u'cell_1	cell_2	cell_3'))
	
	def test_linebreak_creates_tr(self):
		self.assertEqual(	u'<tr><td>row1</td></tr><tr><td>row2</td></tr>',
							self.tabificator.parse(u'row1\nrow2'))

	def test_linebreak_creates_tr(self):
		self.assertEqual(	u'<tr><td>row1col1</td><td>row1col2</td></tr>'+
							u'<tr><td>row2col1</td><td>row2col2</td></tr>',
							self.tabificator.parse(u'row1col1	row1col2\n' +
							u'row2col1	row2col2'))
						
						
		
if __name__ == '__main__':
	unittest.main()