from bs4 import *
from urllib.request import *
import os 
import shutil
import multiprocessing
import multiprocessing as mp
from itertools import repeat
from tqdm import tqdm
import time 
from pathlib import Path

def CheckDir(dir_path):
    if not os.path.isdir(dir_path):
        print("{} not exists!".format(dir_path))

def getYear(url, year):
    content = urlopen(url).read()
    soup = BeautifulSoup(content, features="lxml")
    #help with the urls
    url_list = []
    for j in soup.findAll('a'):
        if j['href'][:4] == year:
            url_path = url + j['href']
            url_list.append(url_path)
    return url_list

def getMonth(url):
    content_new = urlopen(url).read()
    soup_new = BeautifulSoup(content_new, features="lxml")
    day_url_list = []
    for j in soup_new.findAll('a'):
        #select the folder with number
        if any(i.isdigit() for i in j['href']):
            url_path = url + j['href']
            day_url_list.append(url_path)
        else:
            pass

    return day_url_list

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
    path2save = Path('/Volumes/Elements/Download_2.5km_folder_muster_umfolder/')
    #path2save = Path('/Users/sk/Downloads/debug_save_path_conus2.5/Download_2.5km_folder_muster_umfolder/')
    CheckDir(path2save)
    url = "https://nomads.ncdc.noaa.gov/data/ndfd/"
    #give the wanted year data
    year_list = ['2015', '2016']
    #seperate run because the low speed. in order: ['YBUZ98', 'YCUZ98', 'YEUZ98']
    Para_list = ['YBUZ98', 'YCUZ98', 'YEUZ98']
    #multiprocessing pool
    cores = multiprocessing.cpu_count()

    for year in year_list:
        year_path = os.path.join(path2save, year)
        CheckDir(year_path)
        print('year folders exist!')
        url_year_list = getYear(url, year)
        for month_url in url_year_list:
            month_day_list = getMonth(month_url)
            for para in Para_list:
                para_folder_path = os.path.join(year_path, para)
                CheckDir(para_folder_path)
                print('para folder exists!')
                with mp.Pool(cores) as pool:
                    print("start multiprocessing...")
                    download_urls = pool.starmap(getParaFile, zip(repeat(para), month_day_list, repeat(para_folder_path)))
                print('print the results:')
                for res in download_urls:
                    print(res[0], res[1])
                
                # p_download = [mp.Process(target=Download, args=(download_urls[i][0], download_urls[i][1])) for i in range(len(download_urls[0]))]               
                # for p in p_download:
                #     p.start()
                # for p in p_download:
                #     p.join()
                        



    
