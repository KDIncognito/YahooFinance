# -*- coding: utf-8 -*-
"""
Created on Fri May 17 18:46:54 2019
 
@author: skd
"""
import json
import pandas as pd
from yahoofinancials import YahooFinancials
from pandas.io.json import json_normalize
 
stmnt_typ='income'
 
yahoo_financials=YahooFinancials('PCAR')
jsons= yahoo_financials.get_financial_stmts('annual','stmnt_typ')
 
json_ids= []
frames = []
 
for json_id, d in jsons.items():
    json_ids.append(json_id)
    frames.append(pd.DataFrame.from_dict(d, orient='index'))
 
#try
def flatten_json(b, delim):
    val = {}
    for i in b.keys():
        if isinstance(b[i], dict):
            get = flatten_json(b[i], delim)
            for j in get.keys():
                val[i.replace(':', '_') + delim + j.replace(':', '_')] = get[j]
        elif isinstance(b[i], list):
            c = 1
            for it in b[i]:
                if isinstance(it, dict):
                    get = flatten_json(it, delim)
                    for j in get.keys():
                        val[i.replace(':', '_') + delim + j.replace(':', '_') + delim + str(c)] = get[j]
                else:
                    val[i.replace(':', '_') + delim + str(c)] = it
                c += 1
        else:
            val[i.replace(':', '_')] = b[i]
    return val
 
flat_dict = flatten_json(jsons, '__')
 
flatData = pd.DataFrame.from_dict(flat_dict, orient='index')
flatData.reset_index(level=0, inplace=True)
flatData.columns = ['Name','nr']
 
names=flatData['Name'].str.split('__',expand=True)
 
temp0 = flatData['Name'].str.split(',', expand=True)
 
result = pd.concat([names,flatData['nr']], axis=1)
 
result.columns=['stmnt','cmpny','t_frm','itm','rpt','vls']
result_a= result.filter(regex='itm|vls|t_frm')
 
pafk= result_a.pivot_table(values='vls', columns='t_frm',index=['itm'],)