#!/usr/bin/perl -w

use strict;

my $file = shift @ARGV;
open(FILE, "< $file") or die;

my $proteinA; my $proteinB;

my ($finalScore, $coverage, $rmsd, $gaps, $finalScoreNorm) = ("") x 5;
my ($lenA, $lenB) = ("") x 2;

while(my $line = <FILE>){
	
	if($line =~ m/^  FINAL SCORE/){
		chomp $line;
		my @line = split(/[ ]+/, $line);
		$finalScore = $line[3];
		$coverage = $line[5];
		$rmsd = $line[7];
		$gaps = $line[9];
		#print $finalScore."\n";		
	} elsif ($line =~ m/^  Final score/){
		chomp $line;
		my @line = split(/[ ]+/, $line);
		$finalScoreNorm = $line[7];
		last;
	} elsif ($line =~ m/^  Protein A:/){
		chomp $line;
		my @line = split(/[ ]+/, $line);
		$proteinA = $line[3];
		#$proteinA =~ s/\.ent\.pdb$//;
	} elsif ($line =~ m/^  Protein B:/){
		chomp $line;
		my @line = split(/[ ]+/, $line);
		$proteinB = $line[3];
		$proteinB =~ s/\.ent\.pdb$//;
	} elsif ($line =~ m/^  Number of atoms:/){
		chomp $line;
		my @line = split(/[ ]+/, $line);
		$lenA = $line[5];
		$lenB = $line[7];
	}
}

if ($finalScore eq ""){
	exit;
}
my $relCov;
$relCov = sprintf("%.4f", $coverage/$lenB) if ($lenB > 0);
my $relGaps;
$relGaps = sprintf("%.4f", $gaps/$coverage) if ($coverage > 0);
print $proteinA."\t".$proteinB."\t".$finalScore."\t".$coverage."\t".$rmsd."\t".$gaps."\t".$relCov."\t".$relGaps."\t".$finalScoreNorm."\n";
