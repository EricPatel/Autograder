import subprocess
import os
import sys

def gradingSetup():
    tests = []
    results = []
    for file in os.listdir("../pythonSupport/tests"):
        tests.append(file)

    for file in os.listdir("../pythonSupport/results"):
        results.append(file)

    return tests, results

def grade(path):
    print(path, file=sys.stdout)
    tests, results = gradingSetup()
    score = 0
    total = 0
    for x in range(len(tests)):
        cmdUser = os.popen( "powershell.exe cat ../pythonSupport/tests/" + tests[x] + " | python " + '"' + path + '"')
        user = cmdUser.read()
        print(user)
        cmdUser.close()
        #cat test | python3 assigment.py
        cmdresult = os.popen("powershell.exe cat ../pythonSupport/results/" + results[x])
        result = cmdresult.read()
        print(result)
        cmdresult.close()
        if user == result:
            score += 10
        total += 10
    return score, total
