import os
import sys

# Tambahkan path ke root project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from process import *
id = "263109"
title = ""
season = 1
# run_movie(movie_id=id, title=title)
run_tv(tv_id=id, title=title, season_number=season)
        