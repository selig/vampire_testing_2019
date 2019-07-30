import os

def write_file(res):
	with open("res.csv",'w') as file:
		for line in res:
			file.write(line)

class Func(object):
	def __init__(self, funcs):
		self.funcs = funcs
		self.result = []

	def __call__(self, path):
		res = "\"" + path.split('/')[-1] + "\""
		#should break
		flag = False
		with open(path, 'r', encoding='iso-8859-1') as file:
			for line in file:
				for i in range(len(self.funcs)):
					r = self.funcs[i](line)
					if(r != ','):
						res += r
						if(i == len(self.funcs) - 1):
							flag = True
				if(flag):
					break
		res += '\n'
		print(res)
		self.result.append(res)

class Logic(object):
	def __call__(self, line):
		flag = False
		res = ","
		if("set-logic" in line):
			res += "\"" + ((line.split()[-1]).split(')')[0]) + "\""
		return res

class Category(object):
	def __call__(self, line):
		flag = False
		res = ","
		if("set-info :category" in line):
			res += "\"" + ((line.split()[-1]).split(')')[0]) + "\""
		return res
    
class Status(object):
	def __call__(self, line):
		flag = False
		res = ","
		if("set-info :status" in line):
			res += "\"" + ((line.split()[-1]).split(')')[0]) + "\""
		return res

# class Spc(object):
# 	def __call__(self, line):
# 		flag = False
# 		res = ","
# 		if("SPC" in line):
# 			res = ""
# 			line = line.split()[-1].split('_')
# 			for i in range(0, len(line)):
# 				res += ",\"" + line[i] + "\""
#
# 		return res

def walk_through(path, func):
	entries = os.listdir(path)
	directories = []
	res = []
	for entry in entries:
		if(os.path.isdir(path + '/' + entry)):
			directories.append(path + '/' + entry)
		else:
			func(path + '/' + entry)
	for directory in directories:
		walk_through(directory, func)

def main():
	func = Func([Logic(),Category(),Status()])
	walk_through("SMT-lib", func)
	write_file(func.result)

if __name__ == '__main__':
	main()
