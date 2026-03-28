import urllib.request
import urllib.error

# Test if youtube embed search is still active
url = "https://www.youtube.com/embed?listType=search&list=Fix+You+Coldplay+official"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        if "Video unavailable" in html or "class=\"ytp-error\"" in html:
            print("YouTube embed search seems to be returning an error page.")
        else:
            print("YouTube embed search returned HTTP 200, length:", len(html))
            if "listType" not in html:
                print("However, the response may not be a search playlist.")
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
