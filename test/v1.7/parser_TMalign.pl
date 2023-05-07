#!/usr/bin/perl -w

use strict;

my $file = shift @ARGV;
open(FILE, "< $file") or die;
#my $proteinA = substr($file, 0, 7);
#my $proteinB = substr($file, 8, 7);
#my ($proteinA, $proteinB, @file) = split(/_\._/, $file, 3);
my $proteinA;
my $proteinB;
#$proteinB =~ s/\.ent//;
#my ($finalScore, $coverage, $rmsd, $gaps, $finalScoreNorm) = ("") x 5;
my @features = ("") x 5;
# Aligned length
# RMSD
# n_identical/n_aligned
# TM-score (chain 2)
# d0 (chain 2)
while(my $line = <FILE>){
	chomp $line;
	if($line =~ m/^Name of Chain_1:/){
		$line = substr($line, 17, -34);
		my @line = split("/", $line);
		$proteinA = $line[$#line];
	} elsif($line =~ m/^Name of Chain_2:/){
                $line = substr($line, 17);
                my @line = split("/", $line);
                $proteinB = $line[$#line];
		$proteinB =~ s/\.ent\.pdb//;
	} elsif ($line =~ m/^Aligned length/){
		my @line = split(/[ ,]+/, $line);
		$features[0] = $line[2];
		$features[1] = $line[4];
		$features[2] = $line[6];
		#print $finalScore."\n";		
	} elsif ($line =~ m/^Length of Chain_2:/){
		my @line = split(/[ ]+/, $line);
		$features[5] = $line[3];
		#print $finalScore."\n";		
	} elsif ($line =~ m/^TM-score=/ and $line =~ m/Chain_2/){
		my @line = split(/[ ]+/, $line);
		$features[3] = $line[1];
		$features[4] = $line[10];
		$features[4] =~ s/d0=//;
		$features[4] =~ s/\)//;
		last;
	}
}

$features[5] = sprintf("%.4f",$features[0]/$features[5]);
print $proteinA."\t".$proteinB."\t".join("\t", @features)."\n";
#print $proteinA."\t".$proteinB."\t".$finalScore."\t".$coverage."\t".$rmsd."\t".$gaps."\t".$finalScoreNorm."\n";
