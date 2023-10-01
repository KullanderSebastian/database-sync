import hashlib
import json

data = {
    "name": "Erik",
    "role": "Employee",
    "phone": "0761340076"
}

new_data = {
    "name": "Erik",
    "role": "Employee",
    "phone": "0761340075"
}

data_json = json.dumps(data, sort_keys=True)
new_data_json = json.dumps(new_data, sort_keys=True)


sha256_hash = hashlib.sha256()
new_sha256_hash = hashlib.sha256()

sha256_hash.update(data_json.encode('utf-8'))
new_sha256_hash.update(new_data_json.encode('utf-8'))

hashed_data = sha256_hash.hexdigest()
new_hashed_data = new_sha256_hash.hexdigest()

if (hashed_data == new_hashed_data):
    print("samma data")
else:
    print("data har ändrats")
