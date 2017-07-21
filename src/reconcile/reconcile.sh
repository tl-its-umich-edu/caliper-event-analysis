#!/bin/sh --

BASE_FILENAME="reconcile-$$"

echo "Log data: ${1}"
sort -c ${1}
if [[ $? != 0 ]]; then
  echo "Error: ${1} is not sorted"
  exit 1
fi

echo "Event data: ${2}"
sort -c ${2}
if [[ $? != 0 ]]; then
  echo "Error: ${2} is not sorted"
  exit 1
fi

echo
echo "Input line counts:"
wc -l ${1} ${2}

echo
echo "Output files: ${BASE_FILENAME}*"

echo
echo "Reconciling input data..."

comm -23 $1 $2 > ${BASE_FILENAME}-missing.tsv

echo
echo "Missing events output complete:"
ls -lF ${BASE_FILENAME}-missing.tsv

comm -13 $1 $2 > ${BASE_FILENAME}-unlogged.tsv

echo
echo "Unlogged events output complete:"
ls -lF ${BASE_FILENAME}-unlogged.tsv

comm -12 $1 $2 > ${BASE_FILENAME}-matching.tsv

echo
echo "Matching events output complete:"
ls -lF ${BASE_FILENAME}-matching.tsv

echo
echo "Output line counts:"
wc -l ${BASE_FILENAME}-*.tsv
