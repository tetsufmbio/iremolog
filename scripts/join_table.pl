#!/usr/bin/perl -w

#  perl join_table.pl ../SCOP/selected_hits_3_ML_train.tab ../results/lovoalign/parsed_lovoalign.tab > lovoalign_selected_hits_3_ML_train.tab

use strict;

my $file1 = shift @ARGV;
my $file2 = shift @ARGV;

open(FILE2, "< $file2") or die;

my %hash;
my ($q, $s, $rest);

while(my $line = <FILE2>){
	chomp $line;
	($q, $s, $rest) = split("	", $line, 3);
	$hash{$q.".".$s} = $rest;
}
# verify number of columns
my $restMiss = $rest;
$restMiss =~ s/[^\t]//g;

close(FILE2);

open(FILE1, "< $file1") or die;

while(my $line = <FILE1>){
	chomp $line;
	my ($q, $s, $rest) = split("	", $line, 3);
	#if (!exists $hash{$q.".".$s}){
	#	print $q.".".$s."\n";
	#}
	if(exists $hash{$q.".".$s}){
		print $q."\t".$s."\t".$hash{$q.".".$s}."\t".$rest."\n";
	} else {
		print $q."\t".$s."\t".$restMiss."\t".$rest."\n";
	}
}

close(FILE1)