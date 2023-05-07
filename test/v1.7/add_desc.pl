#!/usr/bin/perl -w

use strict;

my $resultFile = shift @ARGV;
my $desFile = shift @ARGV;
my $claFile = shift @ARGV;

open(RES, "< $resultFile") or die;
my %dm;

while(my $line = <RES>){
	chomp $line;
	my @line = split(",", $line);
	$dm{$line[1]} = 1;
	#print $line[0].",".$line[1].",".$des{$cla{$line[1]}{"sf"}}.",".$line[34].",".$line[35]."\n";
}

close RES;

open(CLA, "< $claFile") or die;
my %cla;
while(my $line = <CLA>){
	next if ($line =~ /^#/);
	chomp $line;
	my @line = split("	", $line);
	if(exists $dm{$line[0]}){
		my @class = split(",", $line[5]);
		#$cla{$line[0]}{"fa"} = $class[3];
		#$cla{$line[0]}{"sf"} = $class[2];
		#$cla{$line[0]}{"fo"} = $class[1];
		$cla{$class[2]} = 1;
		$dm{$line[0]} = $class[2];
	}
	
}
$dm{"subject"} = "subject";

close CLA;

open(DES, "< $desFile") or die;

#dir.des.scope.txt
#46456   cl      a       -       All alpha proteins
#46457   cf      a.1     -       Globin-like
#46458   sf      a.1.1   -       Globin-like
#46459   fa      a.1.1.1 -       Truncated hemoglobin
#46460   dm      a.1.1.1 -       Protozoan/bacterial hemoglobin
#116748  sp      a.1.1.1 -       Bacillus subtilis [TaxId: 1423]
#113449  px      a.1.1.1 d1ux8a_ 1ux8 A:
#46461   sp      a.1.1.1 -       Ciliate (Paramecium caudatum) [TaxId: 5885]
#14982   px      a.1.1.1 d1dlwa_ 1dlw A:

my %des;

while(my $line = <DES>){
	next if ($line =~ /^#/);
	chomp $line;
	my @line = split("	", $line);
	if(exists $cla{$line[1]."=".$line[0]}){
		$cla{$line[1]."=".$line[0]} = $line[2]." ".$line[4]
	}
	#$des{$line[1]."=".$line[0]} = $line[2]." ".$line[4];
}
$cla{"subject"} = "superfamily";

close DES;

open(RES, "< $resultFile") or die;

while(my $line = <RES>){
	chomp $line;
	next if($line =~ /^$/);
	my @line = split(",", $line);
	print $line[0]."\t".$line[1]."\t".$cla{$dm{$line[1]}}."\t".$line[$#line-1]."\t".$line[$#line]."\n";
}

close RES;

