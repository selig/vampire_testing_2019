import csv
import re
import sys

def read(problem, strategy):
    with open("commands_SMT.txt","r+") as file:
        lines = file.readlines()
        Totaltime = 0
        Status = "wrong"
        action = False
        rows = []
        for line in lines:
            row = []
            if "Time elapsed" in line:
                temp = line.split(":")[1]
                Totaltime = temp.split("s")[0]
            try:
                if "status" in line:
                    Status = line.split(" ")[3]
                elif "Time limit" in line:
                    Status = 0
            except IndexError as e:
                pass
            if action == True:
                line = line.replace("\n", "")
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
        rowb = [problem, strategy, Totaltime, Status]
    file.close()
    if Status == "wrong":
        print("error")
        exit()
    return rows, rowb


if __name__ == '__main__':
    name1 = ""
    name2 = ""
    try:
        name1 = sys.argv[4]
        name2 = sys.argv[8]
    except IndexError as e:
        print("white blank")
        exit()
    rows, rowb = read(name1.split("/")[-1], name2)
    with open('test1.csv', 'a+')as f:
        f_csv = csv.writer(f)
        f_csv.writerows(rows)
        f.close()
    with open('test2.csv', 'a+')as f2:
        f_csv = csv.writer(f2)
        f_csv.writerow(rowb)
        f2.close()


