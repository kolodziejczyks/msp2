#!/bin/bash

cd /Users/szymonkolodziejczyk/code/msp2

JSON_FILE="credentials.json"

echo "Processing credentials from $JSON_FILE..."

# Extract values and store in temporary files
grep '"username"' "$JSON_FILE" | sed 's/.*"username": *"\([^"]*\)".*/\1/' > /tmp/usernames.txt
grep '"password"' "$JSON_FILE" | sed 's/.*"password": *"\([^"]*\)".*/\1/' > /tmp/passwords.txt
grep '"destinationLogin"' "$JSON_FILE" | sed 's/.*"destinationLogin": *"\([^"]*\)".*/\1/' > /tmp/destinations.txt

# Count lines to know how many credentials we have
NUM_CREDS=$(wc -l < /tmp/usernames.txt)
echo "Found $NUM_CREDS credentials to process..."

# Process each credential
for i in $(seq 1 $NUM_CREDS); do
    USERNAME=$(sed -n "${i}p" /tmp/usernames.txt)
    PASSWORD=$(sed -n "${i}p" /tmp/passwords.txt)
    DESTINATION_LOGIN=$(sed -n "${i}p" /tmp/destinations.txt)
    
    echo "Processing credential $i/$NUM_CREDS: $USERNAME"
    echo "Running: python3 graf.py $USERNAME $PASSWORD $DESTINATION_LOGIN"
    
    # Run your Python script
    python3 graf.py $USERNAME $PASSWORD $DESTINATION_LOGIN
    
    echo "----------------------------------------"
done

# Clean up temporary files
rm -f /tmp/usernames.txt /tmp/passwords.txt /tmp/destinations.txt

echo "All credentials processed!"