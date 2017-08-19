import xmltodict
import itertools
from collections import OrderedDict
import re
import pprint
import os
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


#static library template for android
template_sed_static_library="C:/repos/vcxprojectconverter/StaticLibrary1Android/sed2.vcxproj"

#win32proj="C:/Users/gbrill/Documents/Visual Studio 2017/Projects/StaticLibrary1/Win32Project1/Win32Project1.vcxproj"
#androidproj="C:/Users/gbrill/Documents/Visual Studio 2017/Projects/StaticLibrary1/StaticLibrary2android/StaticLibrary2android.vcxproj"

RESET=   "\033[0m"
RED=     "\033[31m"     
GREEN=   "\033[32m"
YELLOW = "\033[33m"      
BLUE   = "\033[34m"      
MAGENTA =   "\033[35m"      
CYAN    =    "\033[36m"      
WHITE    =   "\033[37m"      
BOLDBLACK =  "\033[1m\033[30m"
BOLDRED    = "\033[1m\033[31m"
BOLDGREEN  = "\033[1m\033[32m"
BOLDYELLOW = "\033[1m\033[33m"
BOLDBLUE   = "\033[1m\033[34m"
BOLDMAGENTA ="\033[1m\033[35m"
BOLDCYAN    ="\033[1m\033[36m"
BOLDWHITE   ="\033[1m\033[37m"
INVERSEMAJ	="\033[45;7m" 
INVERSEYELLOW	="\033[43;7m" 
GREENBARWHITE	="\033[42;8m" 

#define ESC "\x1b"
#define CSI "\x1b["


def load(s):
    with open(s) as fd:
        doc = xmltodict.parse(fd.read())
        return doc

def save(doc, fname):
    with open(fname,"w") as fd2:
        xmltodict.unparse(doc,fd2,pretty=True)

#items not to carry over
no_transfer_files=['stdafx.cpp']
no_transfer_includes=['%(AdditionalIncludeDirectories)',u'$(Sysroot)\\usr\\include',u'$(StlIncludeDirectories)%(AdditionalIncludeDirectories)',u'$(StlIncludeDirectories)']
no_transfer_preproc=['WIN32','NDEBUG','_LIB','_DEBUG','%(PreprocessorDefinitions)','_USRDLL','_WINDOWS']

#items to insert special
add_transfer_preproc=['HAVE_MEMMOVE']

all_transfer_targets_source={}
all_transfer_targets_dest={}
final_transfer_preproc={}
final_transfer_includes={}
final_transfer_files=[]


def getProjectTypes(lib):
    configs=lib['Project']['ItemGroup'][0]['ProjectConfiguration']
    l=[]
    for x in configs:
        l.append( x['@Include'])
    return l

#eg, getPreProc(doc,'Debug|Win32')
#def getPreProc(lib,include):
#    defs=doc['Project']['ItemDefinitionGroup']
#    d={}
#    for x in defs:
#        d[ x['@Condition'].split("==")[1][1:-1] ]= x['ClCompile']['PreprocessorDefinitions']
#    return d

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
       # print '1'
        if u'ClCompile' in k.keys():
      #      print '2'
          #  print type(k['ClCompile'])
          #  for o in k['ClCompile']:
     #           print 3, type(o), type(k['ClCompile'])

                #t=type(o)
            #if t==dict:
            kc=k['ClCompile']
            #print kc,type(kc)
            if type(k['ClCompile']) in [unicode,str]:
                if '@Include' in k['ClCompile']:#o.keys(): #assumes o is a list, won't be if there is only one file, fails here
                #    print 4, k['ClCompile']['@Include']
                    #ll.append(o['@Include'])
                    ll.append(k['ClCompile']['@Include'])
            elif type(k['ClCompile']) in [list]: #it is a list of ordered dictionaries, ie: [OrderedDict([(u'@Include', u'xmlparse.c')]), OrderedDict([(u'@Include', u'xmlrole.c')]), ...
                for item in k['ClCompile']: #iterate through list of dictionaries
                    #   print item['@Include'] #for a given dictionary, get the file out
                    ll.append(item['@Include'])
            elif type(kc) in [OrderedDict]:
                for item in kc.keys():
                    ll.append(kc['@Include'])
                    

            else:
                print RED+"unknown type in getSourceFiles"+RESET,type(k['ClCompile'])
    return ll       
     
                #elif t==unicode:
                #    print 'THING:',o, o['@Include']
                #    exit()
                #else:
                #    RED+"unknown type for file"+RESET
    #print 5

def addFiles(lib,files):
    excluded= set(files) & set(no_transfer_files)

    ig=lib['Project']['ItemGroup']
    for x in lib['Project']['ItemGroup']:
        if x.keys()==[u'ClCompile']:
            for f in files:
                if f in excluded:
                    continue
                else:
              #      print '%file',f,files
                    x[u'ClCompile'].extend( [  OrderedDict([(u'@Include', f) ]  )] )  #must be at least 2 in template or extend won't work

    #remove the first 2 fake ##NO_FILE##
    for x in lib['Project']['ItemGroup']:
        if x.keys()==[u'ClCompile']:
            x[u'ClCompile']=x[u'ClCompile'][2:]
            return


        



#def setPreProc(lib, define):
#    lib['Project']['ItemDefinitionGroup'][3]['ClCompile']['PreprocessorDefinitions']

#def setInclude(lib, define):
#    s="'$(Configuration)|$(Platform)'=='%s'"%define
#    lib['Project']['ItemDefinitionGroup'][3]['ClCompile']['AdditionalIncludeDirectories']


#t['Project']['ItemGroup'][1]['ClCompile'], 2 ordered dictionaries
#adding file, t['Project']['ItemGroup'][1]['ClCompile'].append( OrderedDict([(u'@Include', u'ThirdFile.cpp')]) )

#def setInclude(lib,target,includes):
#    for x in lib['Project']['ItemDefinitionGroup']:
#        s= x['@Condition'].split("==")[1][1:-1]
#        if(s==target):
#            x['ClCompile']['AdditionalIncludeDirectories']=includes


#def setPreProc_(lib,target,pres):
#    for x in lib['Project']['ItemDefinitionGroup']:
#        s= x['@Condition'].split("==")[1][1:-1]
#        if(s==target):
#            x['ClCompile']['PreprocessorDefinitions']=includes


#for x in t['Project']['ItemGroup']:
#    if x.keys()==[u'ClCompile']:
#        print x[u'ClCompile']


#for k in w['Project']['ItemGroup']:
#    if u'ClCompile' in k.keys():
#        if 'Include' in x[ u'ClCompile'].keys():
#            print x[ u'ClCompile']['Include']


def addDelimItemToList(source,item,replaceHolder, listType, target):
    #print '$$source:',source,"type:", listType,"item:",item
    l=source.split(";")

    #if replaceHolder=='':
    #    l.append(item)
    #else:
    #    l = [w.replace(replaceHolder, item) for w in l]

    #print "!!!",l,listType
    #print '***',listType,item
    #if we were given something that is exlucded, just send soure back and don't add anything
    if listType=="preprocessor":
      #  tmp=[x.split(';') for x in item]
      #  chain = itertools.chain(*tmp)
      #  print '1***new preproc',l,'remove:',no_transfer_preproc
      #item comes in ; delimited, so we need to split that
        l.extend(add_transfer_preproc)  
        

        item=item.split(";")
        item=set(item)-set(no_transfer_preproc)
        item=";".join(item)
        
    elif listType=="includes":
        l=set(l)-set(no_transfer_includes)
        #print '---new includes',l

    if replaceHolder=='':
        l.append(item)
    else:
        l = [w.replace(replaceHolder, item) for w in l]

    
    #remove empty from list
    
    #print listType,':',target,";".join(l)
    
    return l#";".join(l)






def setPreProc(lib,target,preproc,  replaceHolder=True):
    for x in lib['Project']['ItemDefinitionGroup']:
        s= x['@Condition'].split("==")[1][1:-1]
        if(s==target):
            pp=x['ClCompile']['PreprocessorDefinitions']
            #print '^^',preproc
            test=addDelimItemToList(pp,preproc, "##PREPROC##" if replaceHolder else '','preprocessor',target)
            #print '!!test!!',test
            x['ClCompile']['PreprocessorDefinitions']=test
            test=[x for x in test if x]
            final_transfer_preproc[target]=test
            
            

def setInclude(lib,target,incl,replaceHolder=True):
    for x in lib['Project']['ItemDefinitionGroup']:
        s= x['@Condition'].split("==")[1][1:-1]
        if(s==target):
            pp=x['ClCompile']['AdditionalIncludeDirectories']
            tmp=addDelimItemToList(pp,incl, "##INCLUDE##" if replaceHolder else '', 'includes',target)
            x['ClCompile']['AdditionalIncludeDirectories']=tmp
            print MAGENTA+'debg, include setting'+RESET,tmp
            final_transfer_includes[target]=tmp
        

#getPreProc(t,p[1])

#assumption is that there is a 64 release and debug on win32 that we will use as our base
def doit(sourceproj, destproj, useMappedTargets=True):
    global final_transfer_files
    global all_transfer_targets
    global all_transfer_targets_source
    global all_transfer_targets_dest

    st=getProjectTypes(sourceproj)
    sd=getProjectTypes(destproj)
    debMap={ u'Debug|x64': [u'Debug|ARM',  u'Debug|ARM64', u'Debug|x64',  u'Debug|x86'] }
    relMap={ u'Release|x64': [u'Release|ARM',  u'Release|ARM64', u'Release|x64',  u'Release|x86'] }
    
    commonTargets =list(set(st) & set (sd))
    all_transfer_targets_source=commonTargets
    allTargets = st+sd
    destTargets=sd
    all_transfer_targets_dest=destTargets
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
       

    pprint.pprint( includesForTemplate)
    pprint.pprint(preprocForTemplate)
    pprint.pprint(filesForTemplate)

    

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
    
    print 'filesToGo',filesForTemplate
    final_transfer_files=filesForTemplate

    addFiles(destproj,filesForTemplate)

    return destproj
    #return [includesForTemplate,preprocForTemplate,filesForTemplate]


#important "AdditionalINcludeDirs may not be present in all projects for win32...so make sure we put that in if it isn't
def testit(source, dest, file="c:/temp/t3.xml",useMap=True):
    w=load(source)
    t=load(dest)
  # t="C:/repos/vcxprojectconverter/Win32ToAndroidConverter/template.xml"     
  #  t=load(t)

    doit(w,t,useMap)
    save(t,file)


#for sed
def filesToClCompileString(files):
    fname_template="<ClCompile Include=\"%s\" />\n"
    
    def isList(fl):
        s=''
        for i in fl:
            s+=fname_template%i
        return s
    
    def isStr(fs):
        if ';' in fs:
            return isList( fs.split(';'))
        else: #just a single file
            return fname_template%files

    switchDict = {list: isList, str: isStr}

    return switchDict[type(files)](files)

#for sed
def includesOrPreprocToString(dirs, checkExists=False):

    def isList(fl):
        s=''
        return ";".join(fl)
    
    def isStr(fs):
        return fs


    switchDict = {list: isList, str: isStr, unicode: isStr}
    return switchDict[type(dirs)](dirs)


#template is the sed-ready file, but we will ultimately duplicate it to outproj, not change it in place
def doSed(template,outproj):
    fin_string = open(template, "r").read()
    print YELLOW+ 'Using template:' + RESET,GREEN+ template+RESET
    fout = open(outproj, "w")

    #prp=includesOrPreprocToString(  final_transfer_preproc)
    #final_transfer_includes
    #final_transfer_files
    print '--------------------------'
    #pprint.pprint(final_transfer_files)
    #pprint.pprint(final_transfer_includes)
    #pprint.pprint( final_transfer_preproc)

    files =filesToClCompileString(final_transfer_files)
    magicReg='(?=\s*?\<)' #folowed by whitespace or <
    for t in all_transfer_targets_dest:
        inc= includesOrPreprocToString(final_transfer_includes[t])
        prep= includesOrPreprocToString(final_transfer_preproc [t])
       # print t,'preproc', '#PREPROC_'+t
       # print t,'includes','#INCLUDE_'+t

        #replace string up intil the first < for the closing tag
        prep=prep.replace('\\','\\\\')
        fin_string = re.sub('\#PREPROC_'+t.replace('|','\|')+magicReg,prep,fin_string)
        swap='\#INCLUDE_'+t.replace('|','\|')+magicReg #'[^<]*'
        print RED+swap+RESET,GREEN+inc+RESET
        inc=inc.replace('\\','\\\\')
        fin_string = re.sub(swap, inc,fin_string)
      

    print YELLOW+'files:'+RESET,files,type(files)
    #print all_transfer_targets_source
    #print all_transfer_targets_dest
        
    #prep="SOMEPREP"
    #inc="c:/sominclude"
    #files="file1;file2"
    
    files=files.replace('\\','\\\\')
    fin_string = re.sub('\#NO_FILE', files,fin_string)

    #text=prep.sub(prep, text)
    #text=inc.sub(inc, text)
    #text=files.sub(files, text)

    fout.write(fin_string)
    fout.close()




def slnParse(sln):
    solutions=[]
    map={}
    dir=os.path.dirname(sln)
    print 'dir:', dir
    os.chdir(dir)
    fin_string = open(sln, "r").read()
    l=fin_string.split('\n')
    projects=[x for x in l if x[:7]=='Project']
    for x in projects:
        l=x.split(',')
        fp=l[1].replace('"','')
        pt=os.path.join(dir,fp).replace('/','\\')
        rl=os.path.abspath(fp).replace('/','\\')
        pt=pt.replace(' ','')
        rl=rl.replace(' ','')
        if os.path.isfile(rl):
            solutions.append(rl)
        elif os.path.isfile(pt):
            solutions.append(pt)
        else:
            print 'Neither is file:',pt,rl
    
      #  print 'abs:',rl
     #   print 'path:',pt

    l=[x for x in solutions if not os.path.isfile(x)]
    print 'projects with bad paths:',l
    for p in solutions:
        map[p]=p[:-8]+'_android.vcxproj'
    
    return map

def processSlnAndCreateAndroidProjects(slnFile):
    m=slnParse(slnFile)
    pprint.pprint(m)
    tem=load(template_main) #only need to load this once
    for k in m.keys():
        source=k
        dest=m[k]
        print 'Converting',GREEN+source+RESET,'to',MAGENTA+dest+RESET
        src=load(source)
        doit(src,tem) #read from template and write bullshit xml, but creates solution globals I use to sed later
        doSed(template_sed_static_library,dest) #replace real template_sed arguments with pro, inc,files generated in doit() call. create new .vcxproj at 'dest'
        exit() #temporary, I just wan to do one at a time



win32proj="C:/repos/vcxprojectconverter/StaticLibrary1Win32/StaticLibrary1Win32.vcxproj"
androidproj="C:/repos/vcxprojectconverter/StaticLibrary1Android/StaticLibrary1Android.vcxproj"
expat="C:/repos/log4cxx/libexpat/expat/lib/expat_static.vcxproj"
expat_android="C:/repos/log4cxx/libexpat/expat/lib/expat_static_android.vcxproj"

#main template we want to use, though it has no purpose so not sure if needed anymore.  Old code used to modify this, but now its just legacy
template_main="C:/repos/vcxprojectconverter/Win32ToAndroidConverter/template2.xml" 

expat_sln='C:/repos/log4cxx/libexpat/expat/lib/expat_static_android.sln'
#this has just one clinclude file in it, so useful for testing
only_one_file='C:/ros/gitsrc/roscpp_core/roscpp_serialization/buildit/roscpp_serialization.vcxproj'
kinetic_sln='C:/ros/SolutionFiles/kinetic_complete_client.sln'

if __name__  == "__main__":
    #testit(expat,template,'C:/repos/log4cxx/libexpat/expat/lib/expat_static_android.vcxproj')

   # w=load(expat)
   # t=load(template)
  # t="C:/repos/vcxprojectconverter/Win32ToAndroidConverter/template.xml"     
  #  t=load(t)
    
    #doit(w,t) #read from template and write bullshit xml
    #doSed(template_sed,expat_android) #'c:\\temp\\sedtest.xml') #replace real template arguments with pro, inc,files generated in doit() call
    processSlnAndCreateAndroidProjects(kinetic_sln)








   