# -*- coding:utf-8 -*-
import sys
import re

def deletingOfIteration(code, listOfRepitings, delList):
    for iter in listOfRepitings:
        delList.append(code[iter.span()[0]:iter.span()[1]])
        print(iter.span())
    for item in delList:
        code = code.replace(item, '')
    return code

def delCommentsAndStringsConst(code):
    delList = []
    listOfRepitings = re.finditer(r'\'[^\']*\'', code)
    code = deletingOfIteration(code, listOfRepitings, delList)


    listOfRepitings = re.finditer(r'\"[^\"]*\"', code)
    for iter in listOfRepitings:
        delList.append(code[iter.span()[0]:iter.span()[1]])
    for item in delList:
        code = code.replace(item, '')

    delList = []
    listOfRepitings = re.finditer(r'//.*\n', code)
    for iter in listOfRepitings:
        delList.append(code[iter.span()[0]:iter.span()[1]])
    for item in delList:
        code = code.replace(item[:len(item) - 1], '')

    delList = []
    listOfRepitings = re.finditer(r'/\*[^/\*]*\*/', code)
    code = deletingOfIteration(code, listOfRepitings, delList)

    print('-----------------corrected code------------------------\n'+code)
    return code

def getFuntionsNames(code):
    listOfFunctions = []
    listOfType = ['int', 'signed',  'unsigned', 'short', 'long',  'char', 'float', 'double', 'void']
    listOfNameOfFunctions = []
    dictionaryOfFuncions = {}

    for type in listOfType:
        listOfFunctionsCode = []
        listOfFunctionsCode += re.finditer(r'%s\s*.*\s*\(.*\)\n*\{' % type, code)
        for item in listOfFunctionsCode:
            counterOfBrackets = -1
            i = item.span()[1]
            while (counterOfBrackets) and (i < len(code)):
                if code[i]=='}':
                    counterOfBrackets += 1
                if code[i]=='{':
                    counterOfBrackets -= 1
                i += 1
            listOfFunctions.append(code[item.span()[1]-1:i])

            i = item.span()[0]
            while not (code[i] == '(') :
                i += 1
            listOfNameOfFunctions.append((code[item.span()[0]+len(type):i]).strip())

    for i in range(len(listOfNameOfFunctions)):
        dictionaryOfFuncions[listOfNameOfFunctions[i]] = listOfFunctions[i]
    return dictionaryOfFuncions


def getFunctionMetric(code):
    listOfOperatorsNames = ['if', 'while', 'for']
    listOfOperatorsStrings = []
    result = 1
    for item in listOfOperatorsNames:
        listOfOperatorsStrings += re.finditer(r'%s\s*(.*)*\s*' % item, code)
    listOfOperatorsStrings += re.finditer(r'case\s*.*\s*:', code)
    result += len(listOfOperatorsStrings)

    return result


def calculateMcCabeMetric(code):
    valueOfMcCabeMetric = 0
    constOfConnectedComponents = 1
    getFuntionsNames(code)
    dictionaryOfFunctions = getFuntionsNames(code)
    dictionaryOfFunctionMetric = {}

    for i in dictionaryOfFunctions:
        print(i, '  ', dictionaryOfFunctions[i])
    for item in dictionaryOfFunctions:
        dictionaryOfFunctionMetric[item] = getFunctionMetric(dictionaryOfFunctions[item])
    for i in dictionaryOfFunctions:
        print('Название функции :', i, ';  число МакКейба для функции =', dictionaryOfFunctionMetric[i])
        valueOfMcCabeMetric += dictionaryOfFunctionMetric[i]
    valueOfMcCabeMetric = valueOfMcCabeMetric -len(dictionaryOfFunctionMetric)+constOfConnectedComponents
    print('Число Маккейба =  ', valueOfMcCabeMetric)





def main():
    choice = None
    code = None
    while choice != 0:
        print("""
        1 - Проанализировать метрикой Мак-Кейба
        2 - Открыть файл с кодом (язык C)
        0 - Выйти
        """)
        try:
            choice = input("Ваш выбор: ")
        except:
            choice = None
        if choice == '1':
            if code:
                calculateMcCabeMetric(code)
            else:
                print("File with code is not loaded!")
        elif choice == '2':
            code = openfile()
            if code:
                print("-*-*-*-*-*-*-*-*-*code-*-*-*-*-*-*-*-*-*-*-*-")
                print(code)
                print('\n')
                code = delCommentsAndStringsConst(code)
            else:
                print("Код недоступен")
        elif choice == '0':
            sys.exit()


def openfile():
    fileName =input("Введите имя файла: ")#'test1.txt'
       #input("Введите имя файла: ")

    try:
        f = open(fileName, "r")
        code = f.read()
    except FileNotFoundError:
        code = None
        f = None
    if f:
        print("File is loaded!")

    return code


if __name__ == "__main__":
    main()


