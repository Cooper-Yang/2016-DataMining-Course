# -*- coding: utf-8 -*-
"""
将CSV文件转换为对象存储起来
"""

class DataTable(object):
	"""
	设置存储数据用的表
	table:
										Attribute
			instance 1
			instance 2		list(element)
			...
	其中最后一列数据约定为class名
	bool add_element(self, string element) : 将element加入当前表项
	bool append_instance(self, instance=None) : 将当前表项加入表的末尾，并清空当前表项，并更新class名表和行、列计数，以及最大值最小值
	bool append_to_line(self, line_num, element) : 将element加入到第line_num条表项的数据中
	list get_same_class(self, string input_class) : 以list的形式返回同一class的所有数据
	list format_out : 进行格式化输出，其输出的list可被writelines直接使用
	"""
	def __init__(self):
		self.info = []
		self.d_attribute = []
		#store table
		self.d_instance = []
		#column count
		self.column = int()
		#row count
		self.row = int()
		self.maximum = list()
		self.minimun = list()
		#表中的所有元素的已知类的集合
		self.class_list = set()

	def add_element(self, element=None):
		"""
		add_element(self, string element)
		将element加入当前表项
		"""
		self.d_attribute.append(element)
		return True

	def append_instance(self, instance=None):
		"""
		append_instance(self, set instance)
		将当前表项加入表的末尾，并清空当前表项，并更新class名表和行、列计数，以及最大值最小值
		"""
		self.d_instance.append(instance)
		#self.class_list.add(instance[-1])
		#refresh column and row counter
		if len(self.d_attribute) > self.column:
			self.column = len(self.d_attribute)
		self.row = len(self.d_instance)
		#refresh max and min counter
		for i in range(0, len(self.d_attribute)):
			try:
				if self.maximum[i] != 'not digits' and self.maximum[i] < float(self.d_attribute[i]):
					self.maximum[i] = float(self.d_attribute[i])
			except IndexError:
				try:
					self.maximum.insert(i, float(self.d_attribute[i]))
				except ValueError:
					self.maximum.insert(i, 'not digits')
			except ValueError:
				self.maximum[i] = 'not digits'

			try:
				if self.minimun[i] != 'not digits' and self.minimun[i] > float(self.d_attribute[i]):
					self.minimun[i] = float(self.d_attribute[i])
			except IndexError:
				try:
					self.minimun.insert(i, float(self.d_attribute[i]))
				except ValueError:
					self.minimun.insert(i, 'not digits')
			except ValueError:
				self.minimun[i] = 'not digits'
		#reset d_attribute to None
		self.d_attribute = []
		return True

	def append_to_line(self, line_num, element):
		"""
		将element加入到第line_num条表项的数据中
		"""
		self.d_instance[line_num].append(element)
		if len(self.d_instance[line_num]) > self.column:
			self.column = len(self.d_instance[line_num])
		return True

	def get_column(self, column_num=None):
		"""
		将某一列的所有数据放在一个list中返回
		"""
		column_list = list()
		for line in self.d_instance:
			column_list.append(line[column_num])
		return column_list

	def get_same_class(self, input_class=None):
		"""
		get_same_class(self, string input_class)
		以list的形式返回同一class的所有
		"""
		temp_list = []
		for line in self.d_instance:
			if line[-1:] == input_class:
				temp_list.append(line[-1:])
		return temp_list

	def format_out(self):
		"""
		进行格式化输出
		"""
		line = str()
		lines = []
		if len(self.info) != 0:
			for info in self.info:
				lines.append(info)
		for ins in self.d_instance:
			for i in range(0, len(ins)-1):
				line = line + str(ins[i]).rjust(17) + ','
			line = line + str(ins[-1]).rjust(17) + '\n'
			lines.append(line)
			line = str()
		return lines

def trans_to_table(input_lines=None):
	"""
	trans_to_table(list input_lines)
	将使用readlines方法输入的数据存储进DataTable类型的对象中
	"""
	table = DataTable()
	#对于输入的每一行
	for line in input_lines:
		#若为注释行，则跳过
		if line[0] == '#':
			continue
		#若为arff格式中的类的信息，加入info中
		if line[0] == '@':
			table.info.append(line)
			continue
		if line[0] == '\n':
			continue
		temp = str(line).split()
		#对于分隔出来的每个单词，去除其中的换行符和空格，将其加入一个表项中
		for word in temp:
			tmp_word = word.split().pop()
			table.add_element(tmp_word)
		#一行结束，将表项加入到表的末尾
		table.append_instance(table.d_attribute)
	return table
