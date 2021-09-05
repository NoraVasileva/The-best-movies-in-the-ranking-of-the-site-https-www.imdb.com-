from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from model import Movies

driver = webdriver.Chrome(ChromeDriverManager().install())
engine = create_engine('sqlite:///Movies.db', echo=True) # връзка с базата данни
Session = sessionmaker(bind=engine) # създавам клас, който да се свързва с базата данни
session = Session() # създавам обект от класа, който представлява сесия, чрез която манипулирам (въвеждам)
# информация в базата


def open_top_rated_movies():
    """
    Load the site and download the list of top 250 best movies.
    Save the name, year and link of the movies in an object to the database.
    """
    site = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    driver.get(site)
    soup = BeautifulSoup(driver.page_source, "lxml") # създавам обект, който ми парсва html-a към обекта. Тоест ми
    # запазва информацията от страницата в обекта и после вътре мога да търся информация
    table = soup.find("table", class_="chart") # търсим информация за table от обекта

    for td in table.find_all("td", class_="titleColumn"): # find_all връща списък, който може да извъртим в цикъла
        movie_link = td.find("a")["href"]
        path_name = movie_link.split("?")[0]
        site_name = f"https://www.imdb.com/{path_name}"
        movie_name = td.text.strip().replace("\n", "").replace("      ", "")
        list_movie_name = list(movie_name)
        first_value = list_movie_name[0]
        second_value = list_movie_name[1]
        third_value = list_movie_name[2]
        fourth_value = list_movie_name[3]
        name_without_numbering_and_year = ""
        year = ""

        if first_value.isnumeric() is True and second_value == ".":
            name_without_numbering = movie_name[2:]
            name_without_numbering_and_year = name_without_numbering[:len(name_without_numbering) - 6]
            year = name_without_numbering[-5:-1]
        elif first_value.isnumeric() is True and second_value.isnumeric() is True and third_value == ".":
            name_without_numbering = movie_name[3:]
            name_without_numbering_and_year = name_without_numbering[:len(name_without_numbering) - 6]
            year = name_without_numbering[-5:-1]
        elif first_value.isnumeric() is True and second_value.isnumeric() is True and third_value.isnumeric() is True\
                and fourth_value == ".":
            name_without_numbering = movie_name[4:]
            name_without_numbering_and_year = name_without_numbering[:len(name_without_numbering) - 6]
            year = name_without_numbering[-5:-1]

        movie_object = Movies(movie_name=name_without_numbering_and_year, year=year, link=site_name) # запазване на имената, годината и линка в модела
        session.add(movie_object) # добавяне в базата данни
        session.commit() # изпълнение на добавянето


def movie_information():
    """
    Opens the site by taking the link to each movie, downloading the information about it and save it in the database.
    """
    movies = session.query(Movies).all()
    for movie in movies:
        driver.get(movie.link)
        soup = BeautifulSoup(driver.page_source, "lxml")
        div = soup.find("div", {"class": "subtext"})
        genre_strings = ""
        for genre in div.find_all("a"):
            if "genres" in genre["href"]:
                genre_strings += genre.text + ", "
        movie.genre = genre_strings[:-2]
        time = div.find("time")
        movie.hours = time.text.strip()
        strong = soup.find("strong")
        rating = strong.find("span").text
        movie.rating = rating
        poster = soup.find("div", {"class": "poster"})
        image = poster.find("img")["src"]
        movie.url_images = image
        div_directors = soup.find("div", {"class": "credit_summary_item"})
        movie.director = div_directors.find("a").text
        div_stars = soup.find_all("div", {"class": "credit_summary_item"})
        actors = ""
        for star in div_stars[2].find_all("a"):
            if star["href"].startswith("/name"):
                actors += star.text + ", "
        movie.actors = actors[:-2]

        session.commit()


open_top_rated_movies()

movie_information()
