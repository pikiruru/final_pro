import sqlite3
import plotly
import plotly.graph_objects as go


## MAKE RADAR CHART
def radar_chart_for_movie(movie_object):
    ''' Use movie object data and plotly function to
        make a radar plot for rating, boxoffice and year
    
    Parameters
    ----------
    movie_object: object
        an instance of a movie
    
    Returns
    -------
    None
        radar plot of data
    '''
    connection=sqlite3.connect('Movie.sqlite')
    cursor=connection.cursor()
    min_rating_query='''
        SELECT movie_rating 
        FROM rating 
        WHERE movie_rating != 'no rating' 
        ORDER by movie_rating 
        LIMIT 1
        '''
    max_rating_query='''
        SELECT movie_rating 
        FROM rating 
        WHERE movie_rating != 'no rating' 
        ORDER by movie_rating DESC
        LIMIT 1
        '''
    min_year_query='''
        SELECT movie_year 
        FROM year 
        WHERE movie_year != 'no year' 
        ORDER by movie_year 
        LIMIT 1
        '''
    max_year_query='''
        SELECT movie_year 
        FROM year 
        WHERE movie_year != 'no year' 
        ORDER by movie_year DESC
        LIMIT 1
        '''
    min_boxoffice_query='''
        SELECT movie_box_office 
        FROM box_office 
        WHERE movie_box_office != 'no boxoffice' 
        ORDER by movie_box_office 
        LIMIT 1
        '''
    min_rating=cursor.execute(min_rating_query).fetchall()
    max_rating=cursor.execute(max_rating_query).fetchall()
    min_year=cursor.execute(min_year_query).fetchall()
    max_year=cursor.execute(max_year_query).fetchall()
    min_boxoffice=cursor.execute(min_boxoffice_query).fetchall()
    connection.close()
    min_rating=float(min_rating[0][0])
    max_rating=float(max_rating[0][0])
    min_year=int(min_year[0][0])
    max_year=int(max_year[0][0])
    min_boxoffice=int(min_boxoffice[0][0])
    max_boxoffice=2797501328

    try:
        movie_rating=float(movie_object.rating)
        movie_rating=(movie_rating-min_rating)/(max_rating-min_rating)
        movie_rating=movie_rating*5
    except:
        movie_rating=0.0
    
    try:
        movie_year=int(movie_object.year)
        movie_year=(movie_year-min_year)/(max_year-min_year)
        movie_year=movie_year*5
    except:
        movie_year=0.0

    try:
        movie_boxoffice=int(movie_object.boxoffice)
        movie_boxoffice=(movie_boxoffice-min_boxoffice)/(max_boxoffice-min_boxoffice)
        movie_boxoffice=movie_boxoffice*5
    except:
        movie_boxoffice=0.0
    val=[movie_rating,movie_year,movie_boxoffice]
    category=['rating','year','boxoffice']
    val_real=[movie_object.rating,movie_object.year,movie_object.boxoffice]


    fig = go.Figure(data=go.Scatterpolar(
    r=val,
    theta=category,
    fill='toself',
    hovertext=val_real,
    hoverinfo='theta+text'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0,5]
        ),
    ),
    showlegend=False
    )

    fig.show()


## MAKE SCATTER LINE CHART
def chart_query(query_type):
    ''' Create different SQL query based on query_type,
        such as year, boxoffice, rating
    
    Parameters
    ----------
    query_type: string
        an instance of a movie
    
    Returns
    -------
    string
        string of SQL query
    '''
    if query_type.strip().lower()=='year':
        query='''
            SELECT movie_title, movie_year
            FROM year
                JOIN movie_chart
                    ON year.chart_index= movie_chart.index_number
            WHERE chart_name = ? 
            ORDER BY id
        '''
    if query_type.strip().lower()=='boxoffice':
        query='''
            SELECT movie_title, movie_box_office
            FROM box_office
                JOIN movie_chart
                    ON box_office.chart_index= movie_chart.index_number
            WHERE chart_name = ? AND movie_box_office != 'no boxoffice'
            ORDER BY id
        '''
    if query_type.strip().lower()=='rating':
        query='''
            SELECT movie_title, movie_rating
            FROM rating
                JOIN movie_chart
                    ON rating.chart_index= movie_chart.index_number
            WHERE chart_name = ? AND movie_rating != 'no rating'
            ORDER BY id
        '''
    return query

def make_year_rating_boxoffice_chart(query_type,chartname):
    query=chart_query(query_type)
    connection=sqlite3.connect('Movie.sqlite')
    cursor=connection.cursor()
    result=cursor.execute(query,[chartname,]).fetchall()
    connection.close()

    xvals=[]
    yvals=[]
    movie_name=[]
    for i in range(len(result)):
        xvals.append(i+1)
        yvals.append(result[i][1])
        movie_name.append(result[i][0])

    scatter_data=go.Scatter(
                        x=xvals,
                        y=yvals,
                        mode='lines+markers',
                        hovertext=movie_name,
                        hoverinfo='y+text',
                        marker={
                            'size': 5,
                            'color':"grey"
                        })
    basic_layout=go.Layout(title='Year Plot for '+chartname)
    fig=go.Figure(data=scatter_data,layout=basic_layout)
    fig.show()

