#!/usr/bin/perl -w

#use Data::Dumper;
use strict;

my $fileFATCAT = shift @ARGV;
my $fileMaxScore = shift @ARGV;

#query-len subject-len Twists ini-len ini-rmsd opt-equ opt-rmsd chain-rmsd Score align-len Gaps
#d16vpa_ d2q13a1 311     266     4       200     9.66    212     7.31    28.35  365.52   311     99      0       6

open(MAX, "< $fileMaxScore") or die;

my %max;

while(my $line = <MAX>){
	chomp $line;
	my @line = split(/ +/, $line);
	$line[0] =~ s/\.ent.pdb//;
	$max{$line[0]} = $line[10];
}

close MAX;

open(FILE, "< $fileFATCAT") or die;

while(my $line = <FILE>){
	chomp $line;
	next if ($line =~ /^$/);
	my @line = split(/[ ]+/, $line);
        $line[1] =~ s/\.ent\.pdb$//;
        #$line[0] =~ s/\.ent\.pdb$//;

	#my @line = split("	", $line);

	next if (!exists $max{$line[1]} or $max{$line[1]} == 0);
	my $minScore = $max{$line[1]};
	my $minSize = $line[3];

	# Score relative to the maxScore for subject
	my $relScore = sprintf("%.4f", $line[10]/$max{$line[1]});

	# Subject alignment coverage
	my $relAli = sprintf("%.4f", ($line[11] - $line[12])/$line[3]);

	#my $relScoreMin = sprintf("%.4f", $line[10]/$minScore);
	#my $relAliMin = sprintf("%.4f", ($line[11] - $line[12])/$minSize);
	
	# exclude column query-len 
	print join("\t", @line[0..1])."\t".join("\t", @line[3..12])."\t".$relScore."\t".$relAli."\n";
	#print join("\t", @line[0..12])."\t".$relScore."\t".$relScoreMin."\t".$relAli."\t".$relAliMin."\t".join("\t", @line[13..14])."\n";
	
}




