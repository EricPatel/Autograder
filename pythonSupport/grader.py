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

def gradePython(path, iden, runType):
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

def gradeC(path, fileName, iden, runType):
    tests, results = gradingSetup(iden)
    score = 0
    compile = subprocess.Popen(["gcc", path + "/" + fileName,  "-o", path + "/out"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile.wait()
    stdout, stderr = compile.communicate()
    #print(stderr.decode("utf-8"))
    if(stderr):
        #file = open("error.txt", "w+")
        #file.write(stderr.decode("utf-8"))
        return score
    if runType == 'CL':
        for x in range(len(tests)):
            cmdUser = os.popen("./" + "'" + path + "/out' " + "../assignmentFiles/" + iden + "/tests/" + tests[x])
            user = cmdUser.read()
            cmdUser.close()
            cmdResult = os.popen("cat ../assignmentFiles/" + iden + "/results/" + results[x])
            result = cmdResult.read()
            cmdResult.close()
            if user == result:
                score += 10
    else:
        for x in range(len(tests)):
            cmdUser = os.popen("cat ../assignmentFiles/" + iden + "/tests/" + tests[x] + " | ./" + "'" + path + "/out'")
            user = cmdUser.read()
            cmdUser.close()
            #cat test | python3 assigment.py
            cmdResult = os.popen("cat ../assignmentFiles/" + iden + "/results/" + results[x])
            result = cmdResult.read()
            cmdResult.close()
            if user == result:
                score += 10
    return score

def gradeJava(path, fileName, iden, runType):
    tests, results = gradingSetup(iden)
    score = 0
    compile = subprocess.Popen(["javac", path + "/" + fileName],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile.wait()
    stdout, stderr = compile.communicate()
    #print(stderr.decode("utf-8"))
    if(stderr):
        #file = open("error.txt", "w+")
        #file.write(stderr.decode("utf-8"))
        return score
    compiledFile = fileName.replace('java', 'class')
    if runType == 'CL':
        for x in range(len(tests)):
            cmdUser = os.popen("java " + "'" + path + "/" + compiledFile + "' " + "../assignmentFiles/" + iden + "/tests/" + tests[x])
            user = cmdUser.read()
            cmdUser.close()
            cmdResult = os.popen("cat ../assignmentFiles/" + iden + "/results/" + results[x])
            result = cmdResult.read()
            cmdResult.close()
            if user == result:
                score += 10
    else:
        for x in range(len(tests)):
            cmdUser = os.popen("cat ../assignmentFiles/" + iden + "/tests/" + tests[x] + " | java " + "'" + path + "/" + compiledFile + "'")
            user = cmdUser.read()
            cmdUser.close()
            #cat test | python3 assigment.py
            cmdResult = os.popen("cat ../assignmentFiles/" + iden + "/results/" + results[x])
            result = cmdResult.read()
            cmdResult.close()
            if user == result:
                score += 10
    return score
