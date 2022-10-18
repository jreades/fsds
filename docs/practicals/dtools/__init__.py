import os
import csv
from urllib.request import urlopen
import numpy as np

def get_url(src, dest):
    
    # Check if dest does *not* exist -- that
    # would mean we had to download it!
    if not os.path.isfile(dest):
        print(f"{dest} not found, downloading!")
        
        # Get the data using the urlopen function
        response = urlopen(src) 
        filedata = response.read().decode('utf-8')
        
        # Extract the part of the dest(ination) that is *not*
        # the actual filename--have a look at how 
        # os.path.split works using `help(os.path.split)`
        path = list(os.path.split(dest)[:-1])
        
        # Create any missing directories in dest(ination) path
        # -- os.path.join is the reverse of split (as you saw above)
        # but it doesn't work with lists... so I had to google how 
        # to use the 'splat' operator! os.makedirs creates missing 
        # directories in a path automatically.
        if len(path) >= 1 and path[0] != '':
            os.makedirs(os.path.join(*path), exist_ok=True)
        
        with open(dest, 'w') as f:
            f.write(filedata)
            
    else:
        print(f"Found {dest} locally!")
    
    return dest

def read_csv(src:str) -> dict:
    """
    Converts a CSV file to a dictionary-of-lists (dol),
    using the first row to create column names.
    
    :param src: a local CSV file
    :returns: a dictionary-of-lists
    """
    csvdata = {} # An empty dictionary-of-lists
    
    with open(src, 'r') as f:
        csvr = csv.reader(f)
        
        # Read in our column names and
        # initialise the dictionary-of-lists
        csvcols = next(csvr) 
        for c in csvcols:
            csvdata[c] = []
        
        # Notice this code is still the same, 
        # we just used next(csvr) to get the 
        # header row first!
        for r in csvr: 
            # Although you can often assume that the order 
            # of the keys is the same, Python doesn't 
            # guarantee it; this way we will always make
            # the correct assignment.
            for idx, c in enumerate(csvcols):
                csvdata[c].append(r[idx])
    
    # Return dictionary of lists
    return csvdata

# Convert the raw data to data of the appropriate
# type: 'column data' (cdata) -> 'column type' (ctype)
def to_type(cdata, ctype):
    # If a string
    if isinstance(cdata, str):
        try:
            if ctype==bool:
                return cdata==True
            else:
                return ctype(cdata)
        except TypeError:
            return cdata
    
    # Not a string (assume list)
    else: 
        fdata = []
        for c in cdata:
            try:
                if ctype==bool:
                    fdata.append( c=='True' )
                else:
                    fdata.append( ctype(c) )
            except:
                fdata.append( c )
        return fdata

def find_val(col:list, val:str):
    """
    
    """
    if val in dir(np) and callable(getattr(np, val)):
        func = getattr(np, val)
        if val in ['min','max']:
            return np.where(col==func(col))[0][0]
        else:
            return func(col)
    else:
        return np.nan
