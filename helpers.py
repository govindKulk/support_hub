import datetime
import os
def generate_file_name(timeframe = "", suffix = "market"):
    # ex file name: 26 july before market.csv or 26 july after market.csv

    # check whether the timeframe file is present in direcotry
    if os.path.exists(datetime.datetime.now().strftime("%d") + " " + datetime.datetime.now().strftime("%m").lower() + " " + timeframe + " market.csv"):
        timeframe = "before"



    file_name = datetime.datetime.now().strftime("%d") + " " + datetime.datetime.now().strftime("%m").lower() + " " + timeframe + " " + suffix + ".csv"
    return file_name