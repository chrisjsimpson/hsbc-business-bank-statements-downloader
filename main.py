import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

'''
Note: browser is declared as a global.
'''

def login():
  code = input("What's the code?")
  fp = webdriver.FirefoxProfile()
  fp.set_preference("browser.download.folderList",2)
  fp.set_preference("browser.download.manager.showWhenStarting",False)
  fp.set_preference("browser.download.dir", os.getcwd())
  fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/excel type")

  global browser 
  browser = webdriver.Firefox(firefox_profile=fp)
  browser.get('https://www.business.hsbc.co.uk/1/2/online-services/accounts/account-list')
  assert 'HSBC' in browser.title
  usernamelm = browser.find_element_by_id('userid1')
  usernamelm.send_keys('SESHI' + Keys.RETURN)
  browser.implicitly_wait(10) # seconds
  memorableAnswerelm = browser.find_element_by_id('memorableAnswer')
  memorableAnswerelm.send_keys(os.getenv('memorable'))

  securitycodeelm = browser.find_element_by_id('idv_OtpCredential')
  securitycodeelm.send_keys(str(code) + Keys.RETURN)

  # Perform login
  submitelm = browser.find_element_by_css_selector('.csButton.hsbcBibButtonStyle01.csAct')
  submitelm.click()
  # Load dashboard
  goelm = browser.find_element_by_css_selector('.jhxCursorHand')
  goelm.click()
  return browser

def goto_list_of_accounts_with_statements():
  """ List of accounts which have statements available """
  # Load statements (choose acount) selection
  statementsPageUrl = "https://www.business.hsbc.co.uk/1/3/online-services/bib-historic-statements?cmd_leftnav=leftnav&functionName=Statements&state=true&BlitzToken=blitz&transactionalSite=true&activeCUNParam=hsbc.B2G.historic_statements_page&LinkCategory=LHN&LinkID=YourAcc_Acc_Statements"
  browser.get(statementsPageUrl)

def goto_account_statements_list(page=None):
  """ Go to select statements download page for an account """
  goto_list_of_accounts_with_statements() # First go to list of account which have statements
  # Go to the first account in the list to view its statements list (page 1)
  # TODO don't hard code visiting the first account only
  downloadelm = browser.find_element_by_css_selector('.button.act.BIBHSSubmitLink3.BIBHistStmts-no-js-show')
  downloadelm.click()
  
def calculate_num_statement_pagination_pages():
  """ Get number of paginated pages to loop through (if many years of 
  statemens, then the bank account will have many pages of statements 
  to loop through

  Link 1 is not a hyperlink until navigating to another page
  (because each page is implemented as a html <input> for some reason.
  """

  # Get the next page links (which are <input> elements)
  # Yes, the css literally has classes BIBHSSubmitLink1, BIBHSSubmitLink2, etc up till 3
  # It's currently unknown what happends beyond 3.
  # NOTE: Pagination links are repeated above and below the table, so number of 
  # elements is double.
  # NOTE: css name "BIBHSSubmitLink1" refers to page 2, not page 1.
  numPages = 1 # Default to 1 page
  if len(browser.find_elements_by_css_selector('.button.act.BIBHSSubmitLink1')) == 2:
    numPages = 2
  if len(browser.find_elements_by_css_selector('.button.act.BIBHSSubmitLink2')) == 2:
    numPages = 3
  if len(browser.find_elements_by_css_selector('.button.act.BIBHSSubmitLink3')) == 2:
    numPages = 4
  print("There are {} paginated pages for this account".format(numPages))
  return numPages

def download_statements_on_page(pageNumber=None):
  """Download all statements on the current paginated page.
  Does not perform any next page logic, this is delegated to
  another function.

  This function simply visits and downloads all available statements on
  the current page which has a list of up to 24 statements (any more than
  24 statements then HSBC puts this onto another page (so pagination handling
  is then needed).
  """

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
      # Go back to statements page with list of available statements to download
      goto_statements_page_number(pageNumber)

def next_statements_page_exists():
  goto_account_statements_list()
  nextStatementsElm = browser.find_element_by_css_selector('.button.act.hsbcBibButtonStyle01B2GUpdate.BIBHistStmts-no-js-show')
  if nextStatementsElm:
    return True
  return False 

def goto_statements_page_number(pageNumber=0):
  # NOTE we select the *third* button with this class match (which is the 
  # "Next Statements" btn
  goto_list_of_accounts_with_statements()
  goto_account_statements_list()
  if pageNumber != 1: # Only go to next page when pageNumer isn't 0
    # Press "Next Statements" until we get to pageNumber.
    for count in range(1, pageNumber):
      nextStatementsElm = browser.find_elements_by_css_selector('.button.act.hsbcBibButtonStyle01B2GUpdate.BIBHistStmts-no-js-show')[3]
      nextStatementsElm.click() 
  
  

login()
goto_list_of_accounts_with_statements()
goto_account_statements_list()
numPages = calculate_num_statement_pagination_pages()
pageNumber = 1 # start at page 1
download_statements_on_page(pageNumber=1)
while pageNumber <= numPages:
  if next_statements_page_exists():
    goto_list_of_accounts_with_statements()
    goto_account_statements_list()
    goto_statements_page_number(pageNumber)
    download_statements_on_page(pageNumber)
    pageNumber += 1

browser.close()  
exit(1)
