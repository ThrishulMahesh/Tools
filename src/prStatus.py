'''
Created on Nov 09, 2017

@authors: Indu
'''
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import re
import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

def border_msg(*args):
    count = 0
    for msg in args:
        length = len(msg) + 2
        if length > count:
            count = length
            msgLength = len(msg)
    dash = "-"*count
    output = "+{dash}+\n".format(dash=dash)

    for msg in args:
        output += "| {msg} |\n".format(msg=msg.ljust(msgLength))

    output += "+{dash}+\n".format(dash=dash)
    return output

#####################################################################################################
def pr_query(query, authors, jiraIDPattern):
    totalCount = 0
    finalJIRAList = []
    finalPRList = []

    # PRs created
    for author in authors:
        print "*" * 50
        print "Author       : {}".format(author)
        search = query + author
        searchBox = driver.find_element_by_id("js-issues-search")
        searchBox.clear()
        searchBox.send_keys(search)
        searchBox.send_keys(Keys.ENTER)
        time.sleep(5)

        # PR details
        JIRAs = []
        PRs = []
        prJiraDict = {}
        JIRACount = 0
        if len(driver.find_elements_by_xpath("//div[@class='border-right border-bottom border-left']")) > 0:
            prList = driver.find_element_by_xpath("//div[@class='border-right border-bottom border-left']")
            listItems = prList.find_elements_by_tag_name("li")
            for item in listItems:
                pRDescription = item.text
                for line in pRDescription.splitlines():
                    prMatch = re.match(r'(#\d+)', line)
                    if prMatch:
                        pr = prMatch.group()
                        break
                regex = r'({}-\d+)'.format(jiraIDPattern)
                jiraNumsList = re.findall(regex, pRDescription)
                prJiraDict.update({pr: jiraNumsList})
                PRs.append(pr)
                JIRAs.extend(jiraNumsList)
                JIRACount += len(jiraNumsList)

        totalCount += JIRACount
        finalJIRAList.extend(JIRAs)
        finalPRList.extend(PRs)

        print "PR details   :"
        for pr, jiraList in prJiraDict.iteritems():
            print "     {}   -   {}".format(pr, ", ".join(jiraList))
        print "JIRA Count   : {}".format(JIRACount)

    return finalPRList, finalJIRAList, totalCount

gitPRLink = ""
userName = ""
password = ""

chromedriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
wait = WebDriverWait(driver, 10)
driver.get(gitPRLink)

# Login
actions = ActionChains(driver)
user_Name = driver.find_element_by_id("login_field")
user_Name.send_keys(userName)
pwd = driver.find_element_by_id("password")
pwd.send_keys(password)
login = driver.find_element_by_name("commit")
actions.click(login).perform()

# Date in YYYY-MM-DD format
date = "2017-11-09"
# Authors List
authors = []
createdSearch = "is:pr created:{} author:".format(date)
closedSearch = "is:pr closed:{} author:".format(date)
# createdSearch = "is:pr created:2017-11-01..2017-11-02 author:"

print "STATUS Report: {}".format("2017-11-09")
print "_"*50
print "Details of PRs Created"
print "_"*50

finalPRList, finalJIRAList, totalCount = pr_query(createdSearch, authors)

print border_msg("PRs raised       : {}".format(", ".join(finalPRList)),\
                 "JIRA List        : {}".format(", ".join(finalJIRAList)),\
                 "Total JIRA Count : {} ".format(totalCount))

#################################################################################################################################################

print "_"*50
print "Details of PRs Closed"
print "_"*50

finalPRList, finalJIRAList, totalCount = pr_query(closedSearch, authors)

print border_msg("PRs closed       : {}".format(", ".join(finalPRList)),\
                 "JIRA List        : {}".format(", ".join(finalJIRAList)),\
                 "Total JIRA Count : {} ".format(totalCount))