import re


win32proj="C:/repos/vcxprojectconverter/StaticLibrary1Win32/StaticLibrary1Win32.vcxproj"
androidproj="C:/repos/vcxprojectconverter/StaticLibrary1Android/StaticLibrary1Android.vcxproj"
expat="C:/repos/log4cxx/libexpat/expat/lib/expat_static.vcxproj"
template="C:/repos/vcxprojectconverter/Win32ToAndroidConverter/template_sed.xml" 
test_expat='C:/repos/log4cxx/libexpat/expat/lib/expat_static_test.vcxproj'

#prep = re.compile("\#\#PREPROC\#\#", re.MULTILINE)
#inc = re.compile("\#\#INCLUDE\#\#", re.MULTILINE)
#files = re.compile("\#\#NO_FILE\#\#", re.MULTILINE)

text = open(template, "r").read()
f = open(test_expat, "w")

prep="SOMEPREP"
inc="c:/sominclude"
files="file1;file2"


text = re.sub("\#\#PREPROC\#\#",prep,text)
text = re.sub("\#\#INCLUDE\#\#", inc,text)
text = re.sub("\#\#NO_FILE\#\#", files,text)

#text=prep.sub(prep, text)
#text=inc.sub(inc, text)
#text=files.sub(files, text)

f.write(text)
f.close()

def filesToClCompileString(files):
    fname_template="<ClCompile Include=%s />\n"
    
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


def includesOrPreprocToString(dirs, checkExists=False):

    def isList(fl):
        s=''
        return ";".join(fl)
    
    def isStr(fs):
        return fs

    switchDict = {list: isList, str: isStr}
    return switchDict[type(dirs)](dirs)

