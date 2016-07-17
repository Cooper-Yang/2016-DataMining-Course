# -*- coding: utf-8 -*-
"""
K-means算法主体
"""
import random
import copy
from io_table import DataTable

class KMeans(object):
	"""
	在此对象内进行KNN算法
	"""
	def __init__(self):
		#存储点数据
		self.data_table = DataTable()
		#存储中心点数据
		self.center_table = DataTable()
		#存储中心点的临近点在data_table中的下标
		self.node_table = []

	def k_means(self):
		"""
		K-MEANS算法主体部分
		"""
		#若输入的中心点数据为空，生成随机中心点
		if self.center_table.row == 0:
			self.generate_init_point(4)
		#将点分配给中心点
		self.assignment_point_to_centers()
		#深拷贝中心点数据
		temp = copy.deepcopy(self.center_table)
		#依照被分配到的所有点的平均值重新计算中心点位置
		self.renew_k_point()
		#不断重复以上步骤，直到重新计算的中心点位置不再变化
		while self.center_table.d_instance != temp.d_instance:
			self.assignment_point_to_centers()
			temp = copy.deepcopy(self.center_table)
			self.renew_k_point()
		return True

	def assignment_point_to_centers(self):
		"""
		assignment_point_to_centers(self, DataTable input_point)
		将data_table中的点按照距离分配给最邻近的中心点
		"""
		#临时存储距离计算结果
		distance = float()
		#存储某一点到最近的候选中心点的距离
		distance_min = float()
		#存储distance_min对应的点
		node_num = 0
		#存储distance_min对应的中心点
		center_num = 0
		#初始化node_table
		self.node_table = []
		for i in range(0, self.center_table.row):
			self.node_table.append(set())
		#遍历所有点（即data_table中的所有行）
		for i in range(0, self.data_table.row):
			#对于每个center_table中的中心点
			for j in range(0, self.center_table.row):
				#计算距离
				distance = float()
				for k in range(0, self.center_table.column):
					distance += (float(self.data_table.d_instance[i][k]) - float(self.center_table.d_instance[j][k])) ** 2
				#若是第一个候选中心点，直接赋值；否则检查该距离是否比已知最短距离还短
				if j == 0:
					distance_min = distance
					node_num = i
					center_num = 0
				elif distance < distance_min:
					distance_min = distance
					node_num = i
					center_num = j
			#将点记录进node_table
			self.node_table[center_num].add(node_num)
		return True

	def renew_k_point(self):
		"""
		根据平均值更新中心点
		函数根据node_table中中心点数据，自动查找对应的data_table中的项并计算其平均值
		"""
		for i in range(0, len(self.node_table)):
			for j in range(0, self.center_table.column):
				distance_sum = float()
				for k in range(0, len(self.node_table[i])):
					#index = list(self.node_table[i])[k]
					distance_sum += float(self.data_table.d_instance[list(self.node_table[i])[k]][j])
				if distance_sum != 0:
					average = distance_sum / len(self.node_table[i])
				else:
					average = float()
				self.center_table.d_instance[i][j] = round(average, 10)
		return True

	def generate_init_point(self, num_of_point=None):
		"""
		生成k个初始点，其值根据此列数据的最大值和最小值来随机取
		"""
		#根据max和min来生成随机初始点
		for j in range(0, num_of_point):
			for k in range(0, self.data_table.column):
				#生成随机数
				rand_num = random.randint(int(self.data_table.minimun[k]), int(self.data_table.maximum[k])) + round(random.random(), 10)
				while rand_num > self.data_table.maximum[k] or rand_num < self.data_table.minimun[k]:
					rand_num = random.randint(int(self.data_table.minimun[k]), int(self.data_table.maximum[k])) + round(random.random(), 10)
				#将随机数作为attribute加入center_table
				self.center_table.add_element(rand_num)
			self.center_table.append_instance(self.center_table.d_attribute)
			#annoing unused Warning
			j = j
		return True

	def format_out(self):
		"""
		输出K-Means的中心点计算结果
		"""
		output_lines = list()
		output_lines.extend(self.center_table.format_out())
		# 注意，由于center_table没有info字段，所以才这样做，否则info字段会破坏
		for i in range(0, self.center_table.row):
			temp = '  ' + str(list(self.node_table[i])) + '\n'
			output_lines[i] = output_lines[i].replace('\n', temp)
		return output_lines
