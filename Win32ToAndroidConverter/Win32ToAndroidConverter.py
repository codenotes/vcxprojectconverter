from xmltodict import *

win32proj="C:/Users/gbrill/Documents/Visual Studio 2017/Projects/StaticLibrary1/Win32Project1/Win32Project1.vcxproj"
androidproj="C:/Users/gbrill/Documents/Visual Studio 2017/Projects/StaticLibrary1/StaticLibrary2android/StaticLibrary2android.vcxproj"

def load(s):
    with open(s) as fd:        doc = xmltodict.parse(fd.read())
        return doc

def save(doc, fname):
    with open(fname,"w") as fd2:
        xmltodict.unparse(doc,fd2,pretty=True)




#xmltodict.unparse


#doc['Project']['ItemGroup'][0].items()[1]
#(u'ProjectConfiguration', [OrderedDict([(u'@Include', u'Debug|Win32'), (u'Configuration', u'Debug'), (u'Platform', u'Win32')]), OrderedDict([(u'@Include', u'Release|Win32'), (u'Configuration', u'Release'), (u'Platform', u'Win32')]), OrderedDict([(u'@Include', u'Debug|x64'), (u'Configuration', u'Debug'), (u'Platform', u'x64')]), OrderedDict([(u'@Include', u'Release|x64'), (u'Configuration', u'Release'), (u'Platform', u'x64')])])
#>>> 

#>>> doc['Project']['ItemGroup'][2]
#OrderedDict([(u'ClCompile', OrderedDict([(u'@Include', u'Source.cpp')]))])

#x=doc['Project']['ItemGroup'][2]
#>>> x[u'ClCompile']
#OrderedDict([(u'@Include', u'Source.cpp')])

#>>> doc['Project']['ItemGroup'][1]['Text']['@Include']
#u'ReadMe.txt'
#>>> 

#>>> x[u'ClCompile'][u'@Include']
#u'Source.cpp'

#change filename
#doc['Project']['ItemGroup'][1]['Text']['@Include']='feedme.txt'

#>>> doc['Project'].keys()
#[u'@DefaultTargets', u'@ToolsVersion', u'@xmlns', u'ItemGroup', u'PropertyGroup', u'Import', u'ImportGroup', u'ItemDefinitionGroup']
#>>> doc['Project']['ItemGroup']
#[OrderedDict([(u'@Label', u'ProjectConfigurations'), (u'ProjectConfiguration', [OrderedDict([(u'@Include', u'Debug|Win32'), (u'Configuration', u'Debug'), (u'Platform', u'Win32')]), OrderedDict([(u'@Include', u'Release|Win32'), (u'Configuration', u'Release'), (u'Platform', u'Win32')]), OrderedDict([(u'@Include', u'Debug|x64'), (u'Configuration', u'Debug'), (u'Platform', u'x64')]), OrderedDict([(u'@Include', u'Release|x64'), (u'Configuration', u'Release'), (u'Platform', u'x64')])])]), OrderedDict([(u'Text', OrderedDict([(u'@Include', 'feedme.txt')]))]), OrderedDict([(u'ClCompile', OrderedDict([(u'@Include', u'Source.cpp')]))])]
#>>> 


x=doc['Project']['ItemGroup'][2]
x[u'ClCompile'][u'@Include']

#project configurations:
doc['Project']['ItemGroup'][0]

#property group
doc['Project']['PropertyGroup']

#>>> doc['Project']['PropertyGroup'][0].keys()
[u'@Label', u'VCProjectVersion', u'ProjectGuid', u'Keyword', u'RootNamespace', u'WindowsTargetPlatformVersion']

#>>> doc['Project']['PropertyGroup'][0]['ProjectGuid']
u'{A3A3C9C1-C0F3-4CF0-B1F7-B9279CAA1FC7}'

#>>> doc['Project']['ItemGroup'][0]['ProjectConfiguration'][0]
OrderedDict([(u'@Include', u'Debug|Win32'), (u'Configuration', u'Debug'), (u'Platform', u'Win32')])
#>>> doc['Project']['ItemGroup'][0]['ProjectConfiguration'][1]
OrderedDict([(u'@Include', u'Release|Win32'), (u'Configuration', u'Release'), (u'Platform', u'Win32')])

#doc['Project']['ItemGroup'][0]['ProjectConfiguration'][0]['@Include']
u'Debug|Win32'
#doc['Project']['ItemGroup'][0]['ProjectConfiguration'][1]['@Include']
u'Release|Win32'
#doc['Project']['ItemGroup'][0]['ProjectConfiguration'][2]['@Include']
u'Debug|x64'
#doc['Project']['ItemGroup'][0]['ProjectConfiguration'][3]['@Include']
u'Release|x64'

def getProjectTypes(lib):
    configs=lib['Project']['ItemGroup'][0]['ProjectConfiguration']
    l=[]
    for x in configs:
        l.append( x['@Include'])
    return l

#eg, getPreProc(doc,'Debug|Win32')
def getPreProc(lib,include):
    defs=doc['Project']['ItemDefinitionGroup']
    d={}
    for x in defs:
        d[ x['@Condition'].split("==")[1][1:-1] ]= x['ClCompile']['PreprocessorDefinitions']
    return d
    