#!/usr/bin/env python3

'''
    a pwnagotchi helper script

    this script reads a "wpa-sec.founds.potfile" in the same directory as this script and stores the passwords
    in /root/handshakes/ as .pcap.cracked textfile for shown in webgpsmap plugin

     - you need to have the wpa-sec plugin enabled and onle cracked passwords
     - you need the potfile from "Download all founds" button at https://wpa-sec.stanev.org/?my_nets

'''

import os
from re import split

handshakesdir = "/root/handshakes"
potfile = handshakesdir + '/wpa-sec.cracked.potfile'

passwords = dict()


# read potfile
with open(potfile) as f:
    content = f.readlines()
content = [x.strip() for x in content]

# parse potfile
for line in content:
    if line:
        mac, cksm, ssid, password = split(':', line, 3)
        if mac not in passwords:
            passwords[mac] = password

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

