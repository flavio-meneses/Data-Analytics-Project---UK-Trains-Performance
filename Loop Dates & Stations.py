import itertools
import datetime
import numpy as np
from CallAPI import readData

#parameters
dayStart = datetime.datetime(2022, 1, 3, 0, 0)
dayEnd = datetime.datetime(2022, 1, 10, 10, 0)

#stations
stations = [
    'BHI', 'BHM', 'BON', 'CAR', 'CTR', 'COV', 'CRE', 'EDB', 'EUS', 'GLC',
    'HYM', 'HHD', 'LAN', 'LTV', 'LIV', 'LSP', 'MAC', 'MAN', 'MKC', 'MTH',
    'NMP', 'NUN', 'PRE', 'RUG', 'STA', 'SPT', 'SOT', 'TAM', 'WBQ', 'WFJ',
    'WGN', 'WVH'
]
#combine stations with all possible options into pairs From/To
stationsCombination = list(itertools.permutations(stations, 2))

#arrange dates
hourIncrease = datetime.timedelta(hours=2)  #hourly step
days = np.arange(dayStart, dayEnd, hourIncrease).astype(
    datetime.datetime)  #convert to list of dates & hour

#read data for each start & end station...
for journey in stationsCombination:

    stationFrom = journey[0]
    stationTo = journey[1]

    #...and each date & hour
    for i in range(0, len(days) - 1):

        hour = int(days[i].time().strftime("%H"))  #convert to hour

        if days[i].weekday() <= 4:  #Monday to Friday only
            if (hour >= 6 and hour <= 9) or (hour >= 16
                                             and hour <= 18):  #rush hour only

                dateFrom = days[i].date().strftime("%Y-%m-%d")
                dateTo = days[i + 1].date().strftime("%Y-%m-%d")
                HourFrom = days[i].time().strftime("%H%M")
                HourTo = days[i + 1].time().strftime("%H%M")

                print("--------------------")
                print(stationFrom, "->", stationTo, "_", dateFrom, "->",
                      dateTo, "_", HourFrom, "->", HourTo)

                #call API
                readData(stationFrom, stationTo, dateFrom, dateTo, HourFrom,
                         HourTo)
