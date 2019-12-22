#!/usr/bin/env python
# -*-coding:Latin-1 -*

# Synchronize directory <SOURCE_DIR>/<SUB_DIR> with directory <DEST_DIR>/<SUB_DIR>
#
# Requires Python 3


import os
import shutil


def main():

    # Directories
    SUB_DIR    = ""
    SOURCE_DIR = "C:\Dev\SyncDirectories\SRC"
    DEST_DIR   = "C:\Dev\SyncDirectories\DEST"

    # Add SUB_DIR to source and destination directories
    if SUB_DIR:
        SOURCE_DIR = os.path.join(SOURCE_DIR, SUB_DIR)
        DEST_DIR   = os.path.join(DEST_DIR, SUB_DIR)

    syncDirectoryClean(SOURCE_DIR, DEST_DIR)
    syncDirectoryCopy(SOURCE_DIR, DEST_DIR)

    print("Directories have been synchronized")


def syncDirectoryClean(SOURCE_DIR, DEST_DIR):

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
                os.remove(dstFile)


    # Print result
    print()
    print("Total Files  :", nbTotal)
    print("Files Removed:", nbRemoved)
    print()


def syncDirectoryCopy(SOURCE_DIR, DEST_DIR):

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
                os.makedirs(tmpDir)

            # If file does not exist in destination directory, copy it
            srcFile = os.path.join(dirname, filename)
            localFile = srcFile.replace(SOURCE_DIR, "")
            dstFile = os.path.join(DEST_DIR, localFile)
            if(not os.path.exists(dstFile)):
                # Copy file
                nbCopied += 1
                print("Copying", srcFile)
                shutil.copyfile(srcFile, dstFile)
            else:
                # Check sizes
                srcSize = os.path.getsize(srcFile)
                dstSize = os.path.getsize(dstFile)
                differentSizes = (srcSize != dstSize)
                #print("Sizes = ", srcSize, dstSize, differentSizes)

                # Check last modification dates
                # srcLastModifTime = os.path.getmtime(srcFile)
                # dstLastModifTime = os.path.getmtime(dstFile)
                #srcModified = (srcLastModifTime > dstLastModifTime)

                replaceFile = differentSizes
                #replaceFile = differentSizes or modified

                # Replace file iff neded
                if(replaceFile):
                    nbReplaced += 1
                    print("Replacing", srcFile)
                    shutil.copyfile(srcFile, dstFile)


    # Print result
    print()
    print("Total Files   :", nbTotal)
    print("Copied Files  :", nbCopied)
    print("Replaced Files:", nbReplaced)
    print()


main()

# Wait for user input to close program (Windows)
os.system("pause")
