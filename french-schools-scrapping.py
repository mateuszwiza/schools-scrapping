import selenium
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import numpy as np
import time

# The list of emails found so far in case something crashes mid-way
emails = []


def find_email(name, adres):
    # Open web driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()

    # Open the website
    driver.get(
        "http://www.enseignement.be/index.php?page=25933&act=search&check=&unite=&geo_type=0&geo_prov=&geo_cp"
        "=&geo_loca=&geo_mots=&reseau=111%2C126%2C123%2C122%2C121&opt_degre=&opt_tyen=&opt_domaine=0&opt_mots"
        "=&opt_groupe=11&opt_option=")
    assert "Enseignement" in driver.title

    # Find the table with the list of schools
    table = driver.find_element_by_id("liste_etablissements")

    # Find the correct cell given name and address
    for row in table.find_elements(By.TAG_NAME, "tr"):
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells[0].text == name and cells[1].text == adres:
            # Get the URL of the school subpage
            link = row.find_element_by_tag_name("a").get_attribute('href')
            break

    # Go the the school subpage
    driver.get(link)
    # Navigate to cell containing email address
    contact = driver.find_elements(By.TAG_NAME, "table")
    rows = contact[0].find_elements(By.TAG_NAME, "tr")
    cells2 = rows[2].find_elements(By.TAG_NAME, "td")
    # Get the email address
    email = cells2[1].text
    emails.append([name, email])

    driver.close()

    return email


# Get the list of names and addresses of schools
schools = pd.read_csv("input/schools-input.csv")
# Add email to dataframe by scrapping
schools['email'] = schools.apply(lambda row: findEmail(row['NAME'], row['ADDRESS']), axis=1)
# Export the results as CSV
schools.to_csv('results/schools-results.csv')

# In case the apply() function crashes, you can print the emails and add to CSV manually
'''
for item in emails:
    print(item[0], ';', item[1])
'''
