'''
@authors: Indu
'''

import re
import sys

comOpsDict = {'= +=' : '==', '! +=' : '!=', '\* +\* ' : '**', '< +>' : '<>', '< +=' : '<=', '> +=' : '>=', '/ +/' : '//', '- +- ' : '--', '\+ +\+' : '++', '\+ +\=' : '+=', '- +\=' : '-=', '< +<': '<<', '> +>': '>>'}
lineFormatDict = {' - I - ':'-I- ', ' - W - ':'-W- ', ' - E - ':'-E- '}
count = 0


def chkSpacing(line):
    line = re.sub('([,:!?+\*/<>=-])', r' \1 ', line)
    line = re.sub(' +',' ',line)
    patternList = comOpsDict.keys()
    for pattern in patternList:
        line = re.sub(pattern, comOpsDict[pattern], line)
    patternList = lineFormatDict.keys()
    for pattern in patternList:
        line = re.sub(pattern, lineFormatDict[pattern], line)
    line = re.sub(r'(-+)\s+(?=\d)', r'\1', line)
    line = re.sub(r'\s([?.!,](?:\s|$))', r'\1', line)
    return line


def main(src):
    with open(src, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        # Find starting position
        startLine = 0
        for i, line in enumerate(lines):
            if line.startswith("try"):
                startLine = i
                break

        for i, line in enumerate(lines):
            print line
            if (i < startLine):
                f.write(line)
            elif "https:" in line or "pylint" in line:
                f.write(line)
            else:
                leading = len(line) - len(line.lstrip())
                line = chkSpacing(line)
                line = line.rjust(leading - 1 + len(line), " ")
                print line
                f.write(line)
        f.close()

if __name__ == '__main__':
    src = sys.argv[1]
    main(src)
