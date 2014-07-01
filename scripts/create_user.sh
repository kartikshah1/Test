#!/usr/bin/sh
## Example script to create single account
## TODO: Read from CSV or maybe an entire python based solution
curl -i -X POST http://10.102.56.95:8080/accounts/api/register/ -F"username=saket" \
    -F "first_name=test" -F "last_name=test" -F "password=123123"\
    -F"email=saketkc@gmail.com" --noproxy 10.102.56.95
