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
import logging

def initFile(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        # os.mknod requires root
        #os.mknod(file_path)
    open(file_path, 'a').close()

def CheckDir(dir_path):
    if not os.path.isdir(dir_path):
        logger.debug("{} not exists!".format(dir_path))
    else:
        logger.info("{} exists!".format(dir_path))

def getYear(url, year):
    content = urlopen(url).read()
    soup = BeautifulSoup(content, features="lxml")
    #help with the urls
    url_list = []
    for j in soup.findAll('a'):
        if j['href'][:4] == year:
            url_path = url + j['href']
            url_list.append(url_path)
    logger.info("get the month urls of year {}!".format(year))
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
    logger.info("get the day urls of folder {}!".format(url))
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
            if not os.path.isfile(file_path_name):
                file_url_list.append(file_url)
                file_path_name_list.append(file_path_name_list)
            else: 
                logger.debug('file {} already exists.'.format(j['href']))
    return file_url_list, file_path_name_list

def download(file_url, file_path_name):
    logger.info("start download day files {}".format(url[-9:]))
    start_time = time.time()
    downloadfile = URLopener()
    downloadfile.retrieve(file_url, file_path_name)
    logger.info('file {} is downloaded:)'.format(j['href']))
    end_time = time.time()
    time.sleep(1)
    logger.info('it takes {:.2f} min to download this files.'.format((end_time-start_time)/60))   
    logger.info('move on to another file!') 

def update(*a):
    return pbar.update()

if __name__ == '__main__':
    logfile_path = '/pfs/work6/workspace/scratch/ov0392-CONUS2.5-0/Download_2.5km_folder_muster_umfolder/CONUS_2.5_Download_v2.log'
    initFile(logfile_path)
    logging_level = logging.INFO
    logger = logging.getLogger('conus_2.5 Download test')
    logger.setLevel(logging_level)
    fh = logging.FileHandler(logfile_path)
    fh.setLevel(logging_level)
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info('get ready!')

    #path2save = Path('/Volumes/Elements/Download_2.5km_folder_muster_umfolder/')
    path2save = Path('/pfs/work6/workspace/scratch/ov0392-CONUS2.5-0/Download_2.5km_folder_muster_umfolder/')
    CheckDir(path2save)
    url = "https://nomads.ncdc.noaa.gov/data/ndfd/"
    #give the wanted year data
    year_list = ['2015']
    #seperate run because the low speed. in order: ['YBUZ98', 'YCUZ98', 'YEUZ98']
    Para_list = ['YBUZ98', 'YCUZ98', 'YEUZ98']
    #multiprocessing pool
    cores = multiprocessing.cpu_count()
    try:
        for year in year_list:
            year_path = os.path.join(path2save, year)
            CheckDir(year_path)
            logger.info('year folders exist!')
            url_year_list = getYear(url, year)
            for para in Para_list:
                para_folder_path = os.path.join(year_path, para)
                CheckDir(para_folder_path)
                logger.info('para folder exists!')
                logger.info('start with para {}.'.format(para))
                for month_url in url_year_list:
                    month_day_list = getMonth(month_url)
                    for day_url in month_day_list:
                        file_url_list, file_path_name_list = getParaFile(para, day_url, para_folder_path)
                        logger.info("start multiprocessing...")
                        pbar = tadm(total = len(file_url_list))
                        for i in range(len(file_url_list)):
                            mp.Pool(cores).starmap_async(download, zip(file_url_list, file_path_name_list), callback=update) 
    except:
        logger.debug("show what happening...")
        break
                
                



    
