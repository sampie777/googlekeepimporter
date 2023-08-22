# Huawei Notes -> Google Keep

This repo contains Python script to help import notes from an unencrypted Huawei backup database file to your Google Keep account.

1. Fire up a virtual Python3 environment and install the dependencies.
2. Create a `local_secrets.py` file or edit `secrets.py` directly with your values.
3. Run `main.py` to collect the memos from the backup file and upload them to Google Keep.

> Note that the tags/labels are automatically capitalized. 

> Note that you should probably enable some sort of lower security authentication in your account, if you get an endless login waiting loop.

> Note that running the script twice will result in duplicates! There's not check in place to see if an note/memo already exists in Google Keep.