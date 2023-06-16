#!/usr/bin/perl -w

#  perl join_table.pl ../SCOP/selected_hits_3_ML_train.tab ../results/lovoalign/parsed_lovoalign.tab > lovoalign_selected_hits_3_ML_train.tab

use strict;

my $file1 = shift @ARGV;
my $file2 = shift @ARGV;

open(my $fh2, "<", $file2) or die "Cannot open file $file2: $!\n";

my %hash;
my ($q, $s, $rest) = ('', '', '');

while (my $line = <$fh2>) {
    chomp $line;
    my @fields = split("	", $line);
    if (scalar @fields >= 3) {
        ($q, $s, $rest) = @fields;
        $hash{"$q.$s"} = $rest;
    }
}

close($fh2);

open(my $fh1, "<", $file1) or die "Cannot open file $file1: $!\n";

while (my $line = <$fh1>) {
    chomp $line;
    my ($q, $s, $rest) = split("	", $line, 3);
    if(exists $hash{"$q.$s"}){
        my $output = join("\t", $q, $s, $hash{"$q.$s"}, $rest);
        $output =~ s/\t$//;  # Remover o último espaço em branco
        print $output . "\n";
    }
}

close($fh1);