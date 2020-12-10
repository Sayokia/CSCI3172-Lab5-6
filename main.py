# Author Yanlin Zhu
# B00812966
# Some code reused or referred to Pat's code

# Headers Required
import requests
from lxml import html
from bs4 import BeautifulSoup
import time
import csv


# Below is the code for getting the data from one entry.
targetURL = 'https://dalonline.dal.ca/PROD/fyskeqiv.P_TransEquiv'

# initalize a list to store the post values params
params = {'prov': '', 'name': '', 'inst': '', 'subj': ''}

# initialize a list to store the institution data
instCodeList = []
instNameList = []





file = open('courseData.csv', 'a+', newline='')


params['prov'] = 'ALLINST'

# Make a request from the server with POST values
HTTPRequest = requests.post(targetURL, data=params)
# You might get told you're making too many requests. Take a break and try again.
while HTTPRequest.status_code == 429:
     time.wait(30)
     HTTPRequest = requests.post(targetURL, data=params)

# Parse the server response into its raw html code
HTMLcode = BeautifulSoup(HTTPRequest.content, "html.parser")



#filter HTML to find inst data
instDataSet = HTMLcode.find('select', attrs={'name': 'inst'}).find_all('option')

# for loop to get data from the data set and add them to data list
for data in instDataSet:

    # check if the code is dummy
    if(data['value'] != "DUMMY"):
        instCode = data['value']
        instName = data.text
        instCodeList.append(instCode)
        instNameList.append(instName)


# loop to find subject code by institution code
for instCode in instCodeList:


    # get the index of inst code form the list list
    index = instCodeList.index(instCode)

    #update params
    params['prov'] = 'AllINST'
    #as the inst name share the same index of inst code, we can get inst name by the index of inst code
    params['name'] = instNameList[index]
    params['inst'] = instCode

    # initilize a list to store the subject data
    subjectList = []

    # Make a request from the server with POST values
    HTTPRequest = requests.post(targetURL, data=params)
    # You might get told you're making too many requests. Take a break and try again.
    while HTTPRequest.status_code == 429:
        time.wait(30)
        HTTPRequest = requests.post(targetURL, data=params)

    # Parse the server response into its raw html code
    HTMLcode = BeautifulSoup(HTTPRequest.content, "html.parser")

    # filter HTML to find subject data
    subjectDataSet = HTMLcode.find('select', {'name': 'subj'})

    # exclude the empty data
    if subjectDataSet is not None:
        validSubjectDataSet = subjectDataSet.findAll('option')
        for subject in validSubjectDataSet:
            if (subject['value'] != "DUMMY"):
                subjectList.append(subject['value'])


    #loop to find course info by subject code
    for subject in subjectList:
        #update params
        params['subj'] = subject


        # Make a request from the server with POST values
        HTTPRequest = requests.post(targetURL, data=params)
        # You might get told you're making too many requests. Take a break and try again.
        while HTTPRequest.status_code == 429:
            time.wait(30)
            HTTPRequest = requests.post(targetURL, data=params)

        # Parse the server response into its raw html code
        HTMLcode = BeautifulSoup(HTTPRequest.content, "html.parser")
        # All the data we want is in td tags that are of class default
        td = HTMLcode.find_all('td', attrs={'class': 'dedefault'})

        #put institution name, code and subject name into final list item String
        finalListHeader = params['inst'] + ";" + params['name'] + ";" + params['subj']

        #create temp to combine 5 course elements into one
        temp = ""
        #use counter to control the process
        counter = 0

        # create csv writer
        write = csv.writer(file, delimiter=';')


        for course in td:
            courseData = course.text
            # check is the empty data
            if (courseData is not None):
                # remove  <br> \n \r \t special character
                courseData = courseData.replace('<br>', '').replace('\n', '').replace('\r', '').replace('\t', '')

                # add data to temp
                temp += ";" + courseData
                counter += 1
                if counter == 5:
                    #combine header with data
                    finalListItem = finalListHeader + temp

                    #turn string into list
                    finalList = list(finalListItem.split(";"))
                    # print result to screen
                    print(finalList)
                    # write the course data into file
                    write.writerow(finalList)

                    #reinitialize temp and counter As this this the sixth value,set it as the first of next group
                    temp = ""
                    counter = 0



































