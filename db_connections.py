import pyodbc
import pandas as pd

CONN_LOCAL = {'Server':r'localhost\SQLEXPRESS','Driver':'{SQL Server}','Database':'trd_db','Trusted_Connection':'yes'}

def conn_string(connection_dict):
    connection_string = ''

    for key in connection_dict:
        substr = key + '=' + connection_dict[key] + ';'
        connection_string += substr
    return connection_string

def get_db_meta(cursor,attr='table_name',lim=-1):

    tbl_dict = {'table_name':[],'table_schem':[],'table_cat':[],'table_type':[]}

    if attr == 'all':
        for key in tbl_dict:
            tbl_dict[key] = get_db_meta(cursor,attr=key,lim=lim)
        return tbl_dict

    else:
        for idx,row in enumerate(cursor.tables()):
            if idx == lim:
                break
            else:
                tbl_dict[attr].append(getattr(row,attr))
        return tbl_dict[attr]

def get_col_meta(cursor,tbl_name,attr='column_name',lim=-1):

    col_dict = {'table_cat':[],'table_schem':[],'table_name':[],'column_name':[],
                'data_type':[],'type_name':[],'column_size':[],'buffer_length':[],
                'decimal_digits':[],'num_prec_radix':[],'nullable':[],'remarks':[],
                'column_def':[],'sql_data_type':[],'sql_datetime_sub':[],
                'char_octet_length':[],'ordinal_position':[],'is_nullable':[]}
    
    if attr == 'all':
        for key in col_dict:
            col_dict[key] = get_col_meta(cursor,tbl_name,attr=key,lim=lim)
        return col_dict

    elif isinstance(attr,list):
        for atr in attr:
            for idx,row in enumerate(cursor.columns(table=tbl_name)):
                if idx == lim:
                    break
                else:
                    col_dict[atr].append(getattr(row,atr))
        return col_dict[attr] # uncorrect because list is not hashable

    else:
        for idx,row in enumerate(cursor.columns(table=tbl_name)):
            if idx == lim:
                break
            else:
                col_dict[attr].append(getattr(row,attr))
        return col_dict[attr]

def get_structure(cursor,lim=[-1,-1]): #get all DB metadata

    struct = dict()
    struct['db_meta'] = get_db_meta(cursor,attr='all',lim=lim[0])

    for tbl_name in struct['db_meta']['table_name']:
        struct[tbl_name] = get_col_meta(cursor,tbl_name,attr='all',lim=lim[1])

    return struct
