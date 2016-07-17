# -*- coding: utf-8 -*-
"""
KNN
"""
import os
import sys
import copy

class DataTable(object):
	"""
	设置存储数据用的表
	table:
										Attribute
			instance 1
			instance 2		list(element)
			...
	其中最后一列数据约定为class名
	add_D_Attr(self, string element) : 将element加入当前表项
	append_instance(self, set ins) : 将当前表项加入表的末尾，并清空当前表项
	"""
	def __init__(self):
		self.info = []
		self.d_instance = []
		self.d_attribute = []
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
		将当前表项加入表的末尾，并清空当前表项，并更新class名表
		"""
		self.d_instance.append(instance)
		self.class_list.add(instance[-1])
		self.d_attribute = []
		return True

	def append_to_line(self, line_num, element):
		"""
		在已存在的某行中加入元素到末尾
		"""
		self.d_instance[line_num].append(element)
		return True

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

	def get_class(self, input_data=None, input_k=None):
		"""
		get_class(self, list input_data, int input_k)
		对输入的input_data计算其和所有数据的距离，然后选取最近的input_k个
		返回最近的input_k个中类别最多的那个类
		"""
		distance_table = []
		element = [float(), str()]
		count_table = []
		for line in self.d_instance:
			#计算距离并获取类别，距离 = 当前距离 + 元素之差的平方
			for k in range(0, len(line)-1):
				element[0] += (float(line[k]) - float(input_data[k])) * (float(line[k]) - float(input_data[k]))
			element[1] = line[-1]
			#将数据加入距离表，距离越近，下标越小
			if len(distance_table) == 0:
				distance_table.append(element)
			else:
				#如果比第一项大，则运行插入算法，否则直接插到第0位
				if distance_table[0][0] <= element[0]:
					#从头到尾遍历表，i记录当前位置。如果小于等于第i-1项的距离且大于等于第i项的距离，则插入到当前位置i
					#如果发生异常说明当前位置i已经超出了表长，即距离比表中所有已知距离都长，不进行插入
					for i in range(1, len(distance_table)+1):
						try:
							if distance_table[i-1][0] <= element[0] <= distance_table[i][0]:
								distance_table.insert(i, element)
								break
						except IndexError:
							break
				else:
					distance_table.insert(0, element)
			#对距离表进行删减
			#如果表长大于input_k，则将表尾元素出表
			#这样可以减少之前遍历距离表进行查找的开销
			if len(distance_table) > input_k:
				distance_table.pop()
			#清空
			element = [float(), str()]

		#进行投票
		#选最近的k个项中最多的类
		for elem in distance_table:
			count_table.append(elem[1])
		#初始化最邻近类为第一个已知类
		closest = list(self.class_list)[0]
		try:
			#对于已知类表中的第二个元素到最后一个元素
			#如果在距离表中查询发现当前遍历到的类名的个数，比当前邻近类的类名在距离表中的个数多，则将邻近类置为当前遍历到的类名
			for i in range(1, len(self.class_list)):
				if count_table.count(list(self.class_list)[i]) > count_table.count(closest):
					closest = list(self.class_list)[i]
		#出错说明超出已知类名表的长度
		except IndexError:
			pass
		return closest

	def format_out(self):
		"""
		进行格式化输出
		"""
		line = str()
		lines = []
		for info in self.info:
			lines.append(info)
		for ins in self.d_instance:
			for i in range(0, len(ins)-1):
				line = line + ins[i].rjust(17) + ','
			line = line + ins[-1].rjust(17) + '\n'
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
		temp = str(line).split(',')
		#对于分隔出来的每个单词，去除其中的换行符和空格，将其加入一个表项中
		for word in temp:
			tmp_word = word.split().pop()
			table.add_element(tmp_word)
		#一行结束，将表项加入到表的末尾
		table.append_instance(table.d_attribute)
	return table

def main_func(input_argv=None):
	"""
	主函数
	"""
	#若定义了输入文件名
	if len(input_argv) > 1:
		#获取绝对路径
		input_test_path = os.path.abspath(input_argv[1])
	else:
		input_test_path = os.path.abspath('./iris.2D.test.arff')
	if len(input_argv) > 2:
		#获取绝对路径
		input_train_path = os.path.abspath(input_argv[1])
	else:
		input_train_path = os.path.abspath('./iris.2D.train.arff')
	#若定义了输出文件名
	if len(input_argv) > 3:
		output_path = os.path.abspath(input_argv[2])
	else:
		output_path = os.path.abspath('./output.txt')
	#打开文件
	try:
		input_test = open(input_test_path, 'r')
		input_train = open(input_train_path, 'r')
		output_file = open(output_path, 'w')
	except IOError:
		sys.exit(1)

	#读取文件，将其输入到表中
	test_table = trans_to_table(input_test.readlines())
	train_table = trans_to_table(input_train.readlines())
	#将测试集深拷贝到输出集中
	output_table = copy.deepcopy(test_table)
	#对测试集中的每一项用KNN算法检测其预测分类，并将其写到输出集中新建的一列
	for num in range(0, len(test_table.d_instance)):
		output_table.append_to_line(num, train_table.get_class(test_table.d_instance[num], 3))

	output_file.writelines(output_table.format_out())

	#关闭文件
	output_file.close()
	input_test.close()
	input_train.close()

	#print sys.argv
	print '\n finished \n'
	return

if __name__ == "__main__":
#调用主函数
	main_func(sys.argv)
