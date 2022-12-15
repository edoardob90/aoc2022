#!/bin/bash

day=${1:-$(date +%-d)}
year=${2:-$(date +%Y)}

title=$(curl -s "https://adventofcode.com/$year/day/$day" | grep -o "<h2>.*</h2>" | sed -E "s/<h2>--- Day.*: (.*) ---<\/h2>/\1/g")
echo "$day - [$title](https://adventofcode.com/$year/day/$day) | ⭕⭕ | - " >> README.md
