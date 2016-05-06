import sys
import commands


def printPlatform(filename):
    output = commands.getoutput("lipo -info " + filename)
    list = output.split(" ")
    add_flag = False
    platform_list = []
    for item in list:
        if add_flag and (len(item) > 0):
            platform_list.append(item)
        elif "are:" in item:
            add_flag = True
    if len(platform_list) == 0:
        list = output.split("architecture: ")
        platform_list.append(list[1])
    return platform_list

def expandLib(filename, platforms):
    for platform_name in platforms:
        commands.getoutput("mkdir " + platform_name)
        commands.getoutput("lipo " + filename + " -thin " + platform_name + " -output " + platform_name + "/new.a")
    for platform_name in platforms:
        commands.getoutput("cd " + platform_name + " && ar xv new.a && cd ..")

def showLib(platforms):
    commands.getoutput("cd " + platforms[0])
    output = commands.getoutput("cd " + platforms[0] + "&& ls *.o && cd ..")
    commands.getoutput("cd ..")
    list = output.split("\n")
    print list

def deleteBinary(platforms, package_name):
    for platform_name in platforms:
        if "-" in package_name:
            cmd = "cd " + platform_name + " && rm " + package_name.replace("-", "") + ".o && cd .."
        else:
            cmd = "cd " + platform_name + " && rm *" + package_name + "* && cd .."
        commands.getoutput(cmd)

def clearCache(platforms):
    for platform in platforms:
        commands.getoutput("rm -rf " + platform)
    print "cache clear"

def regenerateBinary(filename, platforms):
    for platform in platforms:
        commands.getoutput("ar rcs " + filename + "." + platform + " " + platform + "/*.o ")
    cmd = "lipo -create"
    for platform in platforms:
        cmd += (" " + filename + "." + platform)
    cmd += " -output " + filename + ".new"
    commands.getoutput(cmd)

argvcount = len(sys.argv)
func = sys.argv[1]
if func == "-lp":
    filename = sys.argv[2].strip()
    list = printPlatform(filename)
    s = "This library contains:"
    for item in list:
        s += item
        s += " "
    print s
if func == "-lb":
    filename = sys.argv[2].strip()
    list = printPlatform(filename)
    expandLib(filename, list)
    showLib(list)
    clearCache(list)
if func == "-i" and len(sys.argv) >= 5:
    filename = sys.argv[2].strip()
    list = printPlatform(filename)
    expandLib(filename, list)
    if sys.argv[3] == "-rm":
        for i in range(4, len(sys.argv), 1):
            deleteBinary(list, sys.argv[i])
    elif sys.argv[3] == "-from":
        # print sys.argv[4]
        f=open(sys.argv[4],'r')
        while 1:
            line = f.readline().strip()
            if not line:
                break
            deleteBinary(list,line)
    f.close()
    regenerateBinary(filename, list)
    clearCache(list)
