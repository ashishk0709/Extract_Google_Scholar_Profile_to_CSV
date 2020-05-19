# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:01:07 2020

@author: Ashish Kumar
"""

import json
import pandas as pd
import time
chromePath = ".\chromedriver.exe"  #path to chromedriver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True

driver = webdriver.Chrome(options=options, executable_path=chromePath)

# enter url of the google scholar profile
GS_url = 'https://scholar.google.com/citations?user=*********&hl=en'

tt = time.time()
driver.get(GS_url)

while True:
    button = driver.find_element_by_id('gsc_bpf_more')
    print("Expanding the page")
    button.click()
    time.sleep(1)
    if (not button.is_enabled()):
        break
        
all_papers_class = driver.find_elements_by_class_name("gsc_a_at")
all_citations_class = driver.find_elements_by_class_name("gsc_a_ac")
all_papers_tr = driver.find_elements_by_xpath("//tr[@class='gsc_a_tr']")
all_papers_td = driver.find_elements_by_xpath("//tr[@class='gsc_a_tr']/td")
n_papers = len(all_papers_class)

profile_data = {}
all_papers_data = []
for i in range(n_papers):
    print("paper = ",i+1," out of ",n_papers)
    pi_dict_name = 'pi'+'{:05d}'.format(i)
    pi_class = all_papers_class[i]
    pi_authors = all_papers_tr[i].find_elements_by_xpath(".//div[@class='gs_gray']")[0].text
    pi_year = all_papers_tr[i].find_elements_by_class_name("gsc_a_y")[0].text
    pi_citations = all_papers_tr[i].find_elements_by_class_name("gsc_a_c")[0].text
    pi_name = all_papers_tr[i].find_elements_by_class_name("gsc_a_at")[0].text
    print(pi_name)
    print("Total citations = ",pi_citations,'\n')
    pi_link = all_citations_class[i].get_attribute('href')
    
#    generating output data for csv file
    pi_data = (pi_name,pi_authors,pi_year,pi_citations,pi_link)
    profile_data[pi_dict_name] = {}
    profile_data[pi_dict_name]['title'] = pi_name
    profile_data[pi_dict_name]['authors'] = pi_authors
    profile_data[pi_dict_name]['year'] = pi_year
    profile_data[pi_dict_name]['totalCitations'] = pi_citations
    profile_data[pi_dict_name]['link'] = pi_link

    all_papers_data.append(pi_data)

df = pd.DataFrame(all_papers_data,columns=['title','authors','year','citations','link'])
df.to_csv('allPapers.csv',index = False)
driver.close()

elapsed = (time.time() - tt)/60
print("Finished in ",round(elapsed,3), " Minutes....")

json = json.dumps(profile_data)
f = open("profile_data.json","w")
f.write(json)
f.close()
print("profile_data written to the json file")