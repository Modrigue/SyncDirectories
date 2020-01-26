#!/usr/bin/env python
# -*-coding:Latin-1 -*

# Synchronize directory <SOURCE_DIR>/<SUB_DIR> with directory <DEST_DIR>/<SUB_DIR>
#
# Requires:
# - Python 3
# - "diff" directory in this script's current directory


import os
import platform
import shlex
import shutil
import sys, getopt

from subprocess import Popen, PIPE


def main(argv):

    SOURCE_DIR = ""
    DEST_DIR = ""
    checkFilesDifference = False
    simulate = False

    try:
        opts, args = getopt.getopt(argv,"hs:d:ct",["help","srcdir=","dstdir=","checkdiff","test"])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()
            sys.exit()
        elif opt in ("-s", "--srcdir"):
            SOURCE_DIR = arg
        elif opt in ("-d", "--dstdir"):
            DEST_DIR = arg
        elif opt == '-c':
            # Check precise files differences
            print("Check files differences ON")
            checkFilesDifference = True
        elif opt == '-t':
            # Test simulate synchronization
            print("Simulation test ON")   
            simulate = True
   
    print('Source directory:      "' + SOURCE_DIR + '"')
    print('Destination directory: "' + DEST_DIR + '"')
    print()
    
    if(not SOURCE_DIR or not DEST_DIR):
        print('Error: source or destination directory is missing')
        return

    # Synchronize directories
    syncDirectoryClean(SOURCE_DIR, DEST_DIR, simulate)
    syncDirectoryCopy(SOURCE_DIR, DEST_DIR, checkFilesDifference, simulate)
    print("Directories have been synchronized")


def syncDirectoryClean(SOURCE_DIR, DEST_DIR, simulate = False):

    # Add "/" to source and destination directories if necessary
    if(SOURCE_DIR[len(SOURCE_DIR) - 1] != "/"):
        SOURCE_DIR += "/"
    if(DEST_DIR[len(DEST_DIR) - 1] != "/"):
        DEST_DIR += "/"
    
    # Check and change source directory
    if(not os.path.isdir(SOURCE_DIR)):
        print("ERROR: Source directory", SOURCE_DIR, "does not exist")
        os.system("pause")
        exit()

    # Create destination directory if not existing
    if(not os.path.isdir(DEST_DIR)):
        print("Creating directory", DEST_DIR)
        if(not simulate):
            os.makedirs(DEST_DIR)

    if(not simulate):  
        os.chdir(DEST_DIR)
        print("CLEANING", SOURCE_DIR, "->", DEST_DIR)
        print()

    # Rename source files to destination directory
    nbTotal  = 0
    nbRemoved = 0
    for dirname, dirnames, filenames in os.walk(DEST_DIR):

        #print("Processing directory", dirname)

        # If subdirectory does not exist in source directory, remove it
        localDir = dirname.replace(DEST_DIR, "")
        srcDir = os.path.join(SOURCE_DIR, localDir)
        if(not os.path.isdir(srcDir)):
            print("Removing directory", dirname)
            if(not simulate):
                shutil.rmtree(dirname)
            continue

        # Browse files
        for filename in filenames:
            nbTotal += 1

            # If file does not exist in source directory, remove it
            dstFile = os.path.join(dirname, filename)
            localFile = dstFile.replace(DEST_DIR, "")
            srcFile = os.path.join(SOURCE_DIR, localFile)
            if(not os.path.exists(srcFile)):
                nbRemoved += 1
                print("Removing", dstFile)
                if(not simulate):
                    os.remove(dstFile)


    # Print result
    print()
    print("Total Files  :", nbTotal)
    print("Files Removed:", nbRemoved)
    print()


def syncDirectoryCopy(SOURCE_DIR, DEST_DIR, checkFilesDifference = False, simulate = False):

    # Get program directory
    programDir = os.path.dirname(os.path.realpath(__file__))

    # Add "/" to source and destination directories if necessary
    if(SOURCE_DIR[len(SOURCE_DIR) - 1] != "/"):
        SOURCE_DIR += "/"
    if(DEST_DIR[len(DEST_DIR) - 1] != "/"):
        DEST_DIR += "/"

    # Check and change source directory
    if(not os.path.isdir(SOURCE_DIR)):
        print("ERROR: Source directory", SOURCE_DIR, "does not exist")
        os.system("pause")
        exit()
        
    os.chdir(SOURCE_DIR)
    print("COPYING", SOURCE_DIR, "->", DEST_DIR)
    print()

    # Rename source files to destination directory
    nbTotal  = 0
    nbCopied = 0
    nbReplaced = 0
    for dirname, dirnames, filenames in os.walk(SOURCE_DIR):

        #print("Processing directory", dirname)

        # Browse files
        for filename in filenames:
            nbTotal += 1

            # If subdirectory does not exist in destination directory, create it
            localDir = dirname.replace(SOURCE_DIR, "")
            tmpDir = os.path.join(DEST_DIR, localDir)
            if(not os.path.isdir(tmpDir)):
                print("Creating directory", tmpDir)
                if(not simulate):
                    os.makedirs(tmpDir)

            # If file does not exist in destination directory, copy it
            srcFile = os.path.join(dirname, filename)
            localFile = srcFile.replace(SOURCE_DIR, "")
            dstFile = os.path.join(DEST_DIR, localFile)
            if(not os.path.exists(dstFile)):
                # Copy file
                nbCopied += 1
                print("Copying", srcFile)
                if(not simulate):
                    shutil.copyfile(srcFile, dstFile)
            else:
                replaceFile = areFilesDifferent(srcFile, dstFile, checkFilesDifference, programDir)

                # Replace file iff needed
                if(replaceFile):
                    print("Replacing", srcFile)
                    if(not simulate):
                        try:
                            shutil.copyfile(srcFile, dstFile)
                            nbReplaced += 1
                        except:
                            print("Could not replace", dstFile, "(read only?)")


    # Print result
    print()
    print("Total Files   :", nbTotal)
    print("Copied Files  :", nbCopied)
    print("Replaced Files:", nbReplaced)
    print()


def areFilesDifferent(file1Path, file2Path, checkDifference = False, programDir = ""):
    
    # Check sizes
    file1Size = os.path.getsize(file1Path)
    file2Size = os.path.getsize(file2Path)
    differentSizes = (file1Size != file2Size)
    if(differentSizes):
        return True    

    # Disabled: Check last modification dates
    # file1LastModifTime = os.path.getmtime(file1Path)
    # file2LastModifTime = os.path.getmtime(file2Path)
    #modified = (file2LastModifTime > file1LastModifTime)
    #if(modified):
    #    return True  

    # Check files differences if option set
    if(checkDifference):
        file1Path = file1Path.replace('\\', '/')
        file2Path = file2Path.replace('\\', '/')
        if(not programDir):
            programDir = os.path.dirname(os.path.realpath(__file__))
        platformName = platform.system()
        progFile = "diff"
        if(platformName.lower() == "windows"):
            progFile = "diff.exe"
        diffFilePath = os.path.join(programDir, "diff", progFile).replace('\\', '/')
        cmd = diffFilePath + ' "' + file1Path + '" "' + file2Path + '"'
        #print("Diff command = " + cmd)
        process = Popen(shlex.split(cmd), stdout=PIPE)
        process.communicate()
        exitCode = process.wait()
        #print("Diff exit code = " + str(exitCode))
        return (exitCode != 0)
    else:
        return False

def printHelp():
    print()
    print('Usage: python syncDirectories.py -s <source_directory> -d <destination_directory>')
    print()
    print("Options:")
    print("  -s, --srcdir <dir>:    source directory used as reference for synchronization")
    print("  -d, --dstdir <dir>:    destination directory to synchronize")
    print("  -c, --checkdiff:       check precise files difference (slower)")
    print("  -t, --test:            test synchronization simulation (traces only, no effects)")
    print("  -h, --help:            display help")


if __name__ == "__main__":
    main(sys.argv[1:])

    # Wait for user input to close program (Windows)
    os.system("pause")
