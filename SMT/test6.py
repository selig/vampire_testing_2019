import os

def write_file(res):
	with open("SMT.csv",'w') as file:
		for line in res:
			file.write(line)

class Func(object):
	def __init__(self):
		#all of the result will be stored here
		self.result = []
	
	def __call__(self, path):
		#for debugging
		print(path)

		flag = False
		#process one file
		with open(path, 'r', encoding='iso-8859-1') as file:
			for line in file:
				if("set-info :status" in line):
					line = line.split()
					flag = True
					break;
		#if the file contains string "Status", then add it into results
		if flag:
			self.result.append(path.split('/')[-1] + ',' + line[-1] + '\n')

def walk_through(path, func):
	#all entries
	entries = os.listdir(path)
	#folder
	directories = []
	#file
	res = []
	for entry in entries:
		#if this entry is a folder then add it into folder list
		if(os.path.isdir(path + '/' + entry)):
			directories.append(path + '/' + entry)
		else:
			#else process it
			func(path + '/' + entry)
	#for every folders in the current path do the samething as above
	for directory in directories:
		walk_through(directory, func)

def main():
	func = Func()
	walk_through("SMT-lib", func)
	write_file(func.result)

if __name__ == '__main__':
	main()
