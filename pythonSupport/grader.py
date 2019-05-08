import subprocess
import os
import sys

def gradingSetup(id):
    tests = []
    results = []
    for file in os.listdir("..\\assignmentFiles\\" + id + "\\tests"):
        tests.append(file)

    tests.sort()

    for file in os.listdir("..\\assignmentFiles\\" + id + "\\results"):
        results.append(file)

    results.sort()
    return tests, results

def grade(path, iden, runType):
    tests, results = gradingSetup(iden)
    score = 0
    if runType == 'CL':
        for x in range(len(tests)):
            cmdUser = os.popen("python " + "'" + path + "' " + "..\\assignmentFiles\\" + iden + "\\tests\\" + tests[x])
            user = cmdUser.read()
            cmdUser.close()
            cmdResult = os.popen("cat ..\\assignmentFiles\\" + iden + "\\results\\" + results[x])
            result = cmdResult.read()
            cmdResult.close()
            if user == result:
                score += 10
    else:
        for x in range(len(tests)):
            cmdUser = os.popen("cat ..\\assignmentFiles\\" + iden + "\\tests\\" + tests[x] + " | python " + "'" + path + "'")
            user = cmdUser.read()
            cmdUser.close()
            #cat test | python3 assigment.py
            cmdResult = os.popen("cat ..\\assignmentFiles\\" + iden + "\\results\\" + results[x])
            result = cmdResult.read()
            cmdResult.close()
            if user == result:
                score += 10
    return score
