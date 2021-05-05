#!/bin/bash

#you can read the frequency limits using the command cpufreq-info
min=500
max=2100
cpufreqGovernors=('performance' 'powersave')

echo ${cpufreqGovernors[0]}

#check if script is executed as with root privileges
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Please run script with root privileges"
    echo "Exiting ..."
    exit
fi


echo "Please enter new minimal frequency in MHz (hardware limit is ${min})"
read enteredMin

if [ $enteredMin -lt $min ]; then
	echo "Minimum lower than $min."
	echo "Exiting ..."
	exit
fi

echo "Please enter new maximal frequency in MHz (hardware limit is ${max})"
read enteredMax

if [ $enteredMax -gt $max ]; then
	echo "Maximum higher than $max."
	echo "Exiting ..."
	exit
fi

#echo "min: $enteredMin, max: $enteredMax"

/usr/bin/cpufreq-set -c 0 --min "${enteredMin}MHz" --max "${enteredMax}MHz"
/usr/bin/cpufreq-set -c 1 --min "${enteredMin}MHz" --max "${enteredMax}MHz"
/usr/bin/cpufreq-set -c 2 --min "${enteredMin}MHz" --max "${enteredMax}MHz"
/usr/bin/cpufreq-set -c 3 --min "${enteredMin}MHz" --max "${enteredMax}MHz"


echo "Please choose a cpufreq governor (available: performance, powersave)"
read enteredGovernor


