import os

### Add these values to a local file called 'local_secrets.py'. Don't add that file to git.
# Google Keep username
SECRET_USERNAME = None
# Google Keep password
SECRET_PASSWORD = None
# Path to local Memo.db file from your Huawei backup
SECRET_DB_PATH = None
### End of secrets

# This loads the secrets from local_secrets.py if the file exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

local_secrets_path = os.path.join(BASE_DIR, "local_secrets.py")
if os.path.exists(local_secrets_path):
    from local_secrets import *
