# -*- coding: utf-8 -*-
"""
Apriori算法：
"""

import os
import sys

class DataTable(object):
	"""
	设置存储数据用的表
	table:
										Attribute
			instance 1
			instance 2		set(element)
			...
	add_element(self, string element) : 将element加入当前表项
	add_instance(self, set ins) : 将当前表项加入表的末尾，并清空当前表项
	"""
	def __init__(self):
		self.d_instance = []
		self.d_attribute = set()
	def add_element(self, element=None):
		"""
		void add_element(self, string element)
		将element加入当前表项
		"""
		self.d_attribute.add(element)
	def add_instance(self, instance=None):
		"""
		void add_instance(self, set instance)
		将当前表项加入表的末尾，并清空当前表项
		"""
		self.d_instance.append(instance)
		self.d_attribute = set()

class FreqTable(object):
	"""
	设置存储频繁项集用的表
	table:
																			Attribute 1												Attribute 2					...
			instance 1
			instance 2		set(element),float(support),set(from_which_d_ins)				...							...
			...
	"""
	def __init__(self):
		self.f_instance = [[], []]
		self.f_attribute = []
		self.f_attr_elem = [set(), float(), set()]
	def append_element(self, num=None, element=None):
		"""
		append_element(self, int num, set element)
		将element加入频繁num项集
		"""
		#若元素的个数和频繁num项集的num不相等则返回失败
		freq_attribute = list()
		attr_elem = [set(), float(), set()]
		if len(element) != num:
			return False
		#element在频繁num项集中已存在的情况
		#尝试在频繁num项集中索引element，若已存在，则返回True
		if self.get_set_index(num, element) is not None:
			return True
		else:
			#element在频繁num项集中不存在的情况，此时index = None
			#设置一个元素[0]为set(element)的attr_elem项
			attr_elem[0] = element
			#检查频繁num项集是否存在，若存在则将上步新建的attr_elem项加入末尾
			try:
				freq_attribute = self.f_instance[num]
				freq_attribute.append(attr_elem)
				self.f_instance[num] = freq_attribute
			#若不存在则新建频繁num项集，再将上步新建的attr_elem项加入末尾
			except IndexError:
				freq_attribute = list()
				freq_attribute.append(attr_elem)
				self.f_instance.append(freq_attribute)
			self.clean()
			return True
	def get_set_list(self, num=None):
		"""
		get_set_list(self, int num)
		输出频繁num项集中的所有set，这些set会放在一个list中返回
		"""
		set_list = []
		for attr in self.f_instance[num]:
			set_list.append(attr[0])
		return set_list
	def get_set_index(self, num=None, element=None):
		"""
		get_set_index(self, int num, set element)
		获取输入的element在频繁num项集的list中的index
		"""
		if len(element) != num:
			return None
		try:
			for i in range(0, len(self.f_instance[num])):
				try:
					if element == self.f_instance[num][i][0]:
						return i
				except IndexError:
					pass
		except IndexError:
			pass
		return None
	def remove_non_support(self, num=None, min_sup=None):
		"""
		remove_non_support(self, int num, float min_sup)
		进行剪枝
		将不满足支持度计数min_sup的set从频繁num项集中移除
		"""
		remove_list = []
		for i in range(0, len(self.f_instance[num])):
			if self.f_instance[num][i][1] < min_sup:
				remove_list.append(self.f_instance[num][i])
		for item in remove_list:
			self.f_instance[num].remove(item)
		return True

	def connect_element(self, num=None):
		"""
		connect_element(self, int num)
		进行连接
		将频繁num-1项集中的所有项进行连接，生成频繁num项集
		连接的前提，如果频繁num-1项集中的两个set的并集中的元素个数大于等于num-2个，则进行连接
		"""
		for i in range(0, len(self.f_instance[num-1])):
			for j in range(i+1, len(self.f_instance[num-1])):
				set_a = set(self.f_instance[num-1][i][0])
				set_b = set(self.f_instance[num-1][j][0])
				common = set_a & set_b
				cap = set_a | set_b
				if len(common) >= num-2 and len(cap) == num:
					self.append_element(num, cap)
		return True
	def support_scan(self, num=None, input_table=None):
		"""
		扫描数据库
		获取频繁num项集中所有项的支持度，以及每项在数据表中所在的条数
		support_scan(self, int num, set_list input_table)
		其中set_list的结构为：
			Instance 1	set(element_1, element_2, ... , element_n)
			Instance 2
			...
			Instance n
		"""
		set_list = self.get_set_list(num)
		#这里需要遍历所有数据，有没有其他更好的方法？？
		for attr_elem in set_list:
			support = float()
			for i in range(0, len(input_table)):
				if len(input_table[i] & attr_elem) == len(attr_elem):
					support += 1.0
					set(self.f_instance[num][set_list.index(attr_elem)][2]).add(i)
			self.f_instance[num][set_list.index(attr_elem)][1] = support
		return True
	#输出
	def format_out(self):
		"""
		将频繁项集表中的数据进行格式化输出
		"""
		output_lines = []
		for ins in self.f_instance:
			line = ''
			for elem in ins:
				line = line + str(list(elem[0])).rjust(36) + str(elem[1]).rjust(5) + str(list(elem[2])).rjust(32) + '\n'
			output_lines.append(line)
		return output_lines
	def clean(self):
		"""
		清理频繁项集表
		"""
		self.f_attribute = []
		self.f_attr_elem = [set(), float()]
		self.f_attr_elem = [set(), float()]
		return True

def get_confidence(input_conf=None, num=None, input_freq=None, min_conf=None):
	"""
	get_confidence(FreqTable input_conf, int num, FreqTable input_freq, float min_conf = None)
	"""
	pass

def get_freq(input_freq=None, num=None, input_table=None, min_sup=None):
	"""
	get_freq(FreqTable input_freq, int num, DataTable input_table, float min_sup)
	获取频繁项集，freq为输入的频繁项集，num指获取频繁num项集，input_table为输入的数据
	"""
	#如果是频繁1项集
	if num == 1 and input_table is not None:
		for ins in input_table.d_instance:
			for elem in ins:
				#将元素加入频繁 1 项集
				temp = set()
				temp.add(elem)
				input_freq.append_element(num, temp)
		#扫描支持度
		input_freq.support_scan(num, input_table.d_instance)
		#剪枝步
		input_freq.remove_non_support(num, min_sup)
	#如果是频繁 2 项集以上
	elif num > 1 and input_freq is not None:
		#连接步，获取频繁num项集
		input_freq.connect_element(num)
		#扫描支持度计数
		input_freq.support_scan(num, input_table.d_instance)
		#剪枝步
		input_freq.remove_non_support(num, min_sup)
	else:
		return input_freq
	#返回结果
	return input_freq

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
		if line[0] == '\n':
			continue
		temp = str(line).split(',')
		#对于分隔出来的每个单词，去除其中的换行符和空格，将其加入一个表项中
		for word in temp:
			tmp_word = word.split().pop()
			table.add_element(tmp_word)
		#一行结束，将表项加入到表的末尾
		table.add_instance(table.d_attribute)
	return table

def main_func(input_argv=None):
	"""
	主函数
	"""
	#若定义了输入文件名
	if len(input_argv) > 1:
		#获取绝对路径
		input_path = os.path.abspath(input_argv[1])
	else:
		input_path = os.path.abspath('./test.txt')
	#若定义了输出文件名
	if len(input_argv) > 2:
		output_path = os.path.abspath(input_argv[2])
	else:
		output_path = os.path.abspath('./result.txt')
	#打开文件
	input_file = open(input_path, 'r')
	output_file = open(output_path, 'w')

	#进行处理，并将处理结果写入文件
	input_lines = input_file.readlines()
	input_table = trans_to_table(input_lines)
	input_freq = FreqTable()
	input_freq = get_freq(input_freq, 1, input_table, 2.0)
	num = 1

	while len(input_freq.f_instance[num]) != 0:
		get_freq(input_freq, num+1, input_table, 2.0)
		num += 1

	output_file.writelines(input_freq.format_out())

	#关闭文件
	input_file.close()
	output_file.close()

	#print sys.argv
	print '\n finished \n'
	return

if __name__ == "__main__":
#调用主函数
	main_func(sys.argv)
