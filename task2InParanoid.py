#!/usr/bin/python

# I included a sample input text (took the first 5 overlapping species)
# in case you want to run the script and see how it works

import urllib

def main():
    fileIn = open("input.txt","r")  # opens file of common species for reading
    # we skip the first line: "Overlapping species"
    ## Can get rid of "name =" in following line, to avoid confusion.
    name = fileIn.readline()    # reads output line by line
    name = fileIn.readline()    # reads output line by line

    number = 0  # total number of overlapping species
    
    site = "http://inparanoid.sbc.su.se/download/7.0_current/sqltables/sqltable."
    
    L = []  # list of newly-formatted G.species.fa
    
    while name: # while there's still something to read
        words = name.split (" ")    # split the genus and species
        if words[0] == "Total":
            break
        
        number += 1
        genus = name[0] # first letter of Genus

        species = words[1]  # species name
        species = species[:-1]  # removing last letter of species: "\n"
           
        # changing name to its appropriate format: G.species.fa
        name = genus + "." + species + ".fa\n"

        L.append(name)  # places name into the list at the next position
        name = fileIn.readline()
        
    fileIn.close()
    ## Can we use more descriptive variable names for j and L
    j = 1     # used for naming files
    ## Instead of using number, can use the length of the list L? len()
    for x in xrange(0,number):   # 0 <= x < number        
        for y in xrange(x+1,number): # x+1 <= y < number
            if L[x] < L[y]:
                first = L[x]
                first = first[:-1]  # removing last letter: "\n"
                second = L[y]
                
            else:
                first = L[y]
                first = first[:-1]  # removing last letter: "\n"
                second = L[x]

            link = site + first + "-" + second
            print link

            # used for naming files
            first = first.split(".")
            second = second.split(".")

            openFile = urllib.urlopen(link)
            readFile = openFile.read()

            # creates new file, IP stands for InParanoid
            # the last part contains Gspecies-Gspecies
            file = open("%d IP %s%s-%s%s" % (j,first[0],first[1],second[0],second[1]),"wb")

            # place information from link to this file
            file.write(readFile)
            file.close()

            j += 1
            
main()
