import os
import sys
import re
import toml
import json
import hashlib
from pprint import pprint

## 0) change files
def GenDefineFile(folder, defFile="RmDumpDefine.h", enFile="file.cfg"):
    targetFiles = ["main.bak"]
    defineCodes = []
    allFileNames = []
    # 1) parse all files and merge
    parseDict = {}
    for item in targetFiles:
        parserRet = Parser(item)
        for key in parserRet.keys():
            if not key in parseDict:
                parseDict[key] = parserRet[key]

    # 2) extrct definecodes and allfileNames
    defineCodes = []
    allFileNames = []
    for key in parseDict.keys():
        defineCodes.extend(parseDict[key]["defineCodes"])
        allFileNames.extend(parseDict[key]["allFileNames"])


    # 2) gen define files
    with open(defFile, "w") as fn:
        fn.writelines("#ifndef RMDUMPDEFINE__H_\n")
        fn.writelines("#define RMDUMPDEFINE__H_\n")
        fn.writelines("\n".join(defineCodes))
        fn.writelines("\n")
        fn.writelines("#endif")
    with open(enFile, "w") as fn:
        allFileNames = list(set(allFileNames))
        allFileNames.sort()
        pprint(allFileNames)
        fn.writelines("\n".join(allFileNames))

    # 3) change oriFile
    defFileName = os.path.basename(defFile)
    for item in targetFiles:
        # extract definename and sorted by lineNum
        relPath = os.path.relpath(item)
        replaceDefines = {}
        for defineName in parseDict.keys():
            if relPath == parseDict[defineName]["filePath"]:
                for lineNum in parseDict[defineName]["lineNum"]:
                    replaceDefines[lineNum] = defineName
        # change ori files
        lines = []
        with open(relPath, "r") as fp:
            lines = fp.readlines()
        outLines = []
        with open("main.cpp", "w") as fp:
            hasInc = False
            for lineNum in range(len(lines))[::-1]:
                # add define codes
                lastBlank = re.match("(\s*)", lines[lineNum])
                if lastBlank:
                    lastBlank = lastBlank[0]
                else:
                    lastBlank = ""
                if not re.match("\s*RM_DUMP_FUNC_", lines[lineNum]):
                    outLines.append(lines[lineNum])
                if lineNum in replaceDefines.keys():
                    outLines.append(lastBlank + replaceDefines[lineNum]+"\n")
                # add include
                if re.findall(f"#include.*{defFileName}", lines[lineNum]):
                    hasInc = True
            if not hasInc:
                outLines.append(f'#include "{defFileName}"\n')
            fp.writelines(outLines[::-1])
        # pprint(outLines)
        pass

## 1) Paser RM DATA DUMP
def GetRmDumpStrs(fn):
    lines = None
    with open(fn, "r") as fp:
        lines = fp.readlines()

    ret = []
    for idx, line in enumerate(lines):
        reRet = re.findall(r"(?:RM_DUMP_FLAG\s*:\s*)(.*)(?:RM_DUMP_FLAG_END)", line)
        if reRet:
            retDict = {
                "lineNum": idx,
                "dumpStr": reRet[0],
            }
            ret.append(retDict)
    return ret

def ParseDumpStr2Toml(dumpStr):
    tomlDict = toml.loads(dumpStr.replace('||', '\n'))
    return tomlDict

def Parser(fn):
    # 0) output example
    """
    ret = {
        'RM_DUMP_FUNC_9197860a0d06558f775f0546e4461fcb': {
            'allFileNames': ['monitor_0.txt',
                            'monitor_1.txt',
                            'monitor_2.txt',
                            'monitor_3.txt'],
            'defineCodes': ['#define '
                            'RM_DUMP_FUNC_9197860a0d06558f775f0546e4461fcb '
                            '{ \\',
                            'char '
                            'fn[256] = '
                            '{0}; \\',
                            'sprintf(fn, '
                            '"monitor_%d.txt", '
                            'tti); \\',
                            'DUMP_FUNC::DumpData(fn, '
                            '"a+", '
                            'AVar, '
                            'BVar); \\',
                            '}'],
            'filePath': 'main.cpp',
            'lineNum': [30],
            'parseDict': {'_flag': 'a+',
                            '_name': 'monitor_{tti}.txt',
                            '_nameRaw': 'monitor_{int:tti|[0:3]}.txt',
                            '_nameVars': {'tti': {'range': [0,
                                                            1,
                                                            2,
                                                            3],
                                                'type': 'int:tti|[0'}},
                            '_vars': 'AVar, '
                                    'BVar'}},
        },
        "RM_DUMP_FUNC_8D46DFCB84E5AFC7B768DB6DFF40AA1A": {
            ...
        },
    }

    """
    # 1) find all rm dump strings
    relPath = os.path.relpath(fn)
    dumpInfos = GetRmDumpStrs(relPath)

    # 2) extract vars in dump string
    tomlList = []
    for idx, dumpInfo in enumerate(dumpInfos):
        # tomlList.append(ParseDumpStr2Toml(dumpInfo["dumpStr"]))
        dumpInfos[idx]["tomlDict"] = ParseDumpStr2Toml(dumpInfo["dumpStr"])

    # 3) parse vars in file name // TODO need change
    for idx, item in enumerate(dumpInfos):
        dictTmp = ParseName(item["tomlDict"]["_name"])
        for key in item["tomlDict"]:
            if not key in dictTmp.keys():
                dictTmp[key] = item["tomlDict"][key]
        dumpInfos[idx]["parseDict"] = dictTmp

    # 4) construct result dict framework
    parsedToml= {}
    for dumpInfo in dumpInfos:
        # use md5 to gen define name
        s = json.dumps(dumpInfo["tomlDict"]) + relPath
        hashTool = hashlib.md5()
        hashTool.update(s.encode("utf-8"))
        hashRet = hashTool.hexdigest()
        defineName = "RM_DUMP_FUNC_" + hashRet
        if defineName not in parsedToml.keys():
            parsedToml[defineName] = {
                "filePath": relPath,
                "lineNum": [dumpInfo["lineNum"]],
                "parseDict": dumpInfo["parseDict"],
                "defineCodes": [],
                "allFileNames": [],
            }
        else:
            parsedToml[defineName]["lineNum"].append(dumpInfo["lineNum"])

    # 5) generate #define code, to dump files
    # 5) -1) generate all file names according to _nameVars
    for defineName in parsedToml.keys():
        # fullFileNames.extend(GenAllFileNames(parsedDict["_name"], parsedDict["_nameVars"]))
        parseDict = parsedToml[defineName]["parseDict"]
        parsedToml[defineName]["allFileNames"] = GenAllFileNames(parseDict["_name"], parseDict["_nameVars"])

    # 5) -2) generate define code according to dict
    for defineName in parsedToml.keys():
        parseDict = parsedToml[defineName]["parseDict"]
        parsedToml[defineName]["defineCodes"] = GenDefineCode(defineName, parseDict)

    ret = parsedToml

    return ret

def ParseName(strIn):
    """
    parse input:
        monitor_{string:ssType|['CSS', 'USS']}_cfg{int:tti|[1,2,4]}.txt
    output to:
        dict = {
            _nameRaw: monitor_{string:ssType|['CSS', 'USS']}_cfg{int:tti|[1,2,4]}.txt,
            _name: monitor_{ssType}_cfg{tti}.txt,
            _nameVars: {
                ssType: {
                    type: string,
                    range: ['CSS', 'USS'],
                },
                tti: {
                    type: int,
                    range: [1,2,4],
                },
            }
        }
    """
    # 1) extract vars in file name string
    ret = {"_nameVars": {}}
    usrKeyStrs = re.findall(r"(?:\{)(.*?)(?:\})", strIn)
    # pprint(usrKeyStrs)
    for usrKeyStr in usrKeyStrs:
        ty       = re.findall(r"(.*)(?:\:)", usrKeyStr)[0].strip()
        usrKey   = re.findall(r"(?:\:)(.*)(?:\|)", usrKeyStr)[0].strip()
        rangeStr = re.findall(r"(?:\|)(.*)", usrKeyStr)[0].strip()
        ret["_nameVars"][usrKey] = {"type": ty, "range": ParseRange(rangeStr)}

    # 2) replace {} with key
    ret["_name"]    = re.sub(r"\{.*?\:(.*?)\|.*?\}", r"{\1}", strIn)
    ret["_nameRaw"] = strIn

    return ret

def ParseRange(rangeStr):
    ret = None
    colonPairs = re.findall(r"\[([+-]?\d+):([+-]?\d+):?([+-]?\d)?\]", rangeStr.replace(" ", ""))
    if not colonPairs:
        ret = eval(rangeStr)
    elif not colonPairs[0][2]: # 0:2
        ret = list(range(int(colonPairs[0][0]), int(colonPairs[0][1])+1))
    elif colonPairs[0][2]: # 0:2
        ret = list(range(int(colonPairs[0][0]), int(colonPairs[0][2])+1, int(colonPairs[0][1])))
    return ret

## 2) RM Code Gen
def GenDefineCode(defineName, paraDict):
    ret = [] # every line as a member, no \n
    ret.append(f"#define {defineName} " + "{")
    # 1) gen file name codes
    ret.extend(GenFileNameCode(paraDict))

    # 2) gen dump function calling codes
    ret.extend(GenDumpCallingCode(paraDict))

    # 3) merge all code into define codes
    ret = [x + " \\" for x in ret]
    ret.append(r"}")

    return ret

def GenDumpCallingCode(paraDict):
    ret = []
    codeStringList = []
    codeStringList.append(r"DUMP_FUNC::DumpData(fn")
    if "_flag" in paraDict.keys():
        codeStringList.append('"'+paraDict["_flag"]+'"')
    else:
        codeStringList.append('"w"')

    if "_vars" in paraDict.keys():
        varsList = paraDict["_vars"].split(",")
        varsList = [x.strip() for x in varsList]
        codeStringList.extend(varsList)

    codeString = ", ".join(codeStringList) + r");"
    ret.append(codeString)

    return ret

def GenFileNameCode(paraDict):
    ret = []
    # 1) fn declare
    ret.append(r"char fn[256] = {0};")

    # 2) fn string replace %s, %d
    fnStringList = []
    fnStringList.append(r"sprintf(fn")
    fnString = re.sub(r"\{(?P<type>.*?)\:(.*?)\|.*?\}", ChangeTypeFlag, paraDict["_nameRaw"])
    fnStringList.append('"'+fnString+'"')
    varsString = re.findall(r"(?:\{.*?\:)(.*?)(?:\|.*?\})", paraDict["_nameRaw"])
    for item in varsString:
        var = item.strip()
        if paraDict["_nameVars"][var]["type"] == "string":
            fnStringList.append(var+r".c_str()")
        else:
            fnStringList.append(var)
    fileNameString = ", ".join(fnStringList) + r");"
    ret.append(fileNameString)

    return ret

def ChangeTypeFlag(matched):
    typeStr = matched.group("type")
    ret = ""
    if typeStr == "string":
        ret = r"%s"
    elif typeStr == "int":
        ret = r"%d"
    return ret

def GenAllFileNames(strIn, nameVars):
    """ example
    nameVars = {'ssType': {'range': ['CSS', 'USS'], 'type': 'string'},
                'tti': {'range': [1, 2, 4], 'type': 'int'}}
    """
    usrKeyStrs = re.findall(r"(?:\{)(.*?)(?:\})", strIn)
    if not usrKeyStrs:
        return [strIn]
    ret = []
    usrKeyStr = usrKeyStrs[0]
    for item in nameVars[usrKeyStr]["range"]:
        replacedStr = re.sub("{"+f"{usrKeyStr}"+"}", str(item), strIn)
        ret.extend(GenAllFileNames(replacedStr, nameVars))
    return ret

