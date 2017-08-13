import xmltodict

#win32proj="C:/Users/gbrill/Documents/Visual Studio 2017/Projects/StaticLibrary1/Win32Project1/Win32Project1.vcxproj"
#androidproj="C:/Users/gbrill/Documents/Visual Studio 2017/Projects/StaticLibrary1/StaticLibrary2android/StaticLibrary2android.vcxproj"

win32proj="C:/repos/vcxprojectconverter/StaticLibrary1Win32/StaticLibrary1Win32.vcxproj"
androidproj="C:/repos/vcxprojectconverter/StaticLibrary1Android/StaticLibrary1Android.vcxproj"

def load(s):
    with open(s) as fd:
        doc = xmltodict.parse(fd.read())
        return doc

def save(doc, fname):
    with open(fname,"w") as fd2:
        xmltodict.unparse(doc,fd2,pretty=True)

w=load(win32proj)
a=load(androidproj)


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


#x=doc['Project']['ItemGroup'][2]
#x[u'ClCompile'][u'@Include']

#project configurations:
#doc['Project']['ItemGroup'][0]

#property group
#doc['Project']['PropertyGroup']

#>>> doc['Project']['PropertyGroup'][0].keys()
#[u'@Label', u'VCProjectVersion', u'ProjectGuid', u'Keyword', u'RootNamespace', u'WindowsTargetPlatformVersion']

#>>> doc['Project']['PropertyGroup'][0]['ProjectGuid']
#u'{A3A3C9C1-C0F3-4CF0-B1F7-B9279CAA1FC7}'

#>>> doc['Project']['ItemGroup'][0]['ProjectConfiguration'][0]
#OrderedDict([(u'@Include', u'Debug|Win32'), (u'Configuration', u'Debug'), (u'Platform', u'Win32')])
#>>> doc['Project']['ItemGroup'][0]['ProjectConfiguration'][1]
#OrderedDict([(u'@Include', u'Release|Win32'), (u'Configuration', u'Release'), (u'Platform', u'Win32')])

#doc['Project']['ItemGroup'][0]['ProjectConfiguration'][0]['@Include']
#u'Debug|Win32'
#doc['Project']['ItemGroup'][0]['ProjectConfiguration'][1]['@Include']
#u'Release|Win32'
#doc['Project']['ItemGroup'][0]['ProjectConfiguration'][2]['@Include']
#u'Debug|x64'
#doc['Project']['ItemGroup'][0]['ProjectConfiguration'][3]['@Include']
#u'Release|x64'

no_transfer_files=['stdafx.cpp']
no_transfer_includes=['%(AdditionalIncludeDirectories)']
no_transfer_preproc=['WIN32','NDEBUG','_LIB','_DEBUG','%(PreprocessorDefinitions)']


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

def getPreProc(lib,target):
    defs=lib['Project']['ItemDefinitionGroup']
    for x in defs:
        if  x['@Condition'].split("==")[1][1:-1]==target:
            return x['ClCompile']['PreprocessorDefinitions']

def getIncludes(lib,target):
    defs=lib['Project']['ItemDefinitionGroup']
    for x in defs:
        try:
            if  x['@Condition'].split("==")[1][1:-1]==target:
                return x['ClCompile']['AdditionalIncludeDirectories']
        except:
            print "There were no include directories for target"
            return ''




t="C:/repos/vcxprojectconverter/Win32ToAndroidConverter/template.xml"    
t=load(t)

def getSourceFiles(lib):
    ll=[]
    for k in lib['Project']['ItemGroup']:
        if u'ClCompile' in k.keys():
            for o in k['ClCompile']:
                if '@Include' in o.keys():
                    ll.append(o['@Include'])
    return ll       

def addFiles(lib,files):
    excluded= set(files) & set(no_transfer_files)

    ig=lib['Project']['ItemGroup']
    for x in lib['Project']['ItemGroup']:
        if x.keys()==[u'ClCompile']:
            for f in files:
                if f in excluded:
                    continue
                x[u'ClCompile'].extend( [  OrderedDict([(u'@Include', f) ]  )] )  #must be at least 2 in template or extend won't work

    #remove the first 2 fake ##NO_FILE##
    for x in lib['Project']['ItemGroup']:
        if x.keys()==[u'ClCompile']:
            x[u'ClCompile']=x[u'ClCompile'][2:]
            return


        



def setPreProc(lib, define):
    lib['Project']['ItemDefinitionGroup'][3]['ClCompile']['PreprocessorDefinitions']

#def setInclude(lib, define):
#    s="'$(Configuration)|$(Platform)'=='%s'"%define
#    lib['Project']['ItemDefinitionGroup'][3]['ClCompile']['AdditionalIncludeDirectories']


#t['Project']['ItemGroup'][1]['ClCompile'], 2 ordered dictionaries
#adding file, t['Project']['ItemGroup'][1]['ClCompile'].append( OrderedDict([(u'@Include', u'ThirdFile.cpp')]) )

def setInclude(lib,target,includes):
    for x in lib['Project']['ItemDefinitionGroup']:
        s= x['@Condition'].split("==")[1][1:-1]
        if(s==target):
            x['ClCompile']['AdditionalIncludeDirectories']=includes


def setPreProc_(lib,target,pres):
    for x in lib['Project']['ItemDefinitionGroup']:
        s= x['@Condition'].split("==")[1][1:-1]
        if(s==target):
            x['ClCompile']['PreprocessorDefinitions']=includes


for x in t['Project']['ItemGroup']:
    if x.keys()==[u'ClCompile']:
        print x[u'ClCompile']


for k in w['Project']['ItemGroup']:
    if u'ClCompile' in k.keys():
        if 'Include' in x[ u'ClCompile'].keys():
            print x[ u'ClCompile']['Include']


def addDelimItemToList(source,item,replaceHolder, listType=None):
    l=source.split(";")
    
    #if we were given something that is exlucded, just send soure back and don't add anything
    if listType=="preprocessor":
            if item in no_transfer_preproc:
                return source
    elif listType=="includes":
            if item in no_transfer_includes:
                return source

    if replaceHolder=='':
        l.append(item)
    else:
        l = [w.replace(replaceHolder, item) for w in l]

    
        
        
    return ";".join(l)






def setPreProc(lib,target,preproc,  replaceHolder=True):
    for x in lib['Project']['ItemDefinitionGroup']:
        s= x['@Condition'].split("==")[1][1:-1]
        if(s==target):
            pp=x['ClCompile']['PreprocessorDefinitions']
            x['ClCompile']['PreprocessorDefinitions']=addDelimItemToList(pp,preproc, "##PREPROC##" if replaceHolder else '')
            

def setInclude(lib,target,incl,replaceHolder=True):
    for x in lib['Project']['ItemDefinitionGroup']:
        s= x['@Condition'].split("==")[1][1:-1]
        if(s==target):
            pp=x['ClCompile']['AdditionalIncludeDirectories']
            x['ClCompile']['AdditionalIncludeDirectories']=addDelimItemToList(pp,incl, "##INCLUDE##" if replaceHolder else '')


#getPreProc(t,p[1])

#assumption is that there is a 64 release and debug on win32 that we will use as our base
def doit(sourceproj, destproj, useMappedTargets=False):
    st=getProjectTypes(sourceproj)
    sd=getProjectTypes(destproj)
    debMap={ u'Debug|x64': [u'Debug|ARM',  u'Debug|ARM64', u'Debug|x64',  u'Debug|x86'] }
    relMap={ u'Release|x64': [u'Release|ARM',  u'Release|ARM64', u'Release|x64',  u'Release|x86'] }
    
    commonTargets =list(set(st) & set (sd))
    
    
    allTargets = st+sd
    destTargets=sd
    #print 'common targets are:',commonTargets

    includesForTemplate={}
    preprocForTemplate={}
    filesForTemplate=getSourceFiles(sourceproj)

    if useMappedTargets: 
         for d in debMap[u'Debug|x64']:
            inc=getIncludes(sourceproj,u'Debug|x64')
            includesForTemplate[u'Debug|x64']=inc
            pp=getPreProc(sourceproj,u'Debug|x64')
            preprocForTemplate[u'Debug|x64']=pp
         for r in relMap[u'Release|x64']:
            inc=getIncludes(sourceproj,u'Release|x64')
            includesForTemplate[u'Release|x64']=inc
            pp=getPreProc(sourceproj,u'Release|x64')
            preprocForTemplate[u'Release|x64']=pp
    else:
        for target in commonTargets:
            inc=getIncludes(sourceproj,target)
            includesForTemplate[target]=inc
            pp=getPreProc(sourceproj,target)
            preprocForTemplate[target]=pp
            sf=getSourceFiles(sourceproj)
       

    print 'includes (setInclude)',includesForTemplate
    print 'preproc (setPreProc)',preprocForTemplate
    print 'files (addFiles)',filesForTemplate

    if useMappedTargets:
        for d in debMap[u'Debug|x64']: #all debug targets on dest
            setInclude(destproj,d,includesForTemplate[u'Debug|x64'])
            setPreProc(destproj,d,preprocForTemplate[u'Debug|x64'])
        for r in relMap[u'Release|x64']: #all release targets on dest
            setInclude(destproj,r,includesForTemplate[u'Release|x64'])
            setPreProc(destproj,r,preprocForTemplate[u'Release|x64'])
            ##set everything EXCEPT files, because there is only one place where that is done in the XML
    else: #pair up only the targets that match
        destTargets=getProjectTypes(destproj)
        for t in destTargets:
            if(t in commonTargets):
                print 'working with:',t
                setInclude(destproj,t,includesForTemplate[t])
                setPreProc(destproj,t, preprocForTemplate[t])
    
    print filesForTemplate
    addFiles(destproj,filesForTemplate)

    return destproj
    #return [includesForTemplate,preprocForTemplate,filesForTemplate]






#important "AdditionalINcludeDirs may not be present in all projects for win32...so make sure we put that in if it isn't
def testit(useMap=False):
    w=load(win32proj)
    a=load(androidproj)
    t="C:/repos/vcxprojectconverter/Win32ToAndroidConverter/template.xml"    
    t=load(t)

    doit(w,t,useMap)
    save(t,"c:/temp/t3.xml")
