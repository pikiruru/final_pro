import sqlite3
import yizhulu_final as final

## Create table in SQL
conn=sqlite3.connect('Movie.sqlite')
cur=conn.cursor()
drop_movie='''
    drop table if exists 'movie_chart';
'''
create_movie='''
    create table if not exists'movie_chart'(
        'id_number' integer primary key autoincrement unique,
        "chart_name" text not null,
        "maximum_number" integer not null,
        "index_number" text not null
    );
'''

drop_box='''
    drop table if exists 'box_office';
'''
create_box='''
    create table if not exists'box_office'(
        'id' integer primary key autoincrement unique,
        "movie_title" text not null,
        "movie_box_office" integer not null,
        "chart_index" text not null
    );
'''

drop_rating='''
    drop table if exists 'rating';
'''
create_rating='''
    create table if not exists'rating'(
        'id' integer primary key autoincrement unique,
        "movie_rating" numeric not null,
        "movie_title" text not null,
        "chart_index" text not null
    );
'''

drop_year='''
    drop table if exists 'year';
'''
create_year='''
    create table if not exists'year'(
        'id' integer primary key autoincrement unique,
        "movie_title" text not null,
        "movie_year" integer not null,
        "chart_index" text not null
    );
'''

cur.execute(create_box)
cur.execute(create_movie)
cur.execute(create_rating)
cur.execute(create_year)

conn.commit()

## save into SQL function
def insert_to_database(insert_req, data_list):
    ''' Insert data from list to SQL based on 
        query requirement.
    
    Parameters
    ----------
    insert_req: string
        insert query
    data_list: list
        data for store in a list
    
    
    Returns
    -------
    None
    '''
    conn=sqlite3.connect('Movie.sqlite')
    cur=conn.cursor()
    for i in data_list:
        cur.execute(insert_req,i)
    conn.commit()

## Create movie table
insert_movie_chart='''
    INSERT INTO movie_chart
    VALUES (?,?,?,?)
'''
charts=final.build_chart_url_dict()
alpha=['A','B','C','D','E','F']
all_chart_list=[]
for i in range(len(charts)):
    chart_name=list(charts.keys())[i]
    chart_id=str(i+1)
    chart_index=alpha[i]
    chart_data=[chart_id,chart_name,"100",chart_index]
    all_chart_list.append(chart_data)
insert_to_database(insert_movie_chart,all_chart_list)

## Create boxoffice, rating and year table
insert_box_office='''
    INSERT INTO box_office
    VALUES (?,?,?,?)
'''
insert_rating='''
    INSERT INTO rating
    VALUES (?,?,?,?)
'''
insert_year='''
    INSERT INTO year
    VALUES (?,?,?,?)
'''
boxoffice_list=[]
rating_list=[]
year_list=[]
index=0
for i in range(len(charts)):
    chart_index=alpha[i]
    chart_url= list(charts.values())[i]
    movie_object_list=final.get_movies_list_for_chart(chart_url)
    for m in range(len(movie_object_list)):
        movie_title=movie_object_list[m].title
        box_office=movie_object_list[m].boxoffice
        rating=movie_object_list[m].rating
        year=movie_object_list[m].year
        index +=1

        movie_box_list=[str(index),movie_title,box_office,chart_index]
        movie_rating_list=[str(index),rating,movie_title,chart_index]
        movie_year_list=[str(index),movie_title,year,chart_index]

        boxoffice_list.append(movie_box_list)
        rating_list.append(movie_rating_list)
        year_list.append(movie_year_list)
insert_to_database(insert_box_office,boxoffice_list)
insert_to_database(insert_rating,rating_list)
insert_to_database(insert_year,year_list)

