import requests
import json
import time

CACHE_FILE_NAME ='final_project_try.json'

## BASE CACHE AND URL SETTING
def load_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILE_NAME,'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache):
    ''' Saves the current movie of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an request by its baseurl and params

    Parameters
    ----------
    baseurl: string
        The URL for the movie website
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    if params:
        unique_string = []
        connector ="_"
        for key in params.keys():
            unique_string.append(f"{key}_{params[key]}")
        unique_string.sort()
        unique_key = baseurl + connector + connector.join(unique_string)
    else:
        unique_key = baseurl
    return unique_key


## RUQUEST DATA FROM URL AND API ENDPOINT
def make_url_request_using_cache(url, cache, params):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    url: string
        The URL for the website
    cache: dict
        The dictionary to save
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
    '''
    unique_key = construct_unique_key(url,params)

    if (unique_key in cache.keys()):
        print("Using cache")
        return cache[unique_key]
    else:
        print("Fetching")
        time.sleep(1)
        cache[unique_key] = requests.get(url,params).text
        save_cache(cache)
        return cache[unique_key]

def make_url_request_using_cache_API(url,cache,params):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    url: string
        The URL for the API endpoint
    cache: dict
        The dictionary to save
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
    '''
    unique_key=construct_unique_key(url,params)
    if (unique_key in cache.keys()):
        print("Using cache")
        return cache[unique_key]
    else:
        print("Fetching")
        time.sleep(1)
        cache[unique_key] = requests.get(url,params).json()
        save_cache(cache)
        return cache[unique_key]