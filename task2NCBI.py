#!usr/bin/python
# task 2: NCBI script
###### GENOME LOCATIONS ######

import urllib


def main ():

    print 'Genome Locations:'

    # keeps count how many possible species
    count = 0

    
    fileIn = open ("task1.txt", "r")    # open file from task 1
    name = fileIn.readline ()  # read genus and species name

    # according to output of task 1
    if (name == 'Overlapping species:\n'):
        name = fileIn.readline ()


    while name: # continue reading until end of file
        
        names = name.split (" ")    # split genus from species

        # marks the end of file 'Total Overlapping Species: (number of species)'
        # according to output of task 1
        if (names [0] == 'Total'):
            break


        genus = names [0]   # first word is genus
        species = names [1] # second word is species

        # each species name has end terminator '\n'
        # e.g. 'sapiens\n'
        species = species [: len(species) - 1]

        link = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/MapView/%s_%s/sequence' % (genus, species)


        # if the link exists
        # loop exits if website cannot be opened
        try:
            openWebsite = urllib.urlopen (link)  # try opening website

            readWebsite = openWebsite.readline ()    # read each line from website
            words = readWebsite.split (' ')


            # getting the highest BUILD #
            # second last line displays most current (and highest) BUILD #
            while 'current' not in words:
                readWebsite = openWebsite.readline ()
                words = readWebsite.split (' ')  # break down into 'words'

            buildNumber = words [ len (words) - 1]


            # each buildNumber has end terminators '\r\n'
            # e.g. 'BUILD.1.1\r\n'
            buildNumber = buildNumber [: len (buildNumber) - 2]


            # print '%s %s %s' % (genus, species, buildNumber)
            # extend link to include buildNumber
            link = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/MapView/%s_%s/sequence/%s/initial_release/seq_gene.md.gz' % (genus, species, buildNumber)
            print link
            
            # increase number of possible genome locations
            count = count + 1
            

        # if the link does not exist, do nothing
        except:
            # print '%s %s' % (genus, species)
            name = fileIn.readline ()   # read next line
            continue


        name = fileIn.readline ()   # read next line

                       
    fileIn.close()    # close inputted file
    
    print 'Total Number of Genome Locations: %d' % (count)

main()

'''
For writing text into given files:

            openFile = urllib.urlopen(link) # opens NCBI link
            readFile = openFile.read()  # reads link

            # create new file with the genus and species name
            file = open('%s %s' % (genus, species), "wb")

            # place genome info from NCBI link into this file
            file.write(readFile)
            file.close()
'''
