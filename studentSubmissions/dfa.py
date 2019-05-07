import sys
while(sys.stdin.readline().strip() != "begin_rules"):
    continue

line = sys.stdin.readline().split()
rules = {}

while(line[0] != 'end_rules'):
    rules[(line[0], line[4])] = line[2]
    line = sys.stdin.readline().split()

start = sys.stdin.readline().split()[1]
end = sys.stdin.readline().split()[1:]

while(1):
    state = start
    line = sys.stdin.readline().strip()
    if(len(line) < 1):
        exit()
    for i in line:
        state = rules.get((state, i))
    if state in end:
        print("accepted")
    else:
        print("rejected")