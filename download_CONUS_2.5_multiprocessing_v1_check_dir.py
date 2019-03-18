from bs4 import *
from urllib.request import *
import os 
import shutil
import multiprocessing
import multiprocessing as mp
from itertools import repeat
from tqdm import tqdm
import time 

def CheckDir(dir_path):
    if not os.path.isdir(dir_path):
        print("{} not exists!".format(dir_path))
    
def CreatDirList(folder_list, path2save):
    ListDir = []
    for dire in folder_list:
        path = os.path.join(path2save, dire)
        ListDir.append(path)
    return ListDir

def checkListDir(folder_list):
    for i in range(len(folder_list)):
        if not os.path.isdir(folder_list[i]):
            print('dir {} not exists.'.format(folder_list[i]))
        else:
            continue

def getYear(url, path2save, year):
    content = urlopen(url).read()
    soup = BeautifulSoup(content, features="lxml")
    #the file path helps to create dir
    folderPath_list = []
    #help with the urls
    url_list = []
    for j in soup.findAll('a'):
        if j['href'][:4] == year:
            folder_path = path2save + year + '/' + j['href']
            folderPath_list.append(folder_path)
            url_path = url + j['href']
            url_list.append(url_path)
    return folderPath_list, url_list

def getMonth(url, folderPath):
    content_new = urlopen(url).read()
    soup_new = BeautifulSoup(content_new, features="lxml")
    folder_path_list = []
    day_url_list = []
    for j in soup_new.findAll('a'):
        #select the folder with number
        if any(i.isdigit() for i in j['href']):
            folder_path = folderPath + j['href']
            folder_path_list.append(folder_path)
            url_path = url + j['href']
            day_url_list.append(url_path)
        else:
            pass

    return folder_path_list, day_url_list

def getParaFile(para, url, para_dir_path):
    content = urlopen(url).read()
    soup_new = BeautifulSoup(content, features="lxml")
    file_url_list = []
    file_path_name_list = []
    for j in soup_new.findAll('a'):
        if j['href'][:6] == para:
            file_url = url + j['href']
            file_path_name = para_dir_path + '/' + j['href'] + '.dms'
            file_url_list.appand(file_url)
            file_path_name_list.append(file_path_name)
    #time.sleep(random.random() * 3)\
    time.sleep(1)
    return file_url_list, file_path_name_list
            
#download the file            
def Download(file_url, file_path_name):
    downloadfile = URLopener()
    downloadfile.retrieve(file_url, file_path_name)

if __name__ == '__main__':

    path2save = '/Users/sk/Downloads/debug_save_path_conus2.5/Download_2.5km_exists_folder/'
    CheckDir(path2save)
    url = "https://nomads.ncdc.noaa.gov/data/ndfd/"
    #give the wanted year data
    year_list = ['2015', '2016']
    year_list_path = CreatDirList(year_list, path2save)
    checkListDir(year_list_path)
    print('year folders exist!')
    #seperate run because the low speed. in order: ['YBUZ98', 'YCUZ98', 'YEUZ98']
    Para_list = ['YBUZ98', 'YCUZ98', 'YEUZ98']
    #multiprocessing pool
    cores = multiprocessing.cpu_count()

    for year in year_list:
        folderPath_list, url_list = getYear(url, path2save, year)
        checkListDir(folderPath_list)
        print("all month directories are existing")
        for i, url in enumerate(url_list):
            folder_path_list, day_url_list = getMonth(url, folderPath_list[i])
            checkListDir(folder_path_list)
            print("all day directories are existing")
            para_dir_path_list = []
            for parameter in Para_list:
                for folder_path in folder_path_list:
                    para_dir_path = folder_path + parameter
                    CheckDir(para_dir_path)
                    print("paramter {0} dir in folder {1} exists.".format(parameter, folder_path))
                    para_dir_path_list.append(para_dir_path)
                
                print("start multiprocessing...")
                #pool = mp.Pool(4)
                with mp.Pool(4) as pool:
                    results = pool.starmap(getParaFile, zip(repeat(parameter), day_url_list, para_dir_path_list))
                    print('get already the download links and directory: and )print it out')
                    print(results)
                    #results[x][0]
                    #results[x][1]
                    # p = mp.Process(target=Download, args=(results[x][0], results[x][1]))
                    # p. start()
                    # p.join()


                    
                    



   
