#!/usr/bin/env perl 
#===============================================================================
#
#         FILE: syn.pl
#
#        USAGE: ./syn.pl  
#
#  DESCRIPTION: synthesis from mgc and lf0
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Dylan, 
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 2016年04月28日 17时46分13秒
#     REVISION: ---
#===============================================================================
require($ARGV[0]);

$base= $ARGV[1];
$gendir=".";

print " Synthesizing a speech waveform from $base.mgc and $base.lf0...";
$lf0="$base.lf0";
$mgc="$base.mgc";

# convert log F0 to pitch
$line = "$SOPR -magic -1.0E+10 -EXP -INV -m $sr -MAGIC 0.0 $lf0 > $gendir/${base}.pit";
system($line);

# synthesize waveform
$lfil = `$PERL scripts/makefilter.pl $sr 0`;
$hfil = `$PERL scripts/makefilter.pl $sr 1`;

$line = "$SOPR -m 0 $gendir/$base.pit | $EXCITE -n -p $fs | $DFS -b $hfil > $gendir/$base.unv";
system($line);

$line = "$EXCITE -n -p $fs $gendir/$base.pit | ";
$line .= "$DFS -b $lfil | $VOPR -a $gendir/$base.unv | ";
$line .= "$MGLSADF -P 5 -m " . ( $ordr{'mgc'} - 1 ) . " -p $fs -a $fw -c $gm $mgc | ";
$line .= "$X2X +fs -o > $gendir/$base.raw";
system($line);
$line = "$RAW2WAV -s " . ( $sr / 1000 ) . " -d $gendir $gendir/$base.raw";
system($line);

$line = "rm -f $gendir/$base.unv";
system($line);

print "done\n";

