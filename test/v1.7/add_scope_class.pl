#!/usr/bin/perl -w

use strict;

my $inFile = shift @ARGV;
my $dirFile = shift @ARGV;

open(DIR, "< $dirFile") or die;
my %dir;
my %class;
while(my $line = <DIR>){
	chomp $line;
	next if ($line =~ /^#/);
	my @line = split("	", $line);
	my @class = split(",", $line[5]);
	$dir{$line[0]} = $class[0];
	$class{$class[0]} += 1;
}
close DIR;

my @class = ("cl=46456", "cl=48724", "cl=51349", "cl=53931", "cl=56572", "cl=56835", "cl=56992");

open(IN, "< $inFile") or die;
while(my $line = <IN>){
	
	chomp $line;
	my @lines = split("	", $line);
	my $subject = $lines[1];
	
	print $line; 
	foreach my $class(@class){
		if ($dir{$subject} eq $class){
			print "\t1";
		} else {
			print "\t0";
		}
	}
	print "\n";
}

