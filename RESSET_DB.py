# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 20:33:02 2020

@author: e0306210
"""

import sqlite3
import files as Files

class database:
    def __init__(self, db):
        self.db = db
        self.tables = []
        self.conn = sqlite3.connect(Files.db_path + self.db + '.db')
        self.conn.close() 
        
    def get_table(self, name):        
        return table(self.db, name)        

'''///////////////////////////////////////////////////////////////////
'''

class table:
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.fields=[]
        self.types = []
        self.primary_key = []
        self.foreign_key = ''
        
    
    def string_fields(self):
        return ','.join(self.fields)
    
    def string_fields_types(self):
        return ','.join([field + ' ' + fieldtype + ' primary key'   if field in self.primary_key else field + ' ' + fieldtype for field, fieldtype in zip(self.fields, self.types)])
    
    def string_qmarks(self):
        return ','.join(['?']*len(self.fields))
    
    def add_foreign_key(self, flds, tbs, tbs_flds):
        '''please use it before create_table'''
        self.foreign_key = ','.join([' FOREIGN KEY (' + fld + ') REFERENCES table_' + tb + ' (' + tbs_fld + ')' for fld, tb, tbs_fld in zip(flds, tbs, tbs_flds)])
        return self.foreign_key
   
    def sql_create_table(self):
        sql = 'create table if not exists table_' + self.name + ' (' +  self.string_fields_types() + self.foreign_key +  ')'
        return sql
     
    def sql_insert_table(self):
        sql = 'insert into table_' + self.name + ' (' +  self.string_fields() + ')values (' + self.string_qmarks() +')'
        return sql

    def sql_drop_table(self):
        sql = 'DROP table if exists table_' + self.name
        return sql
    
    def exe_sql(self, sql, **kwargs):
        conn = sqlite3.connect(Files.db_path + self.db + '.db')
        cursor = conn.cursor()
        if len(kwargs) == 0:
            cursor.execute(sql)
        else:
            if 'data' in kwargs:
                try:
                    cursor.execute(sql, (kwargs['data']))   #insert data
                except sqlite3.IntegrityError:
                    pass
        cursor.close()
        conn.commit()
        conn.close() 

    def exe_sql_w_return(self, sql, **kwargs):
        conn = sqlite3.connect(Files.db_path + self.db + '.db')
        cursor = conn.cursor()
        if len(kwargs) == 0:
            cursor.execute(sql)
        else:
            if 'data' in kwargs:
                try:
                    cursor.execute(sql, (kwargs['data']))   #insert data
                except sqlite3.IntegrityError:
                    pass
        res =cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close() 
        return res

    def func_write_table(self, data):        
        self.exe_sql(self.sql_create_table())
        self.exe_sql(self.sql_insert_table(), data=data)
    
    def func_write_bulk_table(self, data):        
        self.exe_sql(self.sql_create_table())
        conn = sqlite3.connect(Files.db_path + self.db + '.db')
        cursor = conn.cursor()
        try:
            cursor.executemany(self.sql_insert_table(), data)   #insert data
        except sqlite3.IntegrityError:
            pass
        cursor.close()
        conn.commit()
        conn.close() 
        
    def func_count_by_and(self, vares, var_operators, var_values): 
        condition = ' and '.join([var+' '+ var_operator +" '"+  var_value+ "' " for var, var_operator, var_value in zip(vares, var_operators, var_values)  ])
        sql = 'select count(*) from table_' + self.name + ' where ' +  condition
        counts = self.exe_sql_w_return(sql)
        return counts[0][0]
    
    def func_count_by_or(self, vares, var_operators, var_values): 
        condition = ' or '.join([var+' '+ var_operator +" '"+  var_value+ "' " for var, var_operator, var_value in zip(vares, var_operators, var_values)  ])
        sql = 'select count(*) from table_' + self.name + ' where ' +  condition
        counts = self.exe_sql_w_return(sql)
        return counts[0][0]
    
    #def func_check_w_table(self, other_table):
        
class table_db(table):
    def __init__(self, db):
        super(table_db,self).__init__(db,'db')
        self.fields = ['var_name',   ##
                       'var_url',   ##
                       'var_check']   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['var_name']
        self.exe_sql(self.sql_create_table())


    def func_check_download(self):
        sql = 'select var_name from table_db where var_check is 0'
        return self.exe_sql_w_return(sql)
    
    def func_update_download(self, varid,  check):
       sql = 'update table_db set  var_check = ? where var_name = ?'
       return self.exe_sql_w_return(sql, data = (check, varid))

class table_db_table(table):
    def __init__(self, db):
        super(table_db_table,self).__init__(db,'db_table')
        self.fields = ['var_id',   ##
                       'var_db',
                       'var_table',   ##
                       'var_check']   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['var_id']
        self.exe_sql(self.sql_create_table())


    def func_check_download(self, db):
        sql = 'select var_table from table_db_table where var_check is 0 and var_db = ?'
        return self.exe_sql_w_return(sql, data=(db,))
   
    def func_update_download(self, varid,  check):
       sql = 'update table_db_table set  var_check = ? where var_id = ?'
       return self.exe_sql_w_return(sql, data = (check, varid))


class table_db_table_province(table):
    def __init__(self, db):
        super(table_db_table_province,self).__init__(db,'db_table_province')
        self.fields = ['var_id',   ##
                       'var_db',
                       'var_table',   ##
                       'var_province',
                       'var_check']   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['var_id']
        self.exe_sql(self.sql_create_table())


    def func_check_download(self, db, table):
        sql = 'select var_province from table_db_table_province where var_check is 0 and var_db = ? and var_table=?'
        return self.exe_sql_w_return(sql, data=(db,table))
    
    def func_update_download(self, varid,  check):
        sql = 'update table_db_table_province set  var_check = ? where var_id = ?'
        return self.exe_sql_w_return(sql, data = (check, varid))


class table_db_table_province_city(table):
    def __init__(self, db):
        super(table_db_table_province_city,self).__init__(db,'db_table_province_city')
        self.fields = ['var_id',   ##
                       'var_db',
                       'var_table',   ##
                       'var_province',
                       'var_city',
                       'var_check']   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['var_id']
        self.exe_sql(self.sql_create_table())


    def func_check_download(self, db, table, province):
        sql = 'select var_city from table_db_table_province_city where var_check is 0 and var_db = ? and var_table=? and var_province = ?'
        return self.exe_sql_w_return(sql, data=(db,table, province))
    
    def func_update_download(self, varid,  check):
        sql = 'update table_db_table_province_city set  var_check = ? where var_id = ?'
        return self.exe_sql_w_return(sql, data = (check, varid))

    
class table_db_table_industry(table):
    def __init__(self, db):
        super(table_db_table_industry,self).__init__(db,'db_table_industry')
        self.fields = ['var_id',   ##
                       'var_db',
                       'var_table',   ##
                       'var_province',
                       'var_city',
                       'var_industry',
                       'var_check']   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['var_id']
        self.exe_sql(self.sql_create_table())


    def func_check_download(self, db, table, province, city):
        sql = 'select var_industry from table_db_table_industry where var_check is 0 and var_db = ? and var_table=? and var_province = ? and var_city = ?'
        return self.exe_sql_w_return(sql, data=(db,table, province, city))
    
    def func_update_download(self, varid, check):
        sql = 'update table_db_table_industry set var_check = ? where var_id = ?'
        return self.exe_sql_w_return(sql, data = ( check, varid))
    
    
class table_db_table_subindustry(table):
    def __init__(self, db):
        super(table_db_table_subindustry,self).__init__(db,'db_table_subindustry')
        self.fields = ['var_id',   ##
                       'var_db',
                       'var_table',   ##
                       'var_province',
                       'var_city',
                       'var_industry',
                       'var_subindustry',
                       'var_number',
                       'var_act_number',
                       'var_check']   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['var_id']
        self.exe_sql(self.sql_create_table())


    def func_check_download(self, db, table, province, city, industry):
        sql = 'select var_subindustry from table_db_table_subindustry where var_check is 0 and var_db = ? and var_table=? and var_province = ? and var_city = ? and var_industry = ?'
        return self.exe_sql_w_return(sql, data=(db,table, province, city, industry))
    
    def func_update_download(self, varid, total_page, page, check):
        sql = 'update table_db_table_subindustry set var_number = ? , var_act_number = ?, var_check = ? where var_id = ?'
        return self.exe_sql_w_return(sql, data = (total_page, page, check, varid))