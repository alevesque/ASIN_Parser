#ASIN_Parser

#1. User gives Merchant ID
#2. Download webpage of listings
#3. Get first set of ASINs and number of pages of listings for that merchant
#4. Cycle though the rest of the pages and take their ASINs


import re
import urllib.request
import argparse
import time

#webpage_dl - takes url details and downloads the webpage
#then passes it to asin_parse to analyze
def webpage_dl(url,merchantID_url_tag,merchantID):
    webpage = urllib.request.urlopen(url+merchantID_url_tag+merchantID)
    webContent = webpage.read().decode('utf-8')
    pageCount = asin_parse(webContent,merchantID)
    return(pageCount)

#asin_parse - takes in webpage, spits out ASINs
def asin_parse(webContent,merchantID):

    #open and append to ASIN list file
    filename = 'ASIN_List_'+merchantID
    f = open(filename + ".txt", 'a')

    #find all asin numbers listed on webpage
    asin_pattern1 = 'asin\=\"\w\w\w\w\w\w\w\w\w\w'
    asin_pattern2 = '\w\w\w\w\w\w\w\w\w\w'

    #search downloaded webpage for ASIN tag
    asin_list = re.findall(asin_pattern1,webContent)

    #write each asin to file, removing the "asin=" part
    #of the string from previous regex, using the 2nd pattern
    if asin_list != []:
        for i in asin_list:
            f.write(re.findall(asin_pattern2,i)[0]+'\n')
    else:
        print('Failed to find ASIN!\n')
        return(-1)

    #close file
    f.close

    #find number of seller pages for later iterating download
    page_count_pattern1 = 'a\-disabled\"\>\d\d'
    page_count_pattern2 = '\d\d'
    page_count2 = []

    #filter webpage text by regexes to find number of seller pages
    page_count1 = re.findall(page_count_pattern1,webContent)
    if page_count1 != []:
        for j in page_count1:
            page_count2.extend(re.findall(page_count_pattern2,j))
        return(page_count2[0])
    else:
        print('Failed to find Page Count!\n')
        return(-1)

def main():
    #take in merchant ID as command line argument
    arg_parser = argparse.ArgumentParser(description='List all ASINs from Amazon Seller')
    arg_parser.add_argument("-m",type=str,help="Amazon Merchant ID #",required=True)
    args = arg_parser.parse_args()

    #merchantID is carried throughout functions because needed for naming file
    merchantID = args.m

    #initial page download writes first page of ASINs and retrieves page count
    url = 'https://www.amazon.com/s?'
    merchantID_url_tag='&merchant='

    #call webpage_dl with url to retrieve page count
    pageCount = webpage_dl(url,merchantID_url_tag,merchantID)
    if (int(pageCount) < 0):
        return(-1)

    #now iterate through all the seller's pages
    for i in range(2, int(pageCount)):
        webpage_dl(url+'&page='+str(i),merchantID_url_tag,merchantID)
        #have to wait or amazon cuts you off mid-run
        time.sleep(1)

    print('Operation Success!\n')
main()
