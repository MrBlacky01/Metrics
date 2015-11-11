# -*- coding:utf-8 -*-
import sys
import re

def deletingForDelComments(code, listIter, delList):
    for iter in listIter:
        delList.append(code[iter.span()[0]:iter.span()[1]])
    for item in delList:
        code = code.replace(item, '')
    return  code

def delComments(code):
    delList = []
    listIter = re.finditer(r'\'[^\']*\'', code)
    code = deletingForDelComments(code, listIter, delList)


    listIter = re.finditer(r'\"[^\"]*\"', code)
    for iter in listIter:
        delList.append(code[iter.span()[0]:iter.span()[1]])
    for item in delList:
        code = code.replace(item, '')

    delList = []
    listIter = re.finditer(r'//.*\n', code)
    for iter in listIter:
        delList.append(code[iter.span()[0]:iter.span()[1]])
    for item in delList:
        code = code.replace(item[:len(item) - 1], '')

    delList = []
    listIter = re.finditer(r'/\*[\s\S]*\*/', code)
    code = deletingForDelComments(code, listIter, delList)


    print('-----------------corrected code------------------------\n'+code)
    return code

def allocateVaraible(listVarOfType, listOfString,regPhrase):
    for i in range(len(listOfString)):
        listOfString[i] = listOfString[i][len(regPhrase)+1:].strip()
        listVarOfType += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)', listOfString[i])
        for j in range(len(listVarOfType)):
            if '[' in listVarOfType[j]:
                listVarOfType[j] = listVarOfType[j][:listVarOfType[j].find('[')]
    return listVarOfType

def checkOfInputVarType(regPhrase,code):
    listOfString = []
    listVarOfType=[]
    listOfString += re.findall(r'%s\(.*\)' % regPhrase, code)
    allocateVaraible(listVarOfType, listOfString, regPhrase)
    return listVarOfType


def checkOfThirdVarType(regPhrase,code):
    listOfNeedString=[]
    listVarOfType = []
    listOfNeedString += re.findall(r'%s\s*\(.*\)' % regPhrase, code)
    allocateVaraible(listVarOfType, listOfNeedString, regPhrase)
    return listVarOfType


def workWithTypesOfVal (listVarOfType,allVariable,firstColumn,secondColumn):
    columnOfVar = 0
    for i in range(len(listVarOfType)):
        for j in range(len(allVariable)):
            if listVarOfType[i] in allVariable[j][columnOfVar]:
                allVariable[j][firstColumn] = 1
                allVariable[j][secondColumn] = 0
                #len(listVarOfType[i]) == len(allVariable[j][columnOfVar]) and

def chepinMetrick(code):
    constList = []
    constListString = []
    listOfVariableString = []
    columOfVarName = 0
    columOfInputVar = 1
    columOfModyfyVar = 2
    columOfRuledVar = 3
    columOfEmptyVar = 4
    listOfType = ['int', 'signed',  'unsigned', 'short', 'long',  'char', 'float', 'double']

    for item in listOfType:
        listOfVariableString += (re.findall(r'%s \s*.*[^{];' % item, code))
        for i in range(len(listOfVariableString)):
             if item in listOfVariableString[i]:
                listOfVariableString[i] = listOfVariableString[i][len(item):].strip()

    constListString += (re.findall(r'DEFINE \s*.*[^{];|define \s*.*[^{];', code))
    for i in range(len(constListString)):
        if 'define' in constListString[i]:
            constListString[i] = constListString[i][len('DEFINE'):].strip()

    listOfVariableTemp=[]
    for item in listOfVariableString:
        listOfVariableTemp += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)', item)

    for i in range(len(listOfVariableTemp)):
        if '[' in listOfVariableTemp[i]:
            listOfVariableTemp[i] = listOfVariableTemp[i][:listOfVariableTemp[i].find('[')]

    listOfVariable = []
    for item in listOfVariableTemp:
        if item not in listOfVariable:
            listOfVariable += [item]

    for i in range(len(listOfVariable)):
        if '[' in listOfVariable[i]:
            listOfVariable[i] = listOfVariable[i][:listOfVariable[i].find('[')]

    for item in constListString:
        constList += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)', item)


    for item in constList:
        listOfVariable += [item]

    variableInMetrick = []
    for item in listOfVariable:
        variableInMetrick += [[item,0,0,0,1]]

    listVarOfThirdtype=[]

    listVarOfThirdtype += checkOfThirdVarType('if',code)
    listVarOfThirdtype += checkOfThirdVarType('while',code)
    listVarOfThirdtype += checkOfThirdVarType('for',code)


    workWithTypesOfVal(listVarOfThirdtype, variableInMetrick, columOfRuledVar, columOfEmptyVar)


    listVarOfType = []
    metricList = []
    metricList += re.findall(r'=[^;\n]*',code)
    for i in range(len(metricList)):
        metricList[i] = metricList[i].strip()
        listVarOfType += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)', metricList[i])
        for j in range(len(listVarOfType)):
            if '[' in listVarOfType[j]:
                listVarOfType[j] = listVarOfType[j][:listVarOfType[j].find('[')]

    workWithTypesOfVal(listVarOfType,variableInMetrick,columOfEmptyVar,columOfEmptyVar)

    metricList = []
    listVarOfType=[]
    metricList += re.findall(r'scanf\(.*\)',code)
    for i in range(len(metricList)):
        metricList[i] = metricList[i][len('scanf ('):].strip()
        listVarOfType += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)', metricList[i])
        for j in range(len(listVarOfType)):
            if '&' in listVarOfType[j]:
                listVarOfType[j] = listVarOfType[j][:listVarOfType[j].find('[')]
            if '[' in listVarOfType[j]:
                listVarOfType[j] = listVarOfType[j][:listVarOfType[j].find('[')]

    workWithTypesOfVal(listVarOfType, variableInMetrick, columOfInputVar, columOfEmptyVar)

    listOfRegExpOfInputVar = ['gets', 'getchar', 'printf', 'puts', 'putchar']
    listVarOfType=[]

    for item in listOfRegExpOfInputVar:
        listVarOfType += checkOfInputVarType(item, code)

    workWithTypesOfVal(listVarOfType, variableInMetrick,columOfInputVar,columOfEmptyVar)

    listOfSecondType = []
    for i in range(len(variableInMetrick)):
        if  variableInMetrick[i][1] == 1:
            listOfSecondType += [variableInMetrick[i][0]]

    metricList = []
    listVarOfType=[]
    metricList += re.findall(r'[[a-zA-Z_]+[0-9]*]*[=+-][^;\n]*',code)
    for i in range(len(metricList)):
        metricList[i] = metricList[i][:metricList[i].find('=')].strip()
        listVarOfType += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)', metricList[i])
        for j in range(len(listVarOfType)):
            if '[' in listVarOfType[j]:
                listVarOfType[j] = listVarOfType[j][:listVarOfType[j].find('[')]

    for i in range(len(listVarOfType)):
        for j in range(len(variableInMetrick)):
            if len(listVarOfType[i]) == len(variableInMetrick[j][0]) and listVarOfType[i] in variableInMetrick[j][0] and listVarOfType[i] in listOfSecondType :
                variableInMetrick[j][columOfModyfyVar] = 1
                variableInMetrick[j][columOfEmptyVar] = 0

    for item in variableInMetrick:
        print(item)

    delList=[]
    for i in range(len(variableInMetrick)):
        if ''== variableInMetrick[i][0]:
            delList.append(variableInMetrick[i])
    for item in delList:
        variableInMetrick.remove(item)

    countOfInput=0
    countOfModify=0
    countOfRuled=0
    countOfEmpty = 0
    print('\n')
    for item in variableInMetrick:
        if item[columOfInputVar] == item[columOfModyfyVar] == item[columOfRuledVar] == item[columOfEmptyVar] == 0:
            countOfModify += 1
            #print(item[columOfVarName],' - Modify variable')
        elif item[columOfRuledVar] == 1:
            countOfRuled += 1
            #print(item[columOfVarName],' - Ruled variable')
        elif item[columOfModyfyVar] == 1 and item[columOfRuledVar] == 0 :
            countOfModify += 1
            #print(item[columOfVarName],' - Modify variable')
        elif item[columOfInputVar] == 1 and item[columOfModyfyVar] == 0 and item [columOfRuledVar] == 0:
            countOfInput += 1
            #print(item[columOfVarName],' - Input variable')
        elif item[columOfEmptyVar]== 1 :
            countOfEmpty +=1
            #print(item[columOfVarName],' - Empty variable')

    constCoefficientOfInputVar = 1
    constCoefficientOFModifyVar = 2
    constCoefficientOFRuledVar = 3
    constCoefficientOfEmptyVar = 0.5
    valueOfMetick = constCoefficientOfInputVar*countOfInput+constCoefficientOFModifyVar*abs(countOfModify)+constCoefficientOFRuledVar*countOfRuled+constCoefficientOfEmptyVar*countOfEmpty
    print('\nP(count of Input )=',countOfInput,';\n M(count of Modify)=', countOfModify, ';\n C(count of Ruled)=', countOfRuled, ';\n T(count of Empty)=', countOfEmpty,'\n')
    print('Value of Chepin Metrick = ', valueOfMetick)



def main():
    choice = None
    code = None
    while choice != 0:
        print("""
        1 - Проанализировать метрикой Чепина
        2 - Открыть файл с кодом (язык C)
        0 - Выйти
        """)
        try:
            choice = input("Ваш выбор: ")
        except:
            choice = None
        if choice == '1':
            if code:
                chepinMetrick(code)
            else:
                print("File with code is not loaded!")
        elif choice == '2':
            code = openfile()
            if code:
                print("-*-*-*-*-*-*-*-*-*code-*-*-*-*-*-*-*-*-*-*-*-")
                print(code)
                print('\n')
                code = delComments(code)

            else:
                print("Код недоступен")
        elif choice == '0':
            sys.exit()


def openfile():
    fileName ='test3.txt'
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


