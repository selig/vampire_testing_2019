import os
import random

CONTENT_FILE_NAME = 0
CONTENT_STATUS = 1
CONTENT_LOGIC = 2
CONTENT_CATEGORY = 3

CONTENT_SPC = 2

strategy = "lrs+1011_1_cond=on:ile=on:nwc=1.2:stl=30:add=off:afr=on:afp=4000:afq=1.0:urr=ec_only:updr=off_63\n\
fmb+10_1_fmbsr=1.8:ile=on:nm=64:newcnf=on:av=off_65\n\
lrs+11_1_bd=off:nm=64:newcnf=on:nwc=1:stl=30:sac=on:add=off:afr=on:afp=100000:afq=1.1:amm=off:anc=none:sp=reverse_arity:urr=on:updr=off_4\n\
ott+11_2:1_bd=off:ile=on:irw=on:lma=on:nm=64:newcnf=on:nwc=1:av=off_6\n\
lrs+11_4:1_bsr=on:cond=on:fsr=off:ile=on:nm=64:nwc=1:stl=30:av=off:urr=on:updr=off_43\n\
ott+11_2:3_fsr=off:gs=on:irw=on:lma=on:nm=64:newcnf=on:nwc=1:av=off:urr=on_16\n\
dis+1011_128_ile=on:nwc=1:sos=on:av=off_38\n\
lrs+2_5:4_fsr=off:gs=on:gsem=off:ile=on:nm=2:newcnf=on:nwc=1:nicw=on:stl=30:aac=none:add=off:afr=on:afp=10000:afq=1.2:amm=sco:anc=none:sp=reverse_arity:urr=on_85\n\
ott+11_128_gsp=input_only:gs=on:gsem=on:ile=on:irw=on:lcm=predicate:nm=2:newcnf=on:nwc=1:aac=none:acc=on:add=large:afr=on:afp=40000:afq=1.4:amm=sco:anc=none:sp=reverse_arity:updr=off_40"

def write_file(file_name, res):
    with open(file_name, 'w') as file:
        for line in res:
            file.write(line)

def traverse_dic(res, selection_res):
    if(isinstance(res, dict)):
        for key in res:
            traverse_dic(res[key], selection_res)
    else:
        selection_res += random_selection(res)


def dic_write_helper(file_stream, res, layer):
    if(isinstance(res, dict)):
        for key in res:
            file_stream.write(layer * '\t' + key + '\n')
            dic_write_helper(file_stream, res[key], layer + 1)
    else:
        for e in res:
            file_stream.write(layer * '\t' + e + '\n')
        file_stream.write('\n')

def write_dic(file_name, res):
    with open(file_name, 'w') as file:
        dic_write_helper(file, res, 0)

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
    #path = os.getcwd().split('\\')[-1] + '/'
    #绝对
    path = os.getcwd().replace('\\', '/')
    number = sample_number(len(res))

    while len(index) < number:
        # print(index)
        idx = random.randrange(0, len(res))
        if idx not in index:
            index.append(idx)
        else:
            continue

    # print(index)
    for idx in index:
        strategy_list = strategy.split("\n")
        for strategy_item in strategy_list:
            result.append('./vampire_rel_master_4055' + ' ' + path + '/' + res[idx] + ' ' + '--include ../TPTP-v7.2.0/ --decode' + ' ' + strategy_item + ' ' + '--time_statistics on -p off -t 10s ' + '\n')
        result.append('\n')
    index.clear()
    result.append('\n')
    return result


class Func(object):
    def __init__(self, funcs):
        self.funcs = funcs
        self.result = []
       # n is the number of attribute
    def __call__(self, path):
        if(".git" in path or ".rm" in path):
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
                    #print(r)
                    if (len(r) != 0):
                        res[i + 1] = r
                        flag ^= (1 << i)
                if (flag == 0):
                    break
        self.result.append(res)


class CombineSIM(object):
    def __init__(self):
        self.result = {}

    def __call__(self, line):
        # print(line)

        file_name = line[CONTENT_FILE_NAME]
  
        question_name = file_name.split("/")[-2]
        status  = line[CONTENT_STATUS]
        logic = line[CONTENT_LOGIC]
        category = line[CONTENT_CATEGORY]
        #file_name += " " + self.strategy

        if(question_name not in self.result.keys()):
            self.result[question_name] = dict()
        if(status not in self.result[question_name].keys()):
            self.result[question_name][status] = dict()
        if(logic not in self.result[question_name][status].keys()):
            self.result[question_name][status][logic] = dict()
        if(category not in self.result[question_name][status][logic].keys()):
            self.result[question_name][status][logic][category] = list()

        self.result[question_name][status][logic][category].append(file_name)


class CombineTPTP(object):
    def __init__(self):
        self.result = {}
    # self.cnt = 0

    def __call__(self, line):
        # self.cnt += 1
        if (len(line) < 2):
            # print(line)
            return
        # the first element is file name
        file_name = line[CONTENT_FILE_NAME]

        #question name
        question_name = file_name.split('/')[-2]
        status = line[CONTENT_STATUS]
        spc = line[CONTENT_SPC]
        logic = "Empty"
        remaining = ""

        if("TF1" in spc or "TH0" in spc or 'THF' in spc or 'TFF' in spc or 'TFX' in spc or "TH1" in spc):
            return
        
        print(line)

        if(len(spc) > 0):
            logic = spc[0]
            if(len(spc) > 2):
                for i in range(2, len(spc)):
                    remaining += spc[i] + "_"
                remaining = remaining[0:-2]

        if(question_name not in self.result.keys()):
            self.result[question_name] = dict()
        if(status not in self.result[question_name].keys()):
            self.result[question_name][status] = dict()
        if(logic not in self.result[question_name][status].keys()):
            self.result[question_name][status][logic] = dict()
        if(remaining not in self.result[question_name][status][logic].keys()):
            self.result[question_name][status][logic][remaining] = list()

        self.result[question_name][status][logic][remaining].append(file_name)

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
        res = []
        if ("SPC" in line):
            res = line.split()[-1].split('_')
        return res


class Logic(object):
    def __call__(self, line):
        res = ""
        if ("set-logic" in line):
            res += line.split()[-1][0:-1]
        # print("loigc: " + res)
        return res

class Category(object):
    def __call__(self, line):
        res = ""
        if("set-info :category" in line):
            res += line.split()[-1][0:-1].replace("\"","")
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
    #sim
    # func = Func([Status_sim(), Logic(), Category()])
    # combine = CombineSIM()

    #TPTP
    func = Func([Status(), Spc()])
    combine = CombineTPTP();

    walk_through("../TPTP-v7.2.0/Problems", func)

    for res in func.result:
        combine(res)

    write_dic("res.txt", combine.result)
    final_res = []
    traverse_dic(combine.result, final_res)
    write_file("commands.txt", final_res)


if __name__ == '__main__':
   main()

