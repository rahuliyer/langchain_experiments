import os

HOMEDIR = os.path.expanduser("~")
OPENAI_API_KEY_FILE = os.path.join(HOMEDIR, ".openai_api_key")
GOOGLE_SEARCH_API_KEY_FILE = os.path.join(HOMEDIR, ".google_search_api_key")
GOOGLE_SEARCH_CSE_ID_FILE = os.path.join(HOMEDIR, ".google_search_cse_id")

API_KEY_FILES = {
    "OPENAI_API_KEY": OPENAI_API_KEY_FILE,
    "GOOGLE_API_KEY": GOOGLE_SEARCH_API_KEY_FILE,
    "GOOGLE_CSE_ID": GOOGLE_SEARCH_CSE_ID_FILE,
}

def load_api_keys():
    for var_name, key_file in API_KEY_FILES.items():
        with open(key_file, "r") as f:
            os.environ[var_name] = f.read().strip()