#########################################################
# This was written on a mac, so if you're  using        #
# windows, change the file path from / to \ before use  #
#########################################################

import pandas as pd
from csv import reader
import os
import requests
import base64

cwd = os.getcwd()

########################
#  GOOGLE SHEET INFO   #
########################
"""
googleSheetID grabbed from a viewable google sheets link
countingData is the sheet name
tradeData is the holder for the data from the google sheet
"""
googleSheetId = '1gNV2HlwGg3Kn9orj4EMYLLarTb1kZjH6PXrTu6wb3Ug'
countingData = 'Counting'

tradeData = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
	googleSheetId,
	countingData
)

########################
#    CSV OF VALUES     #
########################
"""
itemData is the raw data pulled from the google sheet
petPageData is the item name and it's assigned value
"""
itemData = pd.read_csv(tradeData, sep=",")
petPageData = itemData[["Item", "last Owls value"]]
petPageData.to_csv(os.path.join(cwd, "valuecsv.csv"), sep='\t', encoding='utf-8')

########################
#   PET PAGE STUFF     #
########################
"""
petPageCSS is the start of the pet page code that includes the CSS and starting blurb 
petPageFooter is the bottom of pet page code
genedCode is the list of items and values made
"""
genedCode = open(os.path.join(cwd, "OWLS PETPAGE COPY.txt"), "w")

petPageCSStxt = "https://raw.githubusercontent.com/kayereeves/owls-petpage-code/main/topOfPetPage.txt"
petPageCSS = requests.get(petPageCSStxt)
petPageCSS = petPageCSS.text

petPageFootertxt = "https://raw.githubusercontent.com/kayereeves/owls-petpage-code/main/endOfPetPage.txt"
petPageFooter = requests.get(petPageFootertxt)
petPageFooter = petPageFooter.text

# css and header to pet page
for line in petPageCSS:
    genedCode.write(line)


# reads csv of item values and puts it into html for pet page
with open(os.path.join(cwd, "valuecsv.csv"), "r") as itemValues:
    csvReader = reader(itemValues)
    for row in csvReader:
        line = row[0].split("\t")
        genedCode.write("<li>" + line[1] + " <strong>~</strong> ")
        if line[2] == "":
            genedCode.write("00 - 00 </li>\n")
        else:
            genedCode.write(line[2] + "</li>\n")


# add the footer
for line in petPageFooter:
    genedCode.write(line)

genedCode.close()

print(cwd)

# fin.