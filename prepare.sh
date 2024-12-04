#!/bin/bash

python3 generate_dirty_data.py

# cleaning
cat ms_data_dirty.csv | grep -v '^#' | grep -v -e '^$' | sed -e 's/,,*/,/g' | cut -d ',' -f1,2,4,5,6 > ms_data.csv

touch insurance.lst # create insurance file

echo -e "insurance_type\nBasic\nPremium\nPlatinum" > insurance.lst # add in different levels of insurance

visits=$(wc -l < ms_data.csv)

echo "Total number of visits: $((visits - 1))" # count visits without header

# show the first records
echo "First 4 records:"
head -n 5 ms_data.csv

chmod +x prepare.sh