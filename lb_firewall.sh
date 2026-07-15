#!/bin/bash

# Flush existing rules
iptables -F
iptables -X

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback interface
iptables -A INPUT -i lo -j ACCEPT

# Allow established and related connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH from anywhere
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP from anywhere
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Allow HTTPS from anywhere
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Optional: allow ICMP (ping)
iptables -A INPUT -p icmp -j ACCEPT

# Log dropped packets (optional)
iptables -A INPUT -j LOG --log-prefix "Dropped: "

# Drop everything else
iptables -A INPUT -j DROP
