#!/bin/bash

# URL to fetch (adjust path if needed)
URL="http://script-server/deploy.sh"

# Local filename
FILE="deploy2.sh"

# Download the script
curl -fsSL "$URL" -o "$FILE" || {
    echo "Download failed"
    exit 1
}

# Make it executable
chmod +x "$FILE"

# Run it
./"$FILE"