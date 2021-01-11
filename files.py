# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 20:51:02 2020

@author: e0306210
"""

import os

import glob
import time

folder = r'G:\RESSET'

os.chdir(folder)


def movefile(original_path, des_path):
    while not os.path.exists(original_path):
        time.sleep(3)
    if os.path.exists(des_path):
        os.remove(des_path)
    os.rename(original_path, des_path)


def createfolder(folder_path):
    directory = folder_path
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def file_no(path):
    files = glob.glob(path)
    return len(files)

default_download_path = r'C:\Users\e0306210\Downloads'
db_path = createfolder(folder + '\\Data\\DB') + '\\'