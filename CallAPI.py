import requests
import json
import os.path


def readData(stationFrom, stationTo, dateFrom, dateTo, timeFrom, timeTo):

    #parameters
    url = 'https://hsp-prod.rockshore.net/api/v1/serviceMetrics'
    Auth = 'xxxxxx'
    weekDay = "WEEKDAY"
    tolerance = ['4']
    saveFileName = "DataExports\ServiceMetrics" + "_" + stationFrom + "to" + stationTo + "_" + dateFrom + "to" + dateTo + "_" + timeFrom + "to" + timeTo + ".json"

    #assemble request
    payload = json.dumps({
        "from_loc": stationFrom,
        "to_loc": stationTo,
        "from_time": timeFrom,
        "to_time": timeTo,
        "from_date": dateFrom,
        "to_date": dateTo,
        "days": weekDay,
        "tolerance": tolerance
    })
    header = {'Authorization': Auth, 'Content-Type': 'application/json'}

    #check if file requested already exists
    #if it doesn't, create placeholder before calling API, so other scripts don't waste time calling it too
    #if it does, exit function
    os.makedirs("DataExports",
                exist_ok=True)  #create directory if it doesn't exist
    file_exists = os.path.exists(saveFileName)
    if not file_exists:
        try:  #in case two scripts try to do this at the same time, exit function
            open(saveFileName, "x")
        except:
            return
    elif file_exists:
        return

    print("Started Reading Data")

    #call API
    try:
        request = requests.post(url, headers=header, data=payload)
        request.raise_for_status()
    #handle errors
    except requests.exceptions.HTTPError as errh:
        os.remove(saveFileName)
        print("Http Error:", errh)
        return
    except requests.exceptions.ConnectionError as errc:
        os.remove(saveFileName)
        print("Error Connecting:", errc)
        return
    except requests.exceptions.Timeout as errt:
        os.remove(saveFileName)
        print("Timeout Error:", errt)
        return
    except requests.exceptions.RequestException as err:
        os.remove(saveFileName)
        print("OOps: Something Else", err)
        return

    #save response to file
    dataToJson = json.loads(request.text)
    with open(saveFileName, 'w') as fp:
        json.dump(dataToJson, fp)
        fp.close()

    print("**Completed**")