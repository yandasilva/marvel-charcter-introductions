#!/usr/bin/python -tt

#-----------------------------------------------------------------------------------------
#Developed by Yan Ramos da Silva (yandasilva.com)
#Plots a graph showing the number of characters introduced by Marvel since Timely Comics
#foundation in 1939, also comparing the number of mutant and inhuman characters introduced
#as well
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#Imports
#-----------------------------------------------------------------------------------------
import pandas as pnd
import requests, datetime
import matplotlib.pyplot as plt


#-----------------------------------------------------------------------------------------
#Creates a list from the articles on a Marvel Wikia category
#-----------------------------------------------------------------------------------------
def create_list_from_category(url):
  try:
    #Requests JSON from URL
    r = requests.get(url)
    response = r.json()
    #Returns every item (page title) that is a character (not a Category)
    return [item['title'] for item in response['items'] if not 'Category' in item['url']]
    
  #Exception handler
  except Exception as exc:
    print str(exc)
    return None      
    
#-----------------------------------------------------------------------------------------
#Writes dataframe info to disk
#-----------------------------------------------------------------------------------------
def write_data_file(df):
  
  #Opens file; creates it if it doesn't exist
  f = open('Character Debuts.txt', 'w')
  #Writes statistical data of the dataframe to the file
  f.write(str(df.describe()))
  f.write('\n\n')
  
  #Changes pandas display option to allow it to print the entire dataset
  pnd.set_option('display.max_rows', 100)

  #Writes each column sorted sorted by descending order
  f.write(str(df.sort_values('New characters', ascending=False)['New characters']))
  f.write('\n\n')
  f.write(str(df.sort_values('Mutants', ascending=False)['Mutants']))
  f.write('\n\n')
  f.write(str(df.sort_values('Inhumans', ascending=False)['Inhumans']))
  f.write('\n\n')
  
  #Closes file
  f.close()
  
#-----------------------------------------------------------------------------------------
#Scrapes marvel.wikia.com pages and saves data to a .csv file
#-----------------------------------------------------------------------------------------
def scrape_data():

  #Sets the Wikia API URL for the list of articles on the desired categories
  debuts_url = 'http://marvel.wikia.com/api/v1/Articles/List?category='
  mutants_url = 'http://marvel.wikia.com/api/v1/Articles/List?category=Mutants_(Homo_superior)&limit=10000'
  inhumans_url = 'http://marvel.wikia.com/api/v1/Articles/List?category=Inhumans_(Inhomo_supremis)&limit=10000'
  
  #Gets current year
  first_year = 1939
  now = datetime.datetime.now()
  
  #Creates data structures
  debuts = dict()
  mutant_debuts = dict()
  inhuman_debuts = dict()
  mutants_list = create_list_from_category(mutants_url)
  inhumans_list = create_list_from_category(inhumans_url)

  
  try:
    #For each year since the creation of Marvel:
    for year in range(first_year, now.year + 1):
      #Requests data for character debuts on that year
      r = requests.get(debuts_url + str(year) + '_Character_Debuts&limit=10000')
      response = r.json()
      
      #Adds number of character, Inhumans and Mutants debuts to respective dicts
      mutants = 0
      inhumans = 0
      others = 0
      for character in response['items']:
        name = character['title']
        if name in mutants_list:
          mutants += 1
        elif name in inhumans_list:
          inhumans += 1
        else:
          others += 1
        mutant_debuts[year] = mutants
        inhuman_debuts[year] = inhumans
        debuts[year] = mutants + inhumans + others
        
  
  #Exception handler
  except Exception as exc:
    print str(exc)
    pass
    
  #Concatenates all scraped data in a single dataframe
  total_df = pnd.DataFrame.from_dict(debuts, orient='index')
  total_df.columns = ['New characters']
  mutants_df = pnd.DataFrame.from_dict(mutant_debuts, orient='index')
  mutants_df.columns = ['Mutants']
  inhumans_df = pnd.DataFrame.from_dict(inhuman_debuts, orient='index')
  inhumans_df.columns = ['Inhumans']
  dataframe = pnd.concat([total_df, mutants_df, inhumans_df], axis=1)
  return dataframe
  
#-----------------------------------------------------------------------------------------
#Main function
#----------------------------------------------------------------------------------------- 
def main():

  #Creates pandas dataframe by scraping data from marvel.wikia.com
  dataframe = scrape_data()
  
  #Writes data to a .txt file
  write_data_file(dataframe)
  
  #Plots the graph
  dataframe.plot(figsize=(16, 9))
  #Draws relevant vertical lines and labels
  plt.axvline(1954, color='b', linestyle='dashed', linewidth=2)
  plt.text(1954,2070, 'Comics Code Authority', color='b', horizontalalignment='center')
  plt.axvline(1965, color='r', linestyle='dashed', linewidth=2)
  plt.text(1965,2120, 'Inhumans are introduced', color='r', horizontalalignment='center')
  plt.axvline(1995, color='g', linestyle='dashed', linewidth=2)
  plt.text(1995,2020, 'Age of Apocalypse', color='g', horizontalalignment='center')
  plt.axvline(1982, color='b', linestyle='dashed', linewidth=2)
  plt.text(1982,2070, 'Marvel Graphic Novels', color='b', horizontalalignment='center')
  plt.axvline(2014, color='r', linestyle='dashed', linewidth=2)
  plt.text(2014,2120, 'Inhumanty: \nThe Awakening', color='r', horizontalalignment='center')
  plt.axvline(2009, color='b', linestyle='dashed', linewidth=2)
  plt.text(2009,2070, 'Disney buys Marvel', color='b', horizontalalignment='center')
  plt.axvline(2005, color='g', linestyle='dashed', linewidth=2)
  plt.text(2005,2020, 'House of M', color='g', horizontalalignment='center')
  #Saves graph as a .png image
  plt.savefig('Character Debuts.png')
  
#-----------------------------------------------------------------------------------------
#Main function call
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
  main()
  
  