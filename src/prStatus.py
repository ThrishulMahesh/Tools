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

class utilities:

    def border_msg(self, *args):
        """
        """
        count = 0
        for msg in args:
            length = len(msg) + 2
            if length > count:
                count = length
                msgLength = len(msg)
        dash = "-" * count
        output = "+{dash}+\n".format(dash=dash)

        for msg in args:
            output += "| {msg} |\n".format(msg=msg.ljust(msgLength))

        output += "+{dash}+\n".format(dash=dash)
        return output

class prStatus:

    def pr_query(self, driver, query, authors, jiraIDPattern):
        """
        """
        totalCount = 0
        finalJIRAList = []
        finalPRList = []

        # Get PR details for each author
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

    def login(self, driver, userName, password):
        """
        """
        # Login
        actions = ActionChains(driver)
        user_Name = driver.find_element_by_id("login_field")
        user_Name.send_keys(userName)
        pwd = driver.find_element_by_id("password")
        pwd.send_keys(password)
        login = driver.find_element_by_name("commit")
        actions.click(login).perform()

    def get_user_input(self):
        """
        """
        gitPRLink = raw_input("Enter Git repo PR link\n Example- https://github.com/xyz/Tools/pulls : ")
        userName = raw_input("Enter Github Username : ")
        password = getpass.getpass("Enter Github Password : ")
        authorsInput = raw_input("Enter list of Authors to query status\n Example - abc pqr xyz  : ")
        authors = authorsInput.split()
        date = raw_input("Enter Status query Date\n(For single day - YYYY-MM-DD\n For range - YYYY-MM-DD..YYYY-MM-DD) : ")
        jiraIDPattern = raw_input("Enter JIRA ID pattern : ")

        return gitPRLink, userName, password, authors, date, jiraIDPattern

    def setup_browser(self, url):
        """
        """
        chromedriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        wait = WebDriverWait(driver, 10)
        driver.get(url)
        return driver

    def pr_create_status(self, driver, date, authors, jiraIDPattern):
        """
        """
        createdSearch = "is:pr created:{} author:".format(date)
        # createdSearch = "is:pr created:2017-11-01..2017-11-02 author:"
        print "_" * 50
        print "Details of PRs Created"
        print "_" * 50
        finalPRList, finalJIRAList, totalCount = self.pr_query(driver, createdSearch, authors, jiraIDPattern)

        utilObj = utilities()
        print utilObj.border_msg("PRs raised       : {}".format(", ".join(finalPRList)), \
                                 "JIRA List        : {}".format(", ".join(finalJIRAList)), \
                                 "Total JIRA Count : {} ".format(totalCount))

    def pr_close_status(self, driver, date, authors, jiraIDPattern):
        """
        """
        closedSearch = "is:pr closed:{} author:".format(date)
        print "_" * 50
        print "Details of PRs Closed"
        print "_" * 50
        finalPRList, finalJIRAList, totalCount = self.pr_query(driver, closedSearch, authors, jiraIDPattern)

        utilObj = utilities()
        print utilObj.border_msg("PRs closed       : {}".format(", ".join(finalPRList)), \
                                 "JIRA List        : {}".format(", ".join(finalJIRAList)), \
                                 "Total JIRA Count : {} ".format(totalCount))


def main():
    """
    """
    prStatusObj = prStatus()
    gitPRLink, userName, password, authors, date, jiraIDPattern = prStatusObj.get_user_input()
    print "STATUS Report: {}".format(date)
    driver = prStatusObj.setup_browser(gitPRLink)
    prStatusObj.login(driver, userName, password)
    prStatusObj.pr_create_status(driver, date, authors, jiraIDPattern)
    prStatusObj.pr_close_status(driver, date, authors, jiraIDPattern)
    driver.close()

if __name__ == "__main__":
    main()
