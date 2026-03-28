import sys
import os
import importlib.util

print(f"System Path: {sys.path}")

def check_package(name):
    try:
        spec = importlib.util.find_spec(name)
        if spec:
            print(f"{name} found at: {spec.origin}")
            if spec.submodule_search_locations:
                print(f"{name} locations: {spec.submodule_search_locations}")
                for loc in spec.submodule_search_locations:
                    if os.path.exists(loc):
                        print(f"Listing {loc}: {os.listdir(loc)[:10]}...")
        else:
            print(f"{name} NOT found")
    except Exception as e:
        print(f"Error checking {name}: {e}")

check_package("langchain")
check_package("langchain.chains")
