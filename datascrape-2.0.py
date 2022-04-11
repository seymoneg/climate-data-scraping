from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import csv

driver = webdriver.Chrome()

def coords():
    coordinates = driver.find_elements(by=By.XPATH, value="//span[@class='subheading']")

    coord_list = []
    for cl in range(len(coordinates)):
        coord_list.append(coordinates[cl].text)

    latitude = ''
    longitude = ''
    for i in coord_list:
        latitude = i[0:8]
        longitude = i[10:]

    return latitude, longitude


def loc():
    location = driver.find_elements(by=By.XPATH, value="//*[@id='inner-content']/div[1]/lib-city-header/div[1]/div/h1/span[1]")
    locationClean = location[0].text
    dbLocation = locationClean.replace(locationClean[15:],'')

    dbCity = dbLocation.split()[0]
    city = dbCity.replace(dbCity[11],'')
    state = dbLocation.split()[1]

    return city, state

def monYr():
    drpMonth = Select(driver.find_element(By.ID, "monthSelection"))
    month = drpMonth.first_selected_option
    dbMonth = month.text

    drpYear = Select(driver.find_element(By.ID, "yearSelection"))
    year = drpYear.first_selected_option
    dbYear = year.text

    return dbMonth, dbYear

def temps():
    maxTemp = driver.find_element(by=By.XPATH, value="//*[@id='inner-content']/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[1]/td[1]")
    dbMaxTemp = maxTemp.text

    avgTemp = driver.find_element(by=By.XPATH, value="//*[@id='inner-content']/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[2]/td[2]")
    dbAvgTemp = avgTemp.text

    minTemp = driver.find_element(by=By.XPATH, value="//*[@id='inner-content']/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[3]/td[3]")
    dbMinTemp = minTemp.text

    return dbMaxTemp, dbAvgTemp, dbMinTemp

def precipitation():
    precipAvg = driver.find_element(by=By.XPATH, value="//*[@id='inner-content']/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[3]/tr[1]/td[2]")
    dbPrecipAvg = precipAvg.text

    return dbPrecipAvg

def wind():
    windAvg = driver.find_element(by=By.XPATH, value="//*[@id='inner-content']/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[4]/tr[1]/td[2]")
    dbWindAvg = windAvg.text

    return dbWindAvg

    winds = wind()

def writeToCSV(finalLat, finalLong, finalCity, finalState, finalMonth, finalYear, maxTmp, avgTmp, minTmp, precips, winds):
    csvData = [finalLat, finalLong, finalCity, finalState, finalMonth, finalYear, maxTmp, avgTmp, minTmp, precips, winds]

    with open('climateData.csv', 'a+', newline="") as csvFile:
        csvFile.seek(0)
        reader = csv.reader(csvFile)
        currentCsv = list(reader)
        csvLength = len(currentCsv)

        if csvLength == 0:
            writer = csv.writer(csvFile)
            writer.writerow(['Latitude','Longitude','City','State','Month','Year','Maximum Temperature','Average Temperature','Minimum Temperature','Precipitation Average','Wind Average'])
            writer.writerow(csvData)
        else:
            writer = csv.writer(csvFile)
            writer.writerow(csvData)
    csvFile.close()

def main():
    for year in range(2011,2022):
        for month in range(1,13):
            page_date = str(year) + '-' + str(month) +'/'
            # Morrisville, NC
            url = 'https://www.wunderground.com/history/monthly/us/nc/morrisville/KRDU/date/' + page_date
            print(url)
            driver.get(url)
            time.sleep(3)

            finalLat, finalLong = coords()
            finalCity, finalState = loc()
            finalMonth, finalYear = monYr()
            maxTmp, avgTmp, minTmp = temps()
            precips = precipitation()
            winds = wind()

            writeToCSV(finalLat, finalLong, finalCity, finalState, finalMonth, finalYear, maxTmp, avgTmp, minTmp, precips, winds)

    driver.close()

if __name__ == '__main__':
    main()
