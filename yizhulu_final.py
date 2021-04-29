#################################
##### Name: Yizhu Lu        #####
##### Uniqname:   yizhulu   #####
#################################


## IMPORT REQUIRED PACKAGES
from bs4 import BeautifulSoup
import requests
import json
import time
import sqlite3
import plotly
import plotly.graph_objects as go

import cache as ca
import plot as pl



## BASE CACHE AND URL SETTING
BASE_URL='https://www.imdb.com'
CACHE_DICT = {}

## WEB SCRAPING AND SCRAWLING FROM MULTIPLE PAGES
class Movie:
    '''a movie object

    every movie attributes
    ----------------------
    Title: string
        name of the movie(e.g.'The Godfather')

    Rating: float
        rating of a movie(e.g. 9.2)
    
    Year: integer
        year of the movie(e.g. 1972)

    Gerne: string
        gerne of the movie(e.g. 'Crime/Drama')

    Boxoffice: integer
        cumulative worldwide gross box office($) (e.g. 246,120,986)

    Taglines: string
        one sentence to introduce the movie(e.g. 'An offer you can't refuse.')

    '''
    def __init__(self,title,rating,year,gerne,boxoffice,taglines):
        self.title=title
        self.rating=rating
        self.year=year
        self.gerne=gerne
        self.boxoffice=boxoffice
        self.taglines=taglines
    
    def basic_info(self):
        return self.title+"("+f'{self.year}'+"): "+ self.gerne + "   Rating: "+ f'{self.rating}'

    def detail_info(self):
        detailinfo= "Title: "+ self.title+"\n"+"Year: "+f'{self.year}'+"\n"+"Rating: "+f'{self.rating}'+"\n"+"Gerne: "+self.gerne+"\n"+"Taglines: "+self.taglines+"\n"+"Boxoffice($): "+f'{self.boxoffice}'+"\n"
        return detailinfo

def build_chart_url_dict():
    ''' Build a dictionary of different charts and its url from 
        IMDb website: https://www.imdb.com/chart/top

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a chart name and value is the url of chart
        e.g.{"box_office":'https://www.imdb.com/chart/boxoffice'}
    
    '''
    chart_url=BASE_URL+'/chart/top'
    response=ca.make_url_request_using_cache(chart_url,CACHE_DICT,params=None)
    soup = BeautifulSoup(response,"html.parser")
    charts = soup.find("div", class_="full-table")
    each_chart = charts.find_all("div", class_="table-cell primary")
    chart_dict={}

    for i in each_chart:
        chart_path = i.find("a").text
        chart_url=i.find("a")["href"]
        chart_dict[chart_path.strip().lower()]=BASE_URL+chart_url

    chart_dict.pop('most popular tv')
    chart_dict.pop('top rated tv')
    return chart_dict

def get_movie_instance(movie_url):
    ''' Make an instance from a movie URL.

    Parameters
    ----------
    movie_url:string
        The URL for a movie page in movie chart

    Returns
    -------
    instance
        a movie instance(title,rating,year,gerne,boxoffice,taglines)
    '''

    blank_space=" "
    response = ca.make_url_request_using_cache(movie_url,CACHE_DICT,params=None)
    soup=BeautifulSoup(response,'html.parser')


    try:
        title_wrapper=soup.find('div', class_='title_wrapper')
        title_year_info=title_wrapper.find('h1')
        movie_title=(title_year_info.text)[:-7].strip()
    except:
        movie_title='no title'

    try:
        title_wrapper=soup.find('div', class_='title_wrapper')
        title_year_info=title_wrapper.find('h1')
        movie_year=int(title_year_info.find('a').text)
    except:
        movie_year='no year'

    try:
        movie_rating=float(soup.find('span',itemprop='ratingValue').text)
    except:
        movie_rating='no rating'

    try:
        storyline=soup.find('div',class_='article', id='titleStoryLine')
        text_info=storyline.find_all('div', class_='txt-block')
        for i in text_info:
            text_word_list=i.text.split()
            if text_word_list[0]=='Taglines:':
                movie_taglines=text_word_list[1:]
        movie_taglines=blank_space.join(movie_taglines).strip()
    except:
        movie_taglines='no taglines'

    try:
        storyline=soup.find('div',class_='article', id='titleStoryLine')
        text_info2=storyline.find_all('div',class_='see-more inline canwrap')
        for i in text_info2:
            text_word_list2=i.text.split()
            if text_word_list2[0]=='Genres:':
                movie_gerne=text_word_list2[1:]
        movie_gerne=blank_space.join(movie_gerne).strip()
    except:
        movie_gerne='no gerne'
    try:
        titledetail=soup.find('div', class_='article', id='titleDetails')
        detail_info=titledetail.find_all('div', class_='txt-block')
        for i in detail_info:
            detail_word_list=i.text.split()
            if detail_word_list[0]=='Cumulative':
                movie_boxoffice=(detail_word_list)[-1]
        remove_char=['$',","]
        for i in remove_char:
            movie_boxoffice=movie_boxoffice.replace(i,'')
        movie_boxoffice=int(movie_boxoffice)
    except:
        movie_boxoffice='no boxoffice'

    movie_object=Movie(movie_title,movie_rating,movie_year,movie_gerne,movie_boxoffice,movie_taglines)
    return movie_object

def get_movies_list_for_chart(chart_url):
    '''Make a list of movie instances from a chart URL.

    Parameters
    ----------
    chart_url:string
        The URL for chart page

    Returns
    -------
    list
        a list of movie instances
    '''
    response= ca.make_url_request_using_cache(chart_url,CACHE_DICT,params=None)
    soup=BeautifulSoup(response,'html.parser')
    movie_list= soup.find('tbody')
    all_movie=movie_list.find_all('td', class_='titleColumn',limit=100)

    movie_object_list=[]
    for i in all_movie:
        movie_url=i.find('a')['href']
        movie_url=BASE_URL+movie_url
        movie_object_list.append(get_movie_instance(movie_url))
        
    return movie_object_list

## ACCESS DATA FROM WIKIPEDIA API
def get_movie_wikipedia(movie_object):
    '''Obtain API data from Wikipedia API.
    
    Parameters
    ----------
    movie_object: object
        an instance of a movie
    
    Returns
    -------
    tuple
        summary of movie Wikipedia, url of movie Wikipedia
    '''
    base_url='https://en.wikipedia.org/w/api.php'
    params={
        'format':'json',
        'action':'query',
        'titles':movie_object.title,
        'prop': 'extracts|info',
        'inprop':'url',
        'exintro':1,
        'explaintext':1,
        'indexpageids':1
    }
    API_response=ca.make_url_request_using_cache_API(base_url,CACHE_DICT,params)
    movie_page_info=API_response['query']['pages']
    wikimdedia_pageid=API_response['query']['pageids'][0]
    movie_summary=movie_page_info[wikimdedia_pageid]['extract']
    movie_url=movie_page_info[wikimdedia_pageid]['fullurl']
    return movie_summary,movie_url

def print_movie_details(movie_object):
    ''' Use the print_movie_details function to get movie details,
        return them in title + year + rating + gerne + taglines + boxoffice + url + summary
    
    Parameters
    ----------
    movie_object: object
        an instance of a movie
    
    Returns
    -------
    string
        string of movie details
    '''
    basic_info=movie_object.detail_info()
    summary,url=get_movie_wikipedia(movie_object)
    movie_summary='Summary: '+ summary
    movie_url='URL:' + url
    return basic_info+movie_url+"\n"*2+movie_summary


if __name__ == "__main__":

    CACHE_DICT = ca.load_cache()

    input_str1="Enter movie chart index you are interested in or \"exit\" to quit: "
    input_str2="Enter what you are interested in: movie index for movie detail search or enter chart detail(e.g. year, boxoffice, rating) or \"exit\" or \"back\": "


    print('Here are six movie charts for selection: ')
    print("-"*len(input_str1))
    number=0
    for i in build_chart_url_dict():
        number+=1
        print("["+ f"{number}" +"] "+i)
    print("-"*len(input_str1))

    response = input(input_str1)
    while(response.strip().lower()!='exit'):
        #response= response.strip().lower()
        chart_dict=build_chart_url_dict()
        
        try:
            key=list(chart_dict.keys())[int(response)-1]
            chart_url= chart_dict[key]
            chart_name=key
            movie_object_list= get_movies_list_for_chart(chart_url)
            movie_list_title= "List of movies in ["+chart_name+"] :"
            print("-"*len(movie_list_title))
            print(movie_list_title)
            print("-"*len(movie_list_title))

            for i in range(len(movie_object_list)):
                print ("["+ f"{i+1}" +"] "+ (movie_object_list[i]).basic_info())
            print("-"*len(input_str2))

            response=input(input_str2)
            while(response.lower() !='exit' and response.lower() !='back' ):
                if response.isnumeric()==True:
                    if (int(response)-1) in range(len(movie_object_list)):
                        movie_object=movie_object_list[int(response)-1]
                        movie_detail=print_movie_details(movie_object)
                        movie_title= "Details of ["+ str(movie_object.title)+"] :"
                        radar_chart_title='Distribution of rating, year and boxoffice in radar chart:'
                        print("-"*len(movie_title))
                        print(movie_title)
                        print("-"*len(movie_title))
                        print(movie_detail+'\n')
                        #print("-"*len(radar_chart_title))
                        print(radar_chart_title)
                        pl.radar_chart_for_movie(movie_object)
                    else:
                        print("[Error] Invalid input")
                        print("-"*len(input_str2))
                else:
                    if response.strip().lower()=='year':
                        year_chart_title='Year distribution plot for ['+chart_name+"] :"
                        print("-"*len(year_chart_title))
                        print(year_chart_title)
                        pl.make_year_rating_boxoffice_chart('year',chart_name)
                    elif response.strip().lower()=='boxoffice':
                        boxoffice_chart_title='Boxoffice distribution plot for ['+chart_name+"] :"
                        print("-"*len(boxoffice_chart_title))
                        print(boxoffice_chart_title)
                        pl.make_year_rating_boxoffice_chart('boxoffice',chart_name)
                    elif response.strip().lower()=='rating':
                        rating_chart_title='Rating distribution plot for ['+chart_name+"] :"
                        print("-"*len(rating_chart_title))
                        print(rating_chart_title)
                        pl.make_year_rating_boxoffice_chart('rating',chart_name)
                    else:
                        print("[Error] Invalid input")
                        print("-"*len(input_str2))
                response=input(input_str2)

            if response.strip().lower() == 'back':
                print('Here are six movie charts for selection: ')
                print("-"*len(input_str1))
                number=0
                for i in build_chart_url_dict():
                    number+=1
                    print("["+ f"{number}" +"] "+i)
                print("-"*len(input_str1))
                response=input(input_str1)
                print("-"*len(input_str1))
                continue
            elif response.strip().lower()=='exit':
                continue

        except:
            print("[Error] Enter proper movie chart name")
            print('Here are six movie charts for selection: ')
            print("-"*len(input_str1))
            number=0
            for i in build_chart_url_dict():
                number+=1
                print("["+ f"{number}" +"] "+i)
            print("-"*len(input_str1))
            response = input(input_str1)
            continue