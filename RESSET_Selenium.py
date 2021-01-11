# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 11:36:38 2020

@author: Yulu Su

# reference 

for Selenium: https://selenium-python.readthedocs.io/getting-started.html
"""



''' 
generate the database information

'''

import RESSET_DB as db
import files

db_name = '2020DEC_subindustry' ### please change the database name
table_db = db.table_db(db_name)
table_db_table = db.table_db_table(db_name)
table_db_table_province = db.table_db_table_province(db_name)
table_db_table_province_city = db.table_db_table_province_city(db_name)
table_db_table_industry = db.table_db_table_industry(db_name)
table_db_table_subindustry = db.table_db_table_subindustry(db_name)


'''
Add scripts folder into the system path

'''


import sys
sys.path.append('./Scripts')



import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException



# please log in first
driver = webdriver.Chrome('./Scripts/chromedriver.exe')


driver.get("http://edp.resset.com") # open url of RESSET
driver.maximize_window() # maximize the window of Chrome


''' 
 please change chrome download default path!!!
 
'''



'''
Get the main-content 工商信息数据库',  '投融资数据库',  '企业信用数据库',  '企业资质数据库',  '司法文书数据库',  '知识产权数据库',
 '招投标数据库',  '标准数据库',  '成果奖励数据库',  '产品价格数据库',  '土地信息数据库',  '人才信息数据库',  '国家基金项目数据库',
 '上市信息数据库',  '招聘数据库'

'''

database_content = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "main-content"))
)

    
database_content = driver.find_element_by_id("main-content")

content_headers = database_content.get_attribute("innerText").split('\n') # get the database name like 企业信用数据库
content_url = [a.get_attribute('href') for a in database_content.find_elements_by_tag_name('a')] # get database url

content = [(content_headers[i], content_url[i],0) for i in range(len(content_headers))] # combine the database name and database url to a dict
table_db.func_write_bulk_table(data=content) # write the database name into table_db
undownloaded_db = table_db.func_check_download() # check whether database is not downloaded
dbbranch = {content_headers[i]: content_url[i] for i in range(len(content_headers))} 

for header in undownloaded_db:
    
    db_folder = files.createfolder( files.folder+ '\Data\\'+header[0]) + '\\' #create a folder for database like 企业信用数据库
   
    driver.get(dbbranch[header[0]]) # open database url in chrome like 企业信用数据库
    
    elem_submenu = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR , ".submenu"))
        ) # get the html of submenu like 工商信息， 股权出质， 工商变更， 股东结构， 主要人员， 分支机构， 对外投资， 动产抵押， 司法协助， 清算， 注销
    
    
    
    submenu_headers = elem_submenu.get_attribute("innerText").split('\n') 
    # get the name of the submenu like 工商信息， 股权出质， 工商变更， 股东结构， 主要人员， 分支机构， 对外投资， 动产抵押， 司法协助， 清算， 注销
    submenu_a = [a for a in elem_submenu.find_elements_by_tag_name('a')] 
    # get the url of the submenu like 工商信息， 股权出质， 工商变更， 股东结构， 主要人员， 分支机构， 对外投资， 动产抵押， 司法协助， 清算， 注销
    
    submenu = [ (header[0] + '_' + submenu_headers[i], header[0], submenu_headers[i], 0) for i in range(len(submenu_headers))] 
    # create bulk data for submenu
    table_db_table.func_write_bulk_table(data=submenu)
    # write the submenus bulk data into table_db_table
    undownloaded_table = table_db_table.func_check_download(header[0])
    # check the undownloaded submenu like 工商信息
    submenu = {submenu_headers[i]:submenu_a[i] for i in range(len(submenu_headers))}
    # generate a dict like {'工商信息'：url}
    
    for submenu_header in undownloaded_table:
        submenu[submenu_header[0]].click() # open the submenu like 工商信息   
        
        table_folder = files.createfolder(files.folder+'\Data\\'+header[0]+'\\'+submenu_header[0]) + '\\'
        
        province_tree = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID , "p-tree"))
            ) # get the html of province
                
        pronvice_headers = province_tree.get_attribute("innerText").split('\n') # get the option like 北京
        pronvice_a = [a for a in province_tree.find_elements_by_css_selector('.tree-branch')] # get the option link
        pronvice_a.pop(0) # pop up the first option since the first option is unclickable
        pronvice = [(header[0] + '_' + submenu_header[0] + '_' + pronvice_headers[i], 
                       header[0], 
                       submenu_header[0], 
                       pronvice_headers[i], 
                       0) for i in range(len(pronvice_headers))] # generate bulk data： table_db_table_province
        
        table_db_table_province.func_write_bulk_table(data=pronvice) # write bulk data into table_db_table_province
        undownloaded_province = table_db_table_province.func_check_download(header[0],submenu_header[0] ) # get the undownloaded province
        
        provincebranch = {pronvice_headers[i]: pronvice_a[i] for i in range(len(pronvice_headers))} # generate a dict like {'北京市': html_a}
        
        driver.execute_script("document.getElementById('p-tree').parentElement.scrollTop=0") # used to scroll down the tiny window province
        provincebranch[' 北京市'].click() #uncollapse the sub-list: province
        provincebranch[' 北京市'].find_elements_by_css_selector(".tree-label")[0].click() #collapse the province
        
        for province_leaf in undownloaded_province:
            
            n = pronvice_headers.index(province_leaf[0]) # used to scroll down the tiny window: province
            driver.execute_script("document.getElementById('p-tree').parentElement.scrollTop="+str(30*n) ) # used to scroll down the tiny window province
            time.sleep(1)
            # select province
            try:
                provincebranch[province_leaf[0]].click() #uncollapse the sub-list: province
            except ElementClickInterceptedException:
                time.sleep(3)
                provincebranch[province_leaf[0]].click() #uncollapse the sub-list: province
            time.sleep(1)
            
            city_a = provincebranch[province_leaf[0]].find_elements_by_css_selector(".tree-item") # get the html_a of province like 东城区
            city_headers = [city_leaf.get_attribute("innerText") for city_leaf in city_a] # get the option like 东城区
            
            city = [(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+'_'+city_headers[i], 
                           header[0], 
                           submenu_header[0], 
                           province_leaf[0], 
                           city_headers[i],
                           0) for i in range(len(city_headers))] # generate bulk data ： table_db_table_province_city
            
            table_db_table_province_city.func_write_bulk_table(data=city) # write bulk data into table_db_table_province_city
            undownloaded_city = table_db_table_province_city.func_check_download(header[0],submenu_header[0],province_leaf[0]) #undownloaded city list
            
            
            for city_leaf in undownloaded_city:
                if city_leaf[0] != ' 全部':
                    n_c = city_headers.index(city_leaf[0]) # get the city index to scroll down, otherwise the system will inform an interaction error
                    driver.execute_script("document.getElementById('p-tree').parentElement.scrollTop="+str(30*(n+n_c))) # used to scroll down the tiny window: province city
                    time.sleep(2)
                    try:
                        provincebranch[province_leaf[0]].find_elements_by_css_selector(".tree-item")[n_c].click() # select the city, like '西城区'
                    except ElementClickInterceptedException:
                        time.sleep(3)
                        provincebranch[province_leaf[0]].find_elements_by_css_selector(".tree-item")[n_c].click()# if encounter error, re-select the city, like '西城区'
                    time.sleep(1)
                    
                    
                    
                    industry_tree = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.ID , "i-tree"))
                    )
                    # get the html of industry
                    
                    industry_headers = industry_tree.get_attribute("innerText").split('\n') # get the option like 住宿餐饮业
                    industry_a = [a for a in industry_tree.find_elements_by_css_selector('.tree-branch')] # get the option link
                    industry_a.pop(0) # pop up the first option since the first option is unclickable
                    
                                     
                    industry = [(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+'_'+city_leaf[0] + '_' + industry_headers[i],
                       header[0], 
                       submenu_header[0], 
                       province_leaf[0], 
                       city_leaf[0],
                       industry_headers[i],      
                       0) for i in range(len(industry_headers))] # generate bulk data: industry
        
                    table_db_table_industry.func_write_bulk_table(data=industry) # write the bulk data into table_db_table_industry
                    undownloaded_industry = table_db_table_industry.func_check_download(header[0],submenu_header[0], province_leaf[0], city_leaf[0]) # undownloaded industry, like 住宿餐饮业
                    
                    industrybranch = {industry_headers[i]: industry_a[i] for i in range(len(industry_headers))} # a dict like {住宿餐饮业: html_a }
                    
                    driver.execute_script("document.getElementById('i-tree').parentElement.scrollTop=0") # used to scroll down the tiny window industry
                    industrybranch[' 农、林、牧、渔业'].click() # select the industry
                    industrybranch[' 农、林、牧、渔业'].find_elements_by_css_selector(".tree-label")[0].click()  #uncollapse the industry
                    
                    for industry_leaf in undownloaded_industry:
                
                        m = industry_headers.index(industry_leaf[0])  # used to scroll down the tiny window industry
                        driver.execute_script("document.getElementById('i-tree').parentElement.scrollTop="+str(30*m) ) # used to scroll down the tiny window industry
                        time.sleep(2)
                        try:
                            industrybranch[industry_leaf[0]].click() # select the industry
                        except ElementClickInterceptedException:
                            time.sleep(3)
                            industrybranch[industry_leaf[0]].click() # select the industry
                        except ElementNotInteractableException:
                            m = industry_headers.index(industry_leaf[0])  # used to scroll down the tiny window industry
                            driver.execute_script("document.getElementById('i-tree').parentElement.scrollTop="+str(30*m) ) # used to scroll down the tiny window industry
                            time.sleep(2)
                            industrybranch[industry_leaf[0]].click()
                        time.sleep(1)
                        
                        subindustry_a = industrybranch[industry_leaf[0]].find_elements_by_css_selector(".tree-item") # get the html of subindustry
                        subindustry_headers = [subindustry_leaf.get_attribute("innerText").replace('\t','').replace(' ','') for subindustry_leaf in subindustry_a] # [其他金融业]
                                   
                        subindustry = [(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+'_'+city_leaf[0] +'_'+industry_leaf[0]+'_'+subindustry_headers[i],
                                        header[0], 
                                        submenu_header[0], 
                                        province_leaf[0], 
                                        city_leaf[0],
                                        industry_leaf[0],
                                        subindustry_headers[i],
                                        0,
                                        0,
                                        0) for i in range(len(subindustry_headers))] # generate bulk data: subindustry
                        
                        table_db_table_subindustry.func_write_bulk_table(data=subindustry) # write the bulk data into table_db_table_subindustry
                        undownloaded_subindustry = table_db_table_subindustry.func_check_download(header[0],
                                                                                                  submenu_header[0], 
                                                                                                  province_leaf[0], 
                                                                                                  city_leaf[0], 
                                                                                                  industry_leaf[0]) # undownloaded subindustry
                                                
                        for subindustry_leaf in undownloaded_subindustry:
                            if subindustry_leaf[0] != '全部':
                                m_c = subindustry_headers.index(subindustry_leaf[0]) # get the index of the subindustry to scroll the window
                                driver.execute_script("document.getElementById('i-tree').parentElement.scrollTop="+str(30*(m+m_c) )) # used to scroll down the tiny window province
                                time.sleep(2)
                                
                                try:
                                    industrybranch[industry_leaf[0]].find_elements_by_css_selector(".tree-item")[m_c].click() # select subindustry
                                except ElementClickInterceptedException:
                                    error_link = True
                                    while error_link:
                                        time.sleep(3)
                                        try:
                                            industrybranch[industry_leaf[0]].find_elements_by_css_selector(".tree-item")[m_c].click() # encounter error, select subindustry
                                            error_link = False
                                        except:
                                            error_link = True
                                            
                                time.sleep(1)
                                
                                button_output = driver.find_element_by_id("export") # get the element of export button 
                                time.sleep(3)
                                try:
                                    button_output.click()   #click the export button 
                                except:
                                    error_button=True
                                    while error_button:                                            
                                        try:
                                            time.sleep(3)
                                            button_output = driver.find_element_by_id("export") # get the element of export button 
                                            time.sleep(3)
                                            button_output.click() # if error, re-click the export button 
                                            error_button=False
                                        except:
                                             error_button=True
                                time.sleep(3)
                                
                                # wait until the iframe appear and switch the driver to iframe
                                WebDriverWait(driver, 50).until(
                                        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe"))
                                    )
                                
                                # get the total page number in the iframe
                                searchtable_page_total = driver.find_element_by_css_selector(".pagination").get_attribute("innerText").split('\n')[-2] 
                                
                                if searchtable_page_total == '上一页':
                                    searchtable_page_total = 0 #if the name of the page before "下一页" is "上一页", the total pages is 0
                                
                                table_db_table_subindustry.func_update_download(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+ '_'+ city_leaf[0]+ '_' + industry_leaf[0] + '_' +subindustry_leaf[0], 
                                                                            searchtable_page_total, 0, 0) # update the subindustry: the total pages
                                detail_folder = files.createfolder(files.folder+'\Data\\'+header[0]+'\\'+submenu_header[0] + '\\' + province_leaf[0]) +'\\'
                                #create a folder: province to store the excel file
                                                                                       
                                cur_page = 1 # set the current page cursor is 1
                                if cur_page > 1 : # if the current page cursor is not 1, chrome will redirect to the current page
                                  for m in range(2, cur_page, 10):
                                    time.sleep(random.randint(60,120))
                                    driver.execute_script("javascript:gotoPage(" + str(m) +")")  # redirect to page m
                
                                
                                for i in range(cur_page, 1+int(searchtable_page_total)):             
                                    
                                    searchtable = WebDriverWait(driver, 20).until(
                                        EC.presence_of_element_located((By.ID , "a"))
                                    ) # get the html_a of iframe
                                    
                                    while True:
                                        time.sleep(10)
                                        filename = searchtable.find_element_by_id("fileName").get_attribute("innerText") # get the excel file name
                                        if filename[-6-len(str(i)):-6] == str(i): # if file name in tandem with the current page cursor, then break the loop and move to the next section
                                            break
                                        
                                        
                                    file_href = driver.find_element_by_xpath("//span[@id='fileName']/following-sibling::a") # get the url of the excel file
                                    time.sleep(3)
                                    file_href_path = file_href.get_attribute("href") # get the href of the excel file
                                    time.sleep(3)
                                    try:
                                        file_href.click() # click the href of the excel file to download the file to default downloaded folder
                                    except: #catch all kinds of errors
                                        error_excel = True
                                        while error_excel:
                                            try:
                                                time.sleep(3)
                                                file_href = driver.find_element_by_xpath("//span[@id='fileName']/following-sibling::a") # get the url of the excel file
                                                time.sleep(3)
                                                file_href_path = file_href.get_attribute("href") 
                                                time.sleep(3)
                                                file_href.click() # if error, click the href of the excel file to download the file to default downloaded folder
                                                error_excel = False
                                            except:
                                                error_excel = True # if error, click the href of the excel file to download the file to default downloaded folder
                                    time.sleep(3)
                                        
                                    
                                    try:
                                        files.movefile(files.folder+'\\'+filename, detail_folder+ header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+ '_' + city_leaf[0]+ '_' + industry_leaf[0] + '_' +subindustry_leaf[0]+ '_' + str(i) +'.xlsx')
                                        # move the excel file to the destination folder and rename the file
                                    except PermissionError:
                                        time.sleep(5)
                                        files.movefile(files.folder+'\\'+filename, detail_folder+ header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+ '_' + city_leaf[0]+ '_' + industry_leaf[0] + '_' +subindustry_leaf[0]+ '_' + str(i) +'.xlsx')
                                        # if error, move the excel file to the destination folder and rename the file
                                        
                                    if i < int(searchtable_page_total):
                                        if i% 50 == 0:
                                            time.sleep(random.randint(300,400))
                                        time.sleep(random.randint(40,100))
                                        driver.execute_script("javascript:gotoPage(" + str(i+1) +")") # to page i + 1
                                    
                                    table_db_table_subindustry.func_update_download(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+ '_'+ city_leaf[0]+ '_' + industry_leaf[0] + '_' +subindustry_leaf[0], 
                                                                            searchtable_page_total, i, 0)
                                    # update the table_db_table_subindustry: page number
                                
                                
                                table_db_table_subindustry.func_update_download(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+ '_'+ city_leaf[0]+ '_' + industry_leaf[0] + '_' +subindustry_leaf[0],
                                                                            searchtable_page_total, 1, 1)
                                # update the table_db_table_subindustry: downloaded already
                                
                                driver.switch_to.default_content() # switch from iframe to selection page
                                time.sleep(1)
                                try:
                                    close_elem = driver.find_element_by_css_selector(".layui-layer-close").click() # close the iframe
                                except ElementClickInterceptedException:
                                    time.sleep(2)
                                    close_elem = driver.find_element_by_css_selector(".layui-layer-close").click() # if error, close the iframe
                                    
                                try:
                                    industrybranch[industry_leaf[0]].find_elements_by_css_selector(".tree-item")[m_c].click() # cancel the selection of subindustry
                                except ElementClickInterceptedException:
                                    time.sleep(2)
                                    industrybranch[industry_leaf[0]].find_elements_by_css_selector(".tree-item")[m_c].click() # if error, cancel the selection of subindustry
                                time.sleep(1)
                        
                        table_db_table_industry.func_update_download(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+'_'+city_leaf[0]+'_'+industry_leaf[0], 1 )
                        # update the table_db_talbe_industry: downloaded already
                         
                        driver.execute_script("document.getElementById('i-tree').parentElement.scrollTop="+str(30*(m) ))  # scroll the tiny window: industry to uncollapse the selection of industry
                        time.sleep(2)
                        try:
                            industrybranch[industry_leaf[0]].find_elements_by_css_selector(".tree-label")[0].click()  #uncollapse the industry
                        except ElementClickInterceptedException:
                            time.sleep(3)
                            industrybranch[industry_leaf[0]].find_elements_by_css_selector(".tree-label")[0].click()  #if error, uncollapse the industry
                        time.sleep(1)
                            
                    table_db_table_province_city.func_update_download(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0]+'_'+city_leaf[0], 1 )
                    # update the table_db_table_province_city: downloaded already
                    
                    try:
                        provincebranch[province_leaf[0]].find_elements_by_css_selector(".tree-item")[n_c].click() # cancel the selection of city
                    except ElementClickInterceptedException:
                        time.sleep(3)
                        provincebranch[province_leaf[0]].find_elements_by_css_selector(".tree-item")[n_c].click() # if error, cancel the selection of city
                    time.sleep(1)
            
            driver.execute_script("document.getElementById('p-tree').parentElement.scrollTop="+str(30*n) ) # used to scroll down the tiny window: province to uncollapse the province selction 
            time.sleep(1)   
            try:
                provincebranch[province_leaf[0]].find_elements_by_css_selector(".tree-label")[0].click() #collapse the province
            except ElementClickInterceptedException:
                time.sleep(3)
                provincebranch[province_leaf[0]].find_elements_by_css_selector(".tree-label")[0].click() #if error, collapse the province
            time.sleep(1)
            
            table_db_table_province.func_update_download(header[0] + '_' + submenu_header[0] + '_' + province_leaf[0], 1 ) # update table_db_table_province: downloaded already
            
            province_tree = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID , "p-tree"))
                ) # re-get the html of the province
            
            pronvice_headers = province_tree.get_attribute("innerText").split('\n') # get the option like 北京
            pronvice_a = [a for a in province_tree.find_elements_by_css_selector('.tree-branch')] # get the option link
            pronvice_a.pop(0) # pop up the first option since the first option is unclickable
            undownloaded_province = table_db_table_province.func_check_download(header[0],submenu_header[0] ) # check which province is not downloaded
            
            provincebranch = {pronvice_headers[i]: pronvice_a[i] for i in range(len(pronvice_headers))} # generate a dict {北京:url_a}
            
        table_db_table.func_update_download(header[0] + '_' + submenu_header[0], 1) # update table_db_table: downloaded already

    table_db_table.func_update_download(header[0], 1) # update table_db: downloaded already