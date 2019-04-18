import os
import trace
import subprocess

tests = []
results = []

for file in os.listdir("tests"):
    tests.append(file)

tests.sort()

for file in os.listdir("results"):
    results.append(file)

results.sort()


value = subprocess.Popen(["gcc", "first.c",  "-o", "out"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
value.wait()
stdout, stderr = value.communicate()
#print(stderr.decode("utf-8"))
if(stderr):
    file = open("error.txt", "w+")
    file.write(stderr.decode("utf-8"))
    print("Error: could not compile")
    exit()

for x in range(len(tests)):
    user = os.popen("./out tests/" + tests[x]).read()
    result = os.popen("cat results/" + results[x]).read()
    if user == result :
        print("Passed " + tests[x])
    else:
        print("Failed " + tests[x])

subprocess.Popen(["rm", "out"])
