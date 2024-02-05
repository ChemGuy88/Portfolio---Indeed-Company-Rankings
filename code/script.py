"""
Scrape Indeed for Company rankings, and number of reviews
"""

import logging
import os
from pathlib import Path
# Third-party packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# Local packages
from drapi.code.drapi.drapi import (getTimestamp,
                                    makeDirPath,
                                    successiveParents)

# Arguments
EMAIL_ADDRESS = "hf.autore@hotmail.com"
PASSWORD = os.environ["HFA_STASIA2_PWD"]

NUM_MAX_CLICKS = 100
CHROME_DRIVER_PATH = "data/input/chromedriver-mac-x64_116/chromedriver"
CHROME_BINARY_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Arguments: Meta-variables
PROJECT_DIR_DEPTH = 2
DATA_REQUEST_DIR_DEPTH = PROJECT_DIR_DEPTH + 3
IRB_DIR_DEPTH = PROJECT_DIR_DEPTH + 1
IDR_DATA_REQUEST_DIR_DEPTH = PROJECT_DIR_DEPTH + 4

ROOT_DIRECTORY = "IRB_DIRECTORY"  # TODO One of the following:
                                                 # ["IDR_DATA_REQUEST_DIRECTORY",    # noqa
                                                 #  "IRB_DIRECTORY",                 # noqa
                                                 #  "DATA_REQUEST_DIRECTORY",        # noqa
                                                 #  "PROJECT_OR_PORTION_DIRECTORY"]  # noqa

LOG_LEVEL = "INFO"

# Arguments: SQL connection settings
SERVER = "DWSRSRCH01.shands.ufl.edu"
DATABASE = "DWS_PROD"
USERDOMAIN = "UFAD"
USERNAME = os.environ["USER"]
UID = None
PWD = os.environ["HFA_UFADPWD"]

# Variables: Path construction: General
runTimestamp = getTimestamp()
thisFilePath = Path(__file__)
thisFileStem = thisFilePath.stem
projectDir, _ = successiveParents(thisFilePath.absolute(), PROJECT_DIR_DEPTH)
dataRequestDir, _ = successiveParents(thisFilePath.absolute(), DATA_REQUEST_DIR_DEPTH)
IRBDir, _ = successiveParents(thisFilePath.absolute(), IRB_DIR_DEPTH)
IDRDataRequestDir, _ = successiveParents(thisFilePath.absolute(), IDR_DATA_REQUEST_DIR_DEPTH)
dataDir = projectDir.joinpath("data")
if dataDir:
    inputDataDir = dataDir.joinpath("input")
    outputDataDir = dataDir.joinpath("output")
    if outputDataDir:
        runOutputDir = outputDataDir.joinpath(thisFileStem, runTimestamp)
logsDir = projectDir.joinpath("logs")
if logsDir:
    runLogsDir = logsDir.joinpath(thisFileStem)
sqlDir = projectDir.joinpath("sql")

if ROOT_DIRECTORY == "PROJECT_OR_PORTION_DIRECTORY":
    rootDirectory = projectDir
elif ROOT_DIRECTORY == "DATA_REQUEST_DIRECTORY":
    rootDirectory = dataRequestDir
elif ROOT_DIRECTORY == "IRB_DIRECTORY":
    rootDirectory = IRBDir
elif ROOT_DIRECTORY == "IDR_DATA_REQUEST_DIRECTORY":
    rootDirectory = IDRDataRequestDir
else:
    raise Exception("An unexpected error occurred.")

# Variables: Path construction: Project-specific
pass

# Variables: SQL Parameters
if UID:
    uid = UID[:]
else:
    uid = fr"{USERDOMAIN}\{USERNAME}"
conStr = f"mssql+pymssql://{uid}:{PWD}@{SERVER}/{DATABASE}"

# Variables: Other
pass

# Directory creation: General
makeDirPath(runOutputDir)
makeDirPath(runLogsDir)

# Logging block
logpath = runLogsDir.joinpath(f"log {runTimestamp}.log")
logFormat = logging.Formatter("""[%(asctime)s][%(levelname)s](%(funcName)s): %(message)s""")

logger = logging.getLogger(__name__)

fileHandler = logging.FileHandler(logpath)
fileHandler.setLevel(9)
fileHandler.setFormatter(logFormat)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(LOG_LEVEL)
streamHandler.setFormatter(logFormat)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

logger.setLevel(9)

if __name__ == "__main__":
    logger.info(f"""Begin running "{thisFilePath}".""")
    logger.info(f"""All other paths will be reported in debugging relative to `{ROOT_DIRECTORY}`: "{rootDirectory}".""")
    logger.info(f"""Script arguments:


    # Arguments
    `EMAIL_ADDRESS`: "{EMAIL_ADDRESS}"
    `NUM_MAX_CLICKS`: "{NUM_MAX_CLICKS}"
    `CHROME_DRIVER_PATH`: "{CHROME_DRIVER_PATH}"
    `CHROME_BINARY_PATH`: "{CHROME_BINARY_PATH}"

    # Arguments: General
    `PROJECT_DIR_DEPTH`: "{PROJECT_DIR_DEPTH}" ----------> "{projectDir}"
    `IRB_DIR_DEPTH`: "{IRB_DIR_DEPTH}" --------------> "{IRBDir}"
    `IDR_DATA_REQUEST_DIR_DEPTH`: "{IDR_DATA_REQUEST_DIR_DEPTH}" -> "{IDRDataRequestDir}"

    `LOG_LEVEL` = "{LOG_LEVEL}"

    # Arguments: SQL connection settings
    `SERVER` = "{SERVER}"
    `DATABASE` = "{DATABASE}"
    `USERDOMAIN` = "{USERDOMAIN}"
    `USERNAME` = "{USERNAME}"
    `UID` = "{UID}"
    `PWD` = censored
    """)

    # Industry categories: Manual list
    LIST_OF_INDUSTRY_CATEGORIES = ["https://www.indeed.com/companies/best-Aerospace-&-Defense-companies",
                                   "https://www.indeed.com/companies/best-Agriculture-companies",
                                   "https://www.indeed.com/companies/best-Arts,-Entertainment-&-Recreation-companies",
                                   "https://www.indeed.com/companies/best-Construction,-Repair-&-Maintenance-Services-companies",
                                   "https://www.indeed.com/companies/best-Education-companies",
                                   "https://www.indeed.com/companies/best-Energy,-Mining-&-Utilities-companies"]

    HOMEURL = "https://www.anastasiadate.com/"
    IN_BETWEEN_PAGE_DELAY = 10

    # Start driver
    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument('window-size=1920x1080')
    options.binary_location = CHROME_BINARY_PATH
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)

    # Go to companies page.
    logger.info("Going to companies page.")
    COMPANIES_HOMEPAGE = "https://www.indeed.com/companies"
    driver.get(COMPANIES_HOMEPAGE)
    logger.info("Going to companies page - Done.")
    # Search first group of industry pages
    logger.info("Getting first six industry category links.")
    industryCategoryLinks = {}
    # TODO Scrape
    # Select with: a[data-tn-element="cmp-Industry-link"]
    # Get attribute: child text
    categoryName = _
    # Get attribute: href
    categoryLink = _
    industryCategoryLinks[categoryName] = categoryLink
    logger.info("Getting first six industry category links. - Done.")

    # See all the other industry categories.
    logger.info("See all industries.")
    # TODO Click
    logger.info("See all industries - Done.")
    logger.info("Scraping all other industry category links.")
    # Get attribute: child text
    categoryName = _
    # Get attribute: href
    categoryLink = _
    industryCategoryLinks[categoryName] = categoryLink

    # For industry category in `industryCategoryLinks`
    for categoryName, categoryLink in industryCategoryLinks.items():
        # TODO :While there is a next-page button:
        while _:
            pass
            # TODO Get company name
            # TODO Get company star rating
            # TODO Get number of company reviews
            # TODO Go to next page

    # End script
    logger.info(f"""Finished running "{thisFilePath.absolute().relative_to(rootDirectory)}".""")
