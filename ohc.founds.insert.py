#!/usr/bin/env python3

'''
    a pwnagotchi helper script

    this script reads a "onlinehashcrack.cracked" csv file and stores the passwords
    as .pcap.cracked textfile for shown in webgpsmap plugin

     - you need to have the onlinehashcrack plugin enabled and "dashboard" configured
'''

import os
import csv

csvfile = "/root/handshakes/onlinehashcrack.cracked"
handshakesdir = "/root/handshakes"


passwords = dict()

# read csv file
file = open(csvfile, "r")
csv_reader = csv.reader(file, delimiter=",")
for row in csv_reader:
    if len(row) == 6:
        if row[4]:
            passwords[row[2].replace(':','')] = row[4]
file.close()

# read handshakes dir
all_files = os.listdir(handshakesdir)
all_pcap_files = [os.path.join(handshakesdir, filename)
                    for filename in all_files
                    if filename.endswith('.pcap')
                    ]
all_files = [os.path.join(handshakesdir, filename)
                    for filename in all_files
                    ]

# write .cracked files if not exist
for mac in passwords:
    for filename in all_pcap_files:
        if mac in filename:
            filename_cracked = filename + ".cracked"
            if filename_cracked not in all_files:
                print(f"new: {filename_cracked}: {mac}: {passwords[mac]}")
                f = open(filename_cracked, "w+")
                f.write(passwords[mac])
                f.close()
            else:
                print(f"already exist: {filename_cracked}: {mac}: {passwords[mac]}")
