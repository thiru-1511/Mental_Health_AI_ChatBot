import json
from test_pipeline import result

try:
    print("Testing json.dumps on result...")
    s = json.dumps(result)
    print("Success! Length:", len(s))
    if "NaN" in s:
        print("WARNING: 'NaN' found in JSON string!")
except Exception as e:
    print("json.dumps failed:", e)
