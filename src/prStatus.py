'''
Created on Nov 09, 2017

@authors: Indu
'''
import os
import time
import re
import getpass
import logging
import sys
from selenium import webdriver
from selenium.webdriver import ActionChains
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

    def log_setup(self, logDirPath = None, logFileNamePattern = None):

        # Disable Request logging
        logging.getLogger("urllib3").setLevel(logging.CRITICAL)
        logging.getLogger("request").setLevel(logging.CRITICAL)

        if not logDirPath and not logFileNamePattern :
            logging.basicConfig(stream=sys.stdout, level= logging.INFO,
                                format='%(message)s')
        else:
            if not os.path.exists(logDirPath):
                os.mkdir(logDirPath)
            logFileName = r'{}_{}.log'.format(logFileNamePattern, time.strftime("%Y%m%d-%H%M%S"))
            logFilePath = r'{}\{}'.format(logDirPath, logFileName)
            logging.basicConfig(filename=logFilePath.format(int(time.time())),
                                level=logging.INFO, format='%(message)s')

class prStatus:

    def pr_query(self, driver, query, authors, jiraIDPattern):
        """
        """
        totalCount = 0
        finalJIRAList = []
        finalPRList = []

        # Get PR details for each author
        for author in authors:
            logging.info("*" * 50)
            logging.info("Author       : {}".format(author))
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
                            prNum = prMatch.group()
                            break
                    regex = r'({}-\d+)'.format(jiraIDPattern)
                    jiraNumsList = re.findall(regex, pRDescription)
                    prJiraDict.update({prNum: jiraNumsList})
                    PRs.append(prNum)
                    JIRAs.extend(jiraNumsList)
                    JIRACount += len(jiraNumsList)

            totalCount += JIRACount
            finalJIRAList.extend(JIRAs)
            finalPRList.extend(PRs)

            logging.info("PR details   :")
            for prNum, jiraList in prJiraDict.iteritems():
                logging.info("     {}   -   {}".format(prNum, ", ".join(jiraList)))
            logging.info("JIRA Count   : {}".format(JIRACount))

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
        gitPRLink = raw_input("Enter Git repo PR link\n Example- https://github.com/xyz/Repo_Name/pulls : ")
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
        logging.info("_" * 50)
        logging.info("Details of PRs Created")
        logging.info("_" * 50)
        finalPRList, finalJIRAList, totalCount = self.pr_query(driver, createdSearch, authors, jiraIDPattern)

        utilObj = utilities()
        logging.info(utilObj.border_msg("PRs raised       : {}".format(", ".join(finalPRList)), \
                                        "JIRA List        : {}".format(", ".join(finalJIRAList)), \
                                        "Total JIRA Count : {} ".format(totalCount)))

    def pr_merged_status(self, driver, date, authors, jiraIDPattern):
        """
        """
        closedSearch = "is:pr merged:{} author:".format(date)
        logging.info("_" * 50)
        logging.info("Details of PRs Merged")
        logging.info("_" * 50)
        finalPRList, finalJIRAList, totalCount = self.pr_query(driver, closedSearch, authors, jiraIDPattern)

        utilObj = utilities()
        logging.info(utilObj.border_msg("PRs merged       : {}".format(", ".join(finalPRList)), \
                                        "JIRA List        : {}".format(", ".join(finalJIRAList)), \
                                        "Total JIRA Count : {} ".format(totalCount)))


def main():
    """
    """
    # Setup logging
    utilObj = utilities()
    reportDirPath = r'{}\{}'.format(os.path.dirname(os.path.realpath(__file__)), "StatusReports")
    utilObj.log_setup(reportDirPath, "Status_Report")
    # utilObj.log_setup()  # To generate report on console

    # Query Status
    prStatusObj = prStatus()
    gitPRLink, userName, password, authors, date, jiraIDPattern = prStatusObj.get_user_input()
    logging.info("STATUS Report: {}".format(date))
    driver = prStatusObj.setup_browser(gitPRLink)
    prStatusObj.login(driver, userName, password)
    prStatusObj.pr_create_status(driver, date, authors, jiraIDPattern)
    prStatusObj.pr_merged_status(driver, date, authors, jiraIDPattern)
    driver.close()


if __name__ == "__main__":
    main()
