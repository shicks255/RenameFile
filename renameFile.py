# !python3

import re
import shutil
import os

def prompt_user_for_directory():
    print(os.getcwd())
    directory = input('Enter a directory \n')
    if directory == 'exit' or directory == 'quit':
        exit()
    else:
        goodPath = get_path(directory)

        if os.path.exists(goodPath) is not True:
            print('The entered value ' + goodPath + ' is not a valid absolute path.')
            prompt_user_for_directory()

        print_path_items(goodPath)
        pathIsGood = prompt_user_if_path_is_good()

        expressionString = ''
        if pathIsGood == 'y':
            expressionString = prompt_user_for_expression()
        if pathIsGood == 'n':
            prompt_user_for_directory()
        if pathIsGood == 'exit' or pathIsGood == 'quit':
            exit()

        if expressionString == 'exit' or expressionString == 'quit':
            exit()

        if len(expressionString.split(',')) < 2:
            print("Must have at least 2 strings separated by a comma.")
            prompt_user_for_expression()

        pathContents = os.listdir(goodPath)
        dictionary = rename_files__for_prompt(expressionString, pathContents)

        yesOrNo = prompt_user_to_rename(dictionary)
        if yesOrNo == 'y':
            rename_files_action(dictionary)
        if yesOrNo == 'exit' or yesOrNo == 'quit':
            exit()

        prompt_user_for_directory()

def get_path(directory):
    directory = os.path.abspath(directory)
    directoryChunks = directory.split('\\')
    directoryChunks.insert(1, '\\')
    goodPath = os.path.join(*directoryChunks)
    return goodPath


def print_path_items(path):
    os.chdir(path)
    print('Contents of ' + path + '\n\n')
    pathContents = os.listdir(path)
    for pathItem in pathContents:
        print(pathItem)
    print(os.getcwd())

def prompt_user_if_path_is_good():
    answer = input("Is this path ok?  Type y for yes, or n to adjust the path\n")
    return answer

def prompt_user_for_expression():
    remover_expression = input('Enter the text you want replace, following by the text to replace it with.'
                               'Enter * as a placeholder for the text being replaced.\n'
                               'Enter -end at the front of the replacement text to append '
                               'text to the end of the filename.\n')
    return remover_expression

def rename_files__for_prompt(remover_expression, pathContents):
    oldAndNewNameDictionary = {}

    expressionArguments = remover_expression.split(',')
    for item in pathContents:

        newName = ""

        replacementString = expressionArguments[1]

        if (expressionArguments[0].startswith('-end')):
            indexOfPeriod = item.index('.')
            newName = item[:indexOfPeriod] + replacementString + item[indexOfPeriod:]
        else:
            regex = re.compile(expressionArguments[0])
            mo = regex.search(item)
            if mo:
                if '*' in replacementString:
                    firstPart = replacementString[:replacementString.index('*')]
                    secondPart = replacementString[replacementString.index('*')+1:]
                    replacementText = firstPart + (mo.group().lstrip()) + secondPart
                    newName = item.replace(mo.group(), replacementText)
                else:
                    newName = item.replace(mo.group(), replacementString)

        if len(newName) > 0:
            newName = re.sub('\s+', ' ', newName)
            newName = re.sub('\s+[.]', '.', newName)
            newName = newName.lstrip()
            oldAndNewNameDictionary[item] = newName

    return oldAndNewNameDictionary

def prompt_user_to_rename(oldAndNewNameDictionary):
    print("The following changes will occur...")
    for key in oldAndNewNameDictionary.keys():
        print(key + " --> " + oldAndNewNameDictionary[key])
    answer = input("Press y to accept\n")
    return answer

def rename_files_action(oldAndNewNameDictionary):
    for key in oldAndNewNameDictionary.keys():
        if oldAndNewNameDictionary[key]:
            shutil.move(key, oldAndNewNameDictionary[key])

prompt_user_for_directory()
