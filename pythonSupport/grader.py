import subprocess
import os
import sys

def gradingSetup(id):
    tests = []
    results = []
    for file in os.listdir("../assignmentFiles/" + id + "/tests"):
        tests.append(file)

    for file in os.listdir("../assignmentFiles/" + id + "/results"):
        results.append(file)

    return tests, results

def grade(path, iden):
    tests, results = gradingSetup(iden)
    score = 0
    total = 0
    for x in range(len(tests)):
        cmdUser = os.popen("powershell.exe cat ../assignmentFiles/" + iden + "/tests/" + tests[x] + " | python " + "'" + path + "'")
        user = cmdUser.read()
        cmdUser.close()
        #cat test | python3 assigment.py
        cmdResult = os.popen("powershell.exe cat ../assignmentFiles/" + iden + "/results/" + results[x])
        result = cmdResult.read()
        cmdResult.close()
        if user == result:
            score += 10
        total += 10
    return score, total
