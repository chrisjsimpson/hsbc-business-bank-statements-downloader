import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


code = input("What's the code?")

fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/excel type")

browser = webdriver.Firefox(firefox_profile=fp)
browser.get('https://www.business.hsbc.co.uk/1/2/online-services/accounts/account-list')

assert 'HSBC' in browser.title

usernamelm = browser.find_element_by_id('userid1')

usernamelm.send_keys('SESHI' + Keys.RETURN)

browser.implicitly_wait(10) # seconds

memorableAnswerelm = browser.find_element_by_id('memorableAnswer')
memorableAnswerelm.send_keys('')



securitycodeelm = browser.find_element_by_id('idv_OtpCredential')
securitycodeelm.send_keys(str(code) + Keys.RETURN)

# Perform login
submitelm = browser.find_element_by_css_selector('.csButton.hsbcBibButtonStyle01.csAct')
submitelm.click()

# Load dashboard

goelm = browser.find_element_by_css_selector('.jhxCursorHand')
goelm.click()

# Load statements (choose acount) selection

statementsPageUrl = "https://www.business.hsbc.co.uk/1/3/online-services/bib-historic-statements?cmd_leftnav=leftnav&functionName=Statements&state=true&BlitzToken=blitz&transactionalSite=true&activeCUNParam=hsbc.B2G.historic_statements_page&LinkCategory=LHN&LinkID=YourAcc_Acc_Statements"

browser.get(statementsPageUrl)

# Select statements download page
downloadelm = browser.find_element_by_css_selector('.button.act.BIBHSSubmitLink3.BIBHistStmts-no-js-show')

downloadelm.click()

statementLinks = browser.find_elements_by_css_selector('.button.act.BIBHSSubmitLink.BIBHistStmts-no-js-show')
numStatements = len(statementLinks)

# Loop each statement link and download it as an excel sheet
for index, statement in enumerate(statementLinks):
    browser.implicitly_wait(10) # seconds

    # Regenerate statement link elements as they're stale from visiting other pages
    statementLinksFresh = browser.find_elements_by_css_selector('.button.act.BIBHSSubmitLink.BIBHistStmts-no-js-show')

    # Click individual statement link
    statementLinksFresh[index].click()
    # Perform download of excel sheet
    transactiondownloadradioelm = browser.find_element_by_id('txdownload')
    transactiondownloadradioelm.click()
    formatselectionelm = browser.find_element_by_id('formats')
    # Choose excel file format
    Select(formatselectionelm).select_by_index(2)
    # Initial Download button (there is a confirmation step)
    downloadelm = browser.find_elements_by_css_selector('.hsbcBibButtonStyle01B2GUpdate.BIBHistStmts-no-js-show')[3]
    if 'Download' not in downloadelm.get_attribute('value'):
        #Subsequent pages have different class names, which throw out download btn index
        downloadelm = browser.find_elements_by_css_selector('.hsbcBibButtonStyle01B2GUpdate.BIBHistStmts-no-js-show')[5]
    downloadelm.click()
    # Download confirm button
    downloadconfirmelm = browser.find_element_by_css_selector('.hsbcBibButtonStyle01B2G')
    downloadconfirmelm.click() # Perform excel download
    # Go back to statements page
    browser.get(statementsPageUrl)
    # Select statements download page
    downloadelm = browser.find_element_by_css_selector('.button.act.BIBHSSubmitLink3.BIBHistStmts-no-js-show')
    downloadelm.click()
