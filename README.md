####(work in progress)
Yahoo Finance or YF as I call it (Python yahoofinancials api), does not need a user specific API key. It works well in extracting historical data from YF. There are instructions and blogs on how to retrieve data from YF API already, but information on how to convert that data to a pd table could be a bit tricky for beginners like myself. This is my attempt to put together the data extraction part and the tabulation piece. Hope you find it useful!

## Data extraction from the API
This article on [pypi](https://pypi.org/project/yahoofinancials/) gives a good list of commands that come with the API. Output is in the form of a json file.
###Code sample:
```
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
```
## Function to flatten a json file
I referenced this article ... (to be continued)

 
