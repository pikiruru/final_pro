This is a simple python project about provide information about IMDb movie chart and movie information.

Required packages:
	BeautifulSoup,requests,sqlite3,plotly

File: 	cache.py, 
      	database.py, 
	plot.py,
	yizhulu_final.py, 
	README.txt, 
	Movie.sqlite
	.gitignore

How to run code:
	1. cache.py contains function to save cache, load cache, fetch data from URL or API to store in cache, I import cache.py to yizhulu_final.py to use cache;
	2. database.py contains function to create SQL file, create 4 tables and save movie data I get into SQL. The Movie.sqlite is the file I make by using database.py and it contains information I access. Movie.sqlite serves as database for me to get data in yizhulu_final.py.
	3. plot.py contains function to create radar plot, scatter plot by using plotly function. I import plot.py to yizhulu_final.py to make interaction;
	4. yizhulu_final.py contains function to create movie object, web scrap/web crawl data from multiple IMDb websites by using BeautifulSoup package, access data from Wikipedia API. It also use command line prompts to make interaction and presentation for movie and chart data.

How to interact:
	1. open yizhulu_final.py and run it. I write input questions and you only need to follow these questions.

