#!/usr/local/bin/perl
# task1.pl

use strict;
use warnings;
use LWP::Simple;
use XML::Simple;

my $ncbi_euk_text = get "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/eukaryotes.txt";
my $ncbi_prok_text = get "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt";
my $inparanoid_xml = get "http://inparanoid.sbc.su.se/download/7.0_current/sequences/species.xml";

my @ncbi_organisms = ();
my @inparanoid_organisms = ();

my @ncbi_eukaryote_text = split(/\n/, $ncbi_euk_text);
my @ncbi_prokaryote_text = split(/\n/, $ncbi_prok_text);

my %species_hash = ();
# add each organism on NCBI to @ncbi_organisms, only once.
# each organism has the form gspecies. Where g is the first letter of the Genus.
foreach my $line (@ncbi_eukaryote_text)
{
    #print "line = $line\n";    
    $line =~ /\A(\w+) (\w+)/; #match the first two words of the line
    #print "line = $line\n";
    my $genus = $1; #first word is genus
    my $species = $2; #2nd word is species
    #print "genus = $genus\n";
    #print "species = $species\n";
    my $full_name = join(' ', $genus, $species);
    $genus = substr($genus,0, 1); #get first letter of genus
    $genus =~ tr/[A-Z]/[a-z]/; #turn first letter to lower case
    my $organism = $genus . $species; # concatenate the genus  now one letter to the species.
    #print "organism  = $organism \n";    
    if (seen_before($organism, @ncbi_organisms)){
        next;
    }
    else{
        push (@ncbi_organisms, $organism);
        $species_hash{$organism} = $full_name;
        #add it to the ncbi_organisms array unless it is already there
    }
}

foreach my $line (@ncbi_prokaryote_text)
{
    #print "line = $line\n";    
    $line =~ /\A(\w+) (\w+)/; #match the first two words of the line
    #print "line = $line\n";
    my $genus = $1; #first word is genus
    my $species = $2; #2nd word is species
    #print "genus = $genus\n";
    #print "species = $species\n";
    my $full_name = join(' ', $genus, $species);
    $genus = substr($genus,0, 1); #get first letter of genus
    $genus =~ tr/[A-Z]/[a-z]/; #turn first letter to lower case
    my $organism = $genus . $species; # concatenate the genus  now one letter to the species.
    #print "organism  = $organism \n";    
    if (seen_before($organism, @ncbi_organisms)){
        next;
    }
    else{
        push (@ncbi_organisms, $organism);
        $species_hash{$organism} = $full_name;
        #add it to the ncbi_organisms array unless it is already there
    }
}

# Get the XML file format.
my $xml = new XML::Simple (KeyAttr=>[]);
my $inparanoid_data =$xml->XMLin($inparanoid_xml);

foreach my $species_listing (@{$inparanoid_data->{species}}) #iterate through each species
{
    my $inparanoid_org = $species_listing->{ identifier};  #get the identifier
    #print "$inparanoid_org\n";
    $inparanoid_org =~ tr/[A-Z]/[a-z]/; #turn first letter to small letter
    #print "$inparanoid_org\n";
    $inparanoid_org =~ s/\Q.\E//; 
    #print "$inparanoid_org\n";
    push (@inparanoid_organisms, $inparanoid_org)
        unless seen_before($inparanoid_org, @inparanoid_organisms);
}    

# make array of overlapping species.
my @overlapping_species = ();

foreach my $ncbi_species (@ncbi_organisms)
{
    if (seen_before($ncbi_species, @inparanoid_organisms)){
        push (@overlapping_species, $ncbi_species);
    }
        # add the species to the array if seen before.
    else{
        next;
    }
}

print "Overlapping species:\n";
foreach my $overlapped (@overlapping_species){
    my $full_name = $species_hash{$overlapped};
    print "$full_name\n";
}

my $size = @overlapping_species;
print "Total Overlapping species:  $size\n";



######### Subroutine

# seen_before: Given a scalar and an array, return 1 if the
# scalar is in the array and 0 if it is not.
sub seen_before{
    my $needle = shift;
    my @haystack = @_;
    foreach my $elem (@haystack) {
        return 1 if $needle eq $elem;
    }
    return 0;
}

