#!/usr/bin/env bash

# Get the tools
source ./scan.lib

# Setting up
PATH_TO_DIRSEARCH="dirsearch"

getopts "m:" OPTION
MODE=$OPTARG
for i in "${@:$OPTIND:$#}"
do
	DOMAIN=$i
	DIRECTORY=reports/${DOMAIN}_recon
	printf "[+] Creating recon directory $DIRECTORY for reports.\n"
	mkdir -p "$DIRECTORY"

	case $MODE in
		nmap-only)
			nmap_scan
			;;
		dirsearch-only)
			dirsearch_scan
			;;
		crt-only)
			crt_scan
			;;
		*)
			nmap_scan
			dirsearch_scan
			crt_scan
			;;
	esac

	# Creating the report 
	printf "[+] Generating recon report for $DOMAIN from output files ...\n"
	TODAY=$(date)

	printf "This scan was created on $TODAY \n" > $DIRECTORY/report

	if [ -f $DIRECTORY/nmap ];then
		printf "\nResults for Nmap:\n" >> $DIRECTORY/report
		grep -E "^\s*\S+\s+\S+\s+\S+\s*$" $DIRECTORY/nmap >> $DIRECTORY/report
	fi

	if [ -f $DIRECTORY/dirsearch ];then
		printf "\nResults for Dirsearch:\n" >> $DIRECTORY/report
		cat $DIRECTORY/dirsearch >> $DIRECTORY/report
	fi

	if [ -f $DIRECTORY/crt ];then
		printf "\nResults for crt.sh:\n" >> $DIRECTORY/report
		jq -r ".[] | .name_value" $DIRECTORY/crt >> $DIRECTORY/report
	fi
done

printf "[+] Done."
