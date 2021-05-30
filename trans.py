from google_trans_new import google_translator
import sys
import re

import string


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def loadFile(filename):
    f = open(filename, "r", encoding='utf8')
    lines = f.readlines()
    f.close()
    return lines


def saveFile(filename, lines):
    f = open(filename, "w", encoding='utf8')
    f.writelines(lines)
    f.close()


def transRun(lines):

    translator = google_translator()
    newLines = []
    for line in lines:
        match = re.search('#.*$', line)
        if match:
            if (isEnglish(match.group())):
                newLines.append(line)
                continue
            reText = translator.translate(match.group(), lang_tgt='ko')
            line = re.sub('#.*$', reText, line)
            print("=>", line)
            newLines.append(line)
        else:
            newLines.append(line)
    return newLines


if __name__ == '__main__':
    print("###" + sys.argv[1] + "###")
    lines = loadFile(sys.argv[1])
    lines = transRun(lines)
    saveFile(sys.argv[1], lines)
