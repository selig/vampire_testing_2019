import csv
import re
import sys

def read(problem, strategy):
    with open("new_test.txt","r+") as file:
        lines = file.readlines()
        Totaltime = 0
        #Status = 0
        action = False
        rows = []
        for line in lines:
            row = []
            line = line.replace("\n", "")
            if "Time elapsed" in line:
                Totaltime = line.split(":")[1]
            else:
                return
            #try:
            #    if "status" in line:
            #        Status = line.split(" ")[3]
            #except IndexError as e:
            #    pass
            if action == True:
                temp = re.split("[%:]", line)
                try:
                    ClockName = re.split("[%:]", line)[1]
                    if "own" in temp[2]:
                        OverallTime = re.split("[()]", temp[2])[0]
                        OwnTime = re.split("[()]", temp[2])[1].split("own")[1]
                    else:
                        OverallTime = temp[2]
                        OwnTime = ""
                    row.extend([problem, strategy, ClockName, OverallTime, OwnTime])
                    rows.append(row)
                except IndexError as e:
                    pass
            if line == "% Time measurement results:\n":
                action = True
        rowb = [problem, strategy, Totaltime]
    file.close()
    return rows, rowb


if __name__ == '__main__':
    name = "./vampire_rel_master_4055 C:/Users/caspe/PycharmProjects/Leo_test/AGT/AGT031^2.p --include ../TPTP-v7.2.0/ --decode lrs+11_1_bd=off:nm=64:newcnf=on:nwc=1:stl=30:sac=on:add=off:afr=on:afp=100000:afq=1.1:amm=off:anc=none:sp=reverse_arity:urr=on:updr=off_4ott+11_2:1_bd=off:ile=on:irw=on:lma=on:nm=64:newcnf=on:nwc=1:av=off_6 --time_statistics on -p off -t 10s"
    name1 = sys.argv[2]
    name2 = sys.argv[6]
    rows, rowb = read(name1.split("/")[-1], name2)
    headers = ['Problem', 'Strategy', 'Clockname', 'Overall time', 'Own time']
    with open('test1.csv', 'a+')as f:
        f_csv = csv.writer(f)
        # f_csv.writerow(headers)
        f_csv.writerows(rows)
        f.close()
    with open('test2.csv', 'a+')as f2:
        f_csv = csv.writer(f2)
        # f_csv.writerow(headers)
        f_csv.writerow(rowb)
        f2.close()


