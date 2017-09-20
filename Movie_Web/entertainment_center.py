# Lesson 3.4: Make Classes
# Mini-Project: Movies Website

# In this file, you will define instances of the class Movie defined
# in media.py. After you follow along with Kunal, make some instances
# of your own!

# After you run this code, open the file fresh_tomatoes.html to
# see your webpage!

import media
import fresh_tomatoes


movies_detail = [
	['The Dark Knight', 'https://www.youtube.com/watch?v=EXeTwQWrcwY', 'http://www.impawards.com/2008/posters/dark_knight_ver4.jpg', 'Movie Info: Visionary filmmaker Christopher Nolan\'s sequel to the highly successful "Batman Begins" sees Batman (Christian Bale) as he raises the stakes in his war on crime. With the help of Lieutenant Jim Gordon (Gary Oldman) and District Attorney Harvey Dent (Aaron Eckhart)...'],
	['Das Leben Der Anderen', 'https://www.youtube.com/watch?v=J3DsLPq884M', 'https://i.pinimg.com/564x/08/59/8d/08598d5ed2a54b3b465a921fb2006d84.jpg', 'Movie Info: This critically-acclaimed, Oscar-winning film (Best Foreign Language Film, 2006) is the erotic, emotionally-charged experience Lisa Schwarzbaum (Entertainment Weekly) calls "a nail-biter of a thriller!"  Before the collapse of the Berlin Wall, East Germany\'s population was...'],
	['Scent of a Woman', 'https://www.youtube.com/watch?v=7xIYQgrd-Sg', 'http://www.impawards.com/1992/posters/scent_of_a_woman_ver1.jpg', 'Movie Info: Al Pacino won an Academy Award for his brilliant portrayal in this heartwarming tale of an overbearing, blind Lieutenant Colonel who hires a young guardian (Chris O\'Donnell) to assist him...'],
	['Intouchables', 'https://www.youtube.com/watch?v=34WIbmXkewU', 'http://img.goldposter.com/2015/04/The-Intouchables_poster_goldposter_com_25.jpg@0o_0l_800w_80q.jpg', 'Movie Info: When Driss, an ex-con from the projects, is hired to take care of an eccentric French aristocrat named Philippe, his newfound job quickly becomes an unpredictable adventure...'],
	['Mad Detective', 'https://www.youtube.com/watch?v=F5h2E30NJfc', 'https://images-na.ssl-images-amazon.com/images/I/A1XQYfRe02L._SL1500_.jpg', 'Movie Info: Chan Kwai-Bun (Sean Lau) is a brilliant detective with a supernatural gift seeing a person\'s "inner personalities," or hidden ghosts. However, he is forced into retirement after severing his ear and presenting it to his retiring boss...'],
	['Hannibal', 'https://www.youtube.com/watch?v=Lr3OavheNu0', 'https://i.pinimg.com/564x/4a/d1/ea/4ad1eaed2b8b41893563974198212baa.jpg', 'Movie Info: Based on the best-selling novel by Thomas Harris, HANNIBAL continues the story begun in Silence of the Lambs. Seven years have passed since Dr. Hannibal Lecter (Anthony Hopkins) escaped from custody...']
]

def get_movies_info(detail):

	movies_list = []
	for i in detail:
	    obj = media.Movie(*i)
	    movies_list.append(obj)

	return fresh_tomatoes.open_movies_page(movies_list)


if __name__ == '__main__':
	
	get_movies_info(movies_detail)