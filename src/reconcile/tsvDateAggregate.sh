#!/bin/sh --

if [[ $# != 3 ]]; then
  exit
fi

# Columns 1-10 give the date (YYYY-MM-DD) without the time
for i in $*; do
    type=$(sed 's/^.*[0-9]-\(.*\)\.tsv/\1/' <<< ${i})
    cut -c1-10 ${i} | uniq -c | awk 'BEGIN{OFS="\t"}{print $2,$1}' > dates_${type}.tsv
done

wc -l dates_*.tsv

# get unique dates found in each file with "0" data as TSV
cut -d$'\t' -f1 dates_*.tsv | sort -u | sed 's/$/\t0/' > dates_all.tsv

wc -l dates_all.tsv

# add "0" to files that are missing dates
for i in dates_[mu]*.tsv; do
    name=$(basename $i .tsv)
    join -a1 -t$'\t' -e0 -o 0,2.2 dates_all.tsv $i > ${name}_withZeroes.tsv
done

wc -l dates_*_withZeroes.tsv

join -t$'\t' dates_missing_withZeroes.tsv dates_matching_withZeroes.tsv | \
    join -t$'\t' - dates_unlogged_withZeroes.tsv > dates_missing_matching_unlogged.tsv

wc -l dates_missing_matching_unlogged.tsv
