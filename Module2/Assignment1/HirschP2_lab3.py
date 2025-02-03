# HirschP2
# Module 2: Assignment 1 -- Python Conditionals and Loops
# CIT 383 | Scripting I
# 2025/01/27

# Data as provided
servers = [
    {'name': 'server1', 'cpu': 85, 'disk': 20, 'reachable': True},
    {'name': 'server2', 'cpu': 70, 'disk': 5, 'reachable': False},
    {'name': 'critical_server', 'cpu': 90, 'disk': 15, 'reachable': True},
    {'name': 'server4', 'cpu': 60, 'disk': 50, 'reachable': True}
]

# CONFIGURATION VALUES
# Values considered by checks preformed, placed at the top for easy reconfiguration given changing needs
CPU_USAGE_THRESHOLD=80  # The minimum acceptable CPU usage before being considered high.  Should be an int 0-100 representing a percentage
DISKSPACE_THRESHOLD=10  # The maximum acceptable available diskspace before being considered low.  Should be an int 0-100 representing a percentage
CRITICAL_SERVER_NAME='critical_server'  # The name of the critical server as reported by the name attribute

# Counts of findings for summary report, all initialized to 0
count_highCPU=0
count_lowDisk=0
count_unreachable=0

# Loop through each server in `servers` and test for each condition considered
# For each condition, if true for the server, produces a relevant error message and increments a counter
for server in servers:
    # Check if server's CPU usage is considered high (as defined by CPU_USAGE_THRESHOLD)
    if server['cpu']>CPU_USAGE_THRESHOLD:
        print('High CPU usage on '+server['name'])
        count_highCPU+=1
        
    # Check if server's remaining disk space is considered low (as defined by DISKSPACE_THRESHOLD)
    if server['disk']<DISKSPACE_THRESHOLD:
        print('Low disk space on '+server['name'])
        count_lowDisk+=1
        
    # Check if the server is reported to be unreachable (reachable attribute == False)
    if server['reachable']==False:
        print('Server '+server['name']+' is unreachable')
        count_unreachable+=1
        
    # Check if the server that has just been evaluated is the critical server (name attribute == CRITICAL_SERVER_NAME)
    #   If it is the critical server, the loop is broken, stopping any further severs from being evaluated.
    #   This check is placed last so that the critical server is included in both logged messages and the summary for all checks.
    if server['name']==CRITICAL_SERVER_NAME:
        print('Critical server found. Stopping checks.')
        break

# Print Summary:
print('\nSummary:')
print('Servers with high CPU: '+str(count_highCPU))
print('Servers with low disk space: '+str(count_lowDisk))
print('Unreachable servers: '+str(count_unreachable))
