Python *yahoofinancials* api, does not need a user specific API key. It works well in extracting historical data from YF. There are instructions and blogs on how to retrieve data from YF API already, but information on how to convert that data to a pd table could be a bit tricky for beginners like myself. This is my attempt to put together the data extraction part and the tabulation piece. Hope you find it useful!

## Data extraction from the API
This article on [pypi](https://pypi.org/project/yahoofinancials/) gives a good list of commands that come with the API. Output is in the form of a json file.
###Code sample:
```
import pandas as pd
from yahoofinancials import YahooFinancials
from pandas.io.json import json_normalize

yahoo_financials=YahooFinancials('PCAR')
jsons= yahoo_financials.get_financial_stmts('annual','income')
json_ids= []
frames = []

for json_id, d in jsons.items():
    json_ids.append(json_id)
    frames.append(pd.DataFrame.from_dict(d, orient='index'))
```
## Function to flatten a json file
It was a little difficult figuring out how to extract data from a json file to a pandas format. This [problem on stack overflow](https://stackoverflow.com/questions/51635872/yahoofinancials-writing-multidimensional-dictionary-to-csv/51678333) was very helpful in flattening the json file.

````
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
````
Now, the flattened file needs to be laid out by year for all the items.

````
flatData = pd.DataFrame.from_dict(flat_dict, orient='index')
flatData.reset_index(level=0, inplace=True)
flatData.columns = ['Name','nr']
names=flatData['Name'].str.split('__',expand=True)
temp0 = flatData['Name'].str.split(',', expand=True)
result = pd.concat([names,flatData['nr']], axis=1)
result.columns=['stmnt','cmpny','t_frm','itm','rpt','vls']
result_a= result.filter(regex='itm|vls|t_frm')
pafk= result_a.pivot_table(values='vls', columns='t_frm',index=['itm'],)
````
Now the object ```` pafk ```` has data in a table you could export to an excel format

#### Please let me know if you find any problems with this version. I will do my best to help you out. Good luck!

 
