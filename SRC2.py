
# Required Modules

import os
from re import sub 
from sys import * 
import hashlib
import time 
import schedule

# ////////////////////////////////////////////
#   
#   Function Name : removeDuplicates 
#   Usage  :   remove duplicate files by skipping original Files 
#   input  :   Dictionary which contain {key : [hashcode] , value : [path_of_a_file]}
#   output :   Delete Duplicate Files Completely
#
# ////////////////////////////////////////////

def removeDuplicates(dict1):
    duplicates = list(filter(lambda x : len(x) > 1 , dict1.values()))
    # print(dict1)
    iCnt = 0 
    if (len(duplicates )> 0):
        for result in duplicates:
            for subresult in result :
                iCnt = iCnt + 1 

                # For Skipping 1 iteration i.e . Skipping original File : 
                if iCnt > 1 :
                    print("Removing :: " , subresult)
                    os.remove(subresult)
            iCnt = 0 
    else :
        print("No Duplicates Found :")

# ////////////////////////////////////////////

# ////////////////////////////////////////////
#   
#   Function Name : hasfile 
#   Usage : to hash file in hexadecimal number to uniquely identify the file
#   input : path of file , blocksize to read file 
#   output : return hexadecimal number of file
#
# ////////////////////////////////////////////

def hashfile(path , blocksize = 4096):
    afile = open (path , 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)

    while len(buf)>0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    # print("--------------------------" , hasher.hexdigest )
    return hasher.hexdigest()

# ////////////////////////////////////////////

# ////////////////////////////////////////////
#   
#   Function Name : treavelDirectory 
#   Usage : To travel firectory , sub directory in it to hash file 
#   input : abs path of file 
#   output : return list of hashdecimal value of files
# 
# ////////////////////////////////////////////

def findDuplicates(path):
    exists = os.path.isdir(path)
    dups = {} #Dictionary
    if exists :
        print("Scanning Files ......")
        for dirName  , subdirs  , fileList in os.walk(path):
            # print("Current Folder is : " , dirName , "***********")
            for file in fileList :
                path = os.path.join(dirName , file)
                print("File Name : : \t\t" , path)
                file_hash = hashfile(path)
                if file_hash in dups :
                    dups[file_hash].append(path)
                else : 
                    dups[file_hash] = [path]
    
    return dups
# ////////////////////////////////////////////


# ////////////////////////////////////////////
#   
#   Function Name : printDuplicate 
#   Usage : to hash file in hesadecimal number to uniquely identify the file
#   input : path of file , blocksize to read file 
#   output : return hexadecimal number of file
# 
# ////////////////////////////////////////////

def printDuplicate (dict1):
    iSize = 0 
    iCount = 0 
    dulplicateList = list(filter(lambda x : len(x) > 1 , dict1.values()))
    if(len(dulplicateList) > 0):
        print("Duplcaite File Are  ")
        # print(dulplicateList)
        for result in dulplicateList:
            # print("Result ::: " , result)
            for subresult in result : 
                # print("subresult :: " , subresult)
                iSize = iSize + os.path.getsize(subresult)
                iCount = 1 +  iCount
                print(subresult)

    return iSize,iCount
# ////////////////////////////////////////////

# ////////////////////////////////////////////
#   
#   Function Name : printSize 
#   Usage : To Print Duplicate file sizes
#   input : Size , Count 
#   output : Display File Count and size
# 
# ////////////////////////////////////////////


def printSize(iSize , iCount):
        print("\n")
        print("Duplicate Files Count is : " , iCount)
        print("Duplicate Files Data Size : " ,( iSize /1024/1024/1024), "GB")
        print("Duplicate Files Data Size : " ,( iSize /1024/1024), "MB")

        print("\n")

# ////////////////////////////////////////////

# ////////////////////////////////////////////
#   
#   Function Name : reoveEmptyDirs 
#   Usage : To Remove All empty Directoies
#   input : path_of_directory 
#   output : remove empty directories
# 
# ////////////////////////////////////////////

def removeEmptyDirs(path):
    for dirName , subdirs , fileList in os.walk(path):
        print(dirName , " -----")
        for subdir in subdirs:
            path = os.path.join(dirName , subdir)
            lenX = os.listdir(path)
            print("Length is  : " , lenX)
            if (len(lenX) == 0 ):
                print("path is : " ,path)
                os.rmdir(path)

# Starter Function

def main():
    print ("\n\n#################################################################")
    print("------ Duplicate File Removal -----  ")
    print ("################################################################# \n\n")

    if len(argv)!= 2 :
        print("Invalid Number of Arguments : ")
        exit()
    
    if (argv[1] == '-h') or (argv[1] == '-H'):
        print("This Script is used to Detect Dulicate Files And remove them From System...\n\n")
        exit()
    
    if (argv[1] == '-u') or (argv[1] == '-U'):
        print("Uasge : ApllicationName Abs_Path_of_Directory\n\n")
        exit()

    try: 
        dict1 = {}
        startTime = time.time()   
        dict1 = findDuplicates(argv[1])
        iSize , iCount = printDuplicate(dict1)
        if (iCount == 0 ):
            print("No Duplicates Found :: \n\n")
        else : 
            printSize(iSize , iCount)
            # flag =  input(("\n\n Remove Files ? ( y or n )"))
            # if flag == 'y' :
            removeDuplicates(dict1)

        endTime = time.time()

        # flag =  input(("Remove empty Directories ? (y / n )"))
        # if flag == 'y' :
        removeEmptyDirs(argv[1])

        endTime = time.time()

        print("\n\nTook %s seconds to execute ... \n\n" %(endTime - startTime))
    
    except ValueError:
        print("Invalid DataType of input : ")
    except Exception as E :
        print("Unknown Error Occured : " , E)


# Scheduling Duplicate File Detection  :
if __name__ == "__main__":
    schedule.every(10).seconds.do(main)

while (True):
    schedule.run_pending()