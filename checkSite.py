import os
import sys
import json
import time

# Settings #
container_path = '/'.join(os.path.realpath(__file__).split('/')[:-1]) + '/'
jsonFile_PATH = container_path + "record.json"
logFile_PATH = container_path + "siteCheck.log"

'''
	JSON structure:
	{websiteName:{'checks':100, 'up':97}}
'''

# Get Website Input #
if len(sys.argv) > 1:
	url = sys.argv[1]
else:
	quit("###ERROR: No url input was given.")

# Get Website Response #
command = f"ping {url} -c 1"
output = os.popen(command).read()

if "packets transmitted, " in output and "packets received, " in output:
	siteIsUp = True
else:
	siteIsUp = False

# Handle Output #
# Update Log File #
with open(logFile_PATH, 'a+') as logFile:
	current_time = time.strftime('%x - %X')
	if siteIsUp:
		logFile.write(f"\n{current_time} | {url} | online")
	else:
		logFile.write(f"\n{current_time} | {url} | NOT DETECTED / OFFLINE")

# Download Json Count File Data #
with open(jsonFile_PATH) as jsonFile:
	DATA = json.load(jsonFile)

# Update Data #
if url in DATA:
	DATA[url]["checks"] += 1
	if siteIsUp:
		DATA[url]["up"] += 1

else:
	DATA[url] = {"checks": 1}
	if siteIsUp:
		DATA[url]["up"] = 1

# Save Updated Data #
print(DATA)
with open(jsonFile_PATH, 'w') as jsonFile:
	json.dump(DATA, jsonFile)
