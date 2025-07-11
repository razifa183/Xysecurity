# Xysecurity
🛡️ XySecurity – Real-Time Packet Analyzer & Intrusion Detection System

XySecurity is a Python-based network security tool that analyzes network traffic in real time, detects anomalies, and alerts users of potential intrusions or suspicious activity. Inspired by tools like Wireshark, XySecurity is lightweight, CLI-based, and customizable for use in academic, research, or enterprise environments.
🎯 Objective
To design a smart and fast packet sniffer and intrusion detection system (IDS) using Python that helps network admins:
    Monitor traffic in real time
    Detect suspicious IPs or patterns
    Analyze packet-level metadata
    Log and classify security threats

⚙️ Features

    🔍 Real-time packet sniffing using scapy
    📦 Analyzes IP, TCP, UDP, ICMP, ARP, HTTP layers
    🚨 Detects common attacks: port scanning, IP spoofing, abnormal traffic
    📊 Logs packet info with timestamps and flags
    🔐 Can be extended with signature-based or ML-based threat detection

🛠️ Tech Stack

    Python
    scapy, socket, os, 
    matplotlib / seaborn (for traffic visualizations)

🔍 Packet Analysis Capabilities
    Packet count by protocol
    Source & destination IP tracking
    Payload length, flags, TTL, etc.
    Detect repeated SYN packets (possible SYN flood)
    Monitor unusual traffic patterns

