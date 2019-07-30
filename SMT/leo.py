import os
import random


def write_file(file_name, res):
    with open(file_name, 'w') as file:
        for line in res:
            file.write(line)


def write_dic(file_name, res):
    with open(file_name, 'w') as file:
        for key in res:
            file.write(key + '\n')
            for k in res[key]:
                file.write('\t' + k + '\n')
                for e in res[key][k]:
                    file.write("\t" * 2 + e + '\n');
            file.write('\n')


def sample_number(size):
    res = 0
    if size >= 50:
        res = 10
    elif 10 <= size < 50:
        res = 5
    elif 4 <= size < 10:
        res = 3
    else:
        res = size
    return res


def random_selection(res):
    index = []
    result = []
    #相对
    path = os.getcwd().split('\\')[-1] + '/'
    #绝对
    # path = os.getcwd().replace('\\', '/')
    for key in res:
        for k in res[key]:
            # if(len(res[key][k]) < number):
            # for e in res[key][k]:
            # 	result.append(path + e + '\n')
            # result.append('\n\n')
            # continue
            number = sample_number(len(res[key][k]))

            while len(index) < number:
                # print(index)
                idx = random.randrange(0, len(res[key][k]))
                if idx not in index:
                    index.append(idx)
                else:
                    continue

            print(index)
            for idx in index:
                result.append(path + res[key][k][idx] + '\n')
            index.clear()
            result.append('\n')
    return result


class Func(object):
    def __init__(self, funcs):
        self.funcs = funcs
        self.result = []
       # n is the number of attribute
    def __call__(self, path):
        if(".git" in path):
            return
        # res =  "\"" + path.split('/')[-1] + "\""
        res = ["" for i in range(len(self.funcs) + 1)]  # .split('/')[-1]
        res[0] = path
        # should break
        flag = (1 << len(self.funcs)) - 1
        with open(path, 'r', encoding='iso-8859-1') as file:
            for line in file:
                for i in range(len(self.funcs)):
                    r = self.funcs[i](line)
                    if (len(r) != 0):
                        res[i + 1] = r
                        flag ^= (1 << i)
                if (flag == 0):
                    break
        self.result.append(res)


class Combine(object):
    def __init__(self):
        self.result = {}

    # self.cnt = 0

    def __call__(self, line):
        # self.cnt += 1
        print(line)
        if (len(line) < 2):
            print(line)
            return
        # the first element is file name
        file_name = line[0]
        # the second is status
        status = line[1]

        logic = ""
        if (len(line) > 2):
            logic = line[2]
        else:
            logic = "Empty"

        if (status not in self.result.keys()):
            self.result[status] = dict()
        if (logic not in self.result[status].keys()):
            self.result[status][logic] = []
        self.result[status][logic].append(file_name)


class Status(object):
    def __call__(self, line):
        res = ""
        if ("Status" in line):
            # res += "\"" + line.split()[-1] + "\""
            res += line.split()[-1]
        return res


class Status_sim(object):
    def __call__(self, line):
        # print(line)
        # print (line)
        res = ""
        if ("set-info :status" in line):
            res += line.split()[-1][0:-1]
        # print("status: " + res)
        return res


class Spc(object):
    def __call__(self, line):
        res = ""
        if ("SPC" in line):
            line = line.split()[-1].split('_')
            res = line[0]
            # for i in range(0, len(line)):
            #     #	res += ",\"" + line[i] + "\""
            #     res += line[i]
        return res


class Logic(object):
    def __call__(self, line):
        res = ""
        if ("set-logic" in line):
            res += line.split()[-1][0:-1]
        # print("loigc: " + res)
        return res


def walk_through(path, func):
    entries = os.listdir(path)
    directories = []
    res = []
    for entry in entries:
        if (os.path.isdir(path + '/' + entry)):
            directories.append(path + '/' + entry)
        else:
            func(path + '/' + entry)
    for directory in directories:
        walk_through(directory, func)


def main():
    func = Func([Status_sim(), Logic()])
    walk_through("SMT-lib", func)

    combine = Combine();
    for res in func.result:
        combine(res)

    write_dic("res.txt", combine.result)
    write_file("result.txt", random_selection(combine.result))


if __name__ == '__main__':
    main()
