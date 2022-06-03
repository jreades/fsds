#!/usr/bin/env python
# coding: utf-8

from urllib.request import urlopen
import csv
import os

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
    
    with open(dest, 'r') as f:
        return f.read().splitlines()

# Notice that it doesn't make sense to use `dest` as the 
# parameter name here because we always read *from* a data
# source. Your names can be whatever you want, but they 
# should be logical wherever possible!
def to_lol(lst):
    
    # Rest of code to read file and convert it goes here
    csvdata = []
    
    # This is the same code that you used last week, but 
    # you'll have to rename some vars to get things to
    # work for you here.
    csvfile  = csv.reader(lst)
    for row in csvfile:              
        csvdata.append( row )
    
    # Return list of lists
    return csvdata

def to_dol(lol):
    """
    Converts a list-of-lists (LoL) to a dict-of-lists (dol)
    using the first element in the LoL to create column names.
    
    :param lol: a list-of-lists where each element of the list represents a row of data
    :returns: a dict-of-lists
    """
    # Create empty dict-of-lists
    ds = {}

    # I had a version of this code that used
    # lol.pop(0) since it made the for loop
    # easier to read. But I changed my mind...
    #
    # Can you think why?
    col_names = lol[0]
    for c in col_names:
        ds[c] = []

    # Then values into a list attached to each key
    for row in lol[1:]:
        for c in range(0,len(col_names)):
            ds[ col_names[c] ].append( row[c] )
            
    return ds

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


    