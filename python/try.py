import os

tests = []
results = []

for file in os.listdir("tests"):
    tests.append(file)

for file in os.listdir("results"):
    results.append(file)

for x in range(len(tests)):
    user = os.popen("cat tests/" + tests[x] + " | python3 rpn.py").read()
    #cat test | python3 assigment.py
    result = os.popen("cat results/" + results[x]).read()
    if user == result :
        print("Passed " + tests[x])
    else:
        print("Failed " + tests[x])


#support python, java, C
