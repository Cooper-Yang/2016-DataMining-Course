# -*- coding: utf-8 -*-
"""
Main function
"""
import os
import sys

from io_table import trans_to_table
from k_means import KMeans

def main_func(input_argv=None):
	"""
	主函数
	"""
	#若定义了输入文件名
	if len(input_argv) > 1:
		#获取绝对路径
		input_test_path = os.path.abspath(input_argv[1])
	else:
		input_test_path = os.path.abspath('./data.arff')
	#若定义了输出文件名
	if len(input_argv) > 2:
		output_path = os.path.abspath(input_argv[2])
	else:
		output_path = os.path.abspath('./output.txt')
	#打开文件
	try:
		input_test = open(input_test_path, 'r')
		output_file = open(output_path, 'w')
	except IOError:
		sys.exit(1)

	#读取文件，将其输入到表中
	test_table = KMeans()
	test_table.data_table = trans_to_table(input_test.readlines())
	test_table.k_means()
	output_lines = test_table.format_out()
	output_file.writelines(output_lines)

	#关闭文件
	output_file.close()
	input_test.close()

	#print sys.argv
	print '\n finished \n'
	return

if __name__ == "__main__":
#调用主函数
	main_func(sys.argv)
