import numpy as np
from PIL import Image
import os
import shutil


def compare(folder, fp1, fp2):
    # returns true if same, false if different. Takes in 2 file paths and maximum mse as arguments.
    fn1 = './img/' + folder + '/' + fp1
    fn2 = './img/' + folder + '/' + fp2
    if (not (fn1.lower().endswith(('.png', '.jpg', '.jpeg')) and fn2.lower().endswith(('.png', '.jpg', '.jpeg')))):
        return False
    try:
        image1 = Image.open(fn1)
        image2 = Image.open(fn2)
        if (image1.size != image2.size):
            return False
        if (image1 == image2):
            return True
        return False
        #image1.close()
        #image2.close()
    except:
        return False
    

def find_duplicates(folder):
    # creates 2d list where each element is another list of files that are the same image
    file_list = os.listdir("./img/" + folder)
    dups = []
    dup_element = []
    i = 0
    count = 0
    size = len(file_list)
    while (i < len(file_list)):
        fp1 = file_list[i]
        j = i + 1
        while (j < len(file_list)):
            #print(i)
            fp2 = file_list[j]
            if (compare(folder, fp1, fp2)):
                if (len(dup_element) == 0):
                    dup_element.append(fp1)
                dup_element.append(fp2)
                file_list.pop(j)
            else:
                j+=1
                count += 1 
                if (count % 1000 == 0):
                    print(f"{count} comparisons made out of max {(size/2)*(size + 1)}")
            
        if (len(dup_element) != 0):
            dups.append(dup_element.copy())
            dup_element.clear()
        i += 1
    return dups

def move_duplicates(folder, dups):
    # moves the file names in 2d list to another folder with subfolders for each element
    errfn = []
    if (len(dups) != 0):
        MYDIRDUPS = './img/' + folder + '/' + "duplicates"

        if not os.path.isdir(MYDIRDUPS):
            os.makedirs(MYDIRDUPS)
            print("created folder : ", MYDIRDUPS)

        else:
            print(MYDIRDUPS, "folder already exists.")  
        
        i = 0
        for dup in dups:
            MYDIRDUP = MYDIRDUPS + '/' + str(i)
            i += 1
            if not os.path.isdir(MYDIRDUP):
                os.makedirs(MYDIRDUP)
                print("created folder : ", MYDIRDUP)

            else:
                print(MYDIRDUP, "folder already exists.")  
            for o in dup:
                src = './img/' + folder + '/' + o
                dst = MYDIRDUP + '/' + o
                try:
                    shutil.move(src, dst)
                except WindowsError:
                    errfn.append(src)
                    pass
    return errfn


if __name__ == "__main__":
    folder = "Test"
    dups = find_duplicates(folder)
    errfn = move_duplicates(folder, dups)
    if (len(errfn) != 0):
        print("Could not move these files:")
        print(errfn)
    else:
        print("successfully moved duplicates")