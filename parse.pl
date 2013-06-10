#!/usr/bin/perl
#print $ARGV[0], $ARGV[1];
open(PLIK,$ARGV[0]);
$proc = $ARGV[1];

@lista = <PLIK>;

foreach(@lista)
{
#	if($_ =~ /confirms to/)
#	if($_ =~ /delayed/)
	if($_ =~ /^$proc/)
	{
		print $_;
	}
}
