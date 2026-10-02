import json, re, urllib.request
from pathlib import Path

FOLDER='1BVAgKXl4OaPRS81Qn5B4GGV9azzGKO6X'
URL=f'https://drive.google.com/embeddedfolderview?id={FOLDER}#grid'
req=urllib.request.Request(URL,headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36',
    'Accept-Language':'en-AU,en;q=0.9',
})
html=urllib.request.urlopen(req,timeout=30).read().decode('utf-8','ignore')

# Public Drive folder HTML has changed format over time. Collect IDs from all
# known link/thumbnail forms, plus opaque IDs adjacent to image MIME types.
patterns=[
    r'/file/d/([A-Za-z0-9_-]{10,})',
    r'[?&](?:id|fileId)=([A-Za-z0-9_-]{10,})',
    r'(?:thumbnail|uc)\?[^"\'<>]{0,200}?id=([A-Za-z0-9_-]{10,})',
    r'"([A-Za-z0-9_-]{10,})"[^\n]{0,500}?"image/(?:jpeg|jpg|png|webp|heic|heif)"',
    r'"image/(?:jpeg|jpg|png|webp|heic|heif)"[^\n]{0,500}?"([A-Za-z0-9_-]{10,})"',
]
ids=[]
for pat in patterns:
    for x in re.findall(pat,html,re.I):
        if x != FOLDER and x not in ids:
            ids.append(x)

# Exclude common non-file tokens and keep plausible Drive IDs.
bad={'embeddedfolderview','folders','thumbnail','view','drive','google'}
ids=[x for x in ids if 10 <= len(x) <= 100 and x.lower() not in bad][:500]
photos=[{
    'id':x,
    'thumb':f'https://drive.google.com/thumbnail?id={x}&sz=w1600',
    'view':f'https://drive.google.com/file/d/{x}/view'
} for x in ids]

Path('photo-data.js').write_text('window.SA_U9_PHOTOS = '+json.dumps(photos,separators=(',',':'))+';\n')
Path('photo-sync-debug.json').write_text(json.dumps({'found':len(photos),'html_bytes':len(html)},indent=2)+'\n')
print(f'Fetched {len(html)} bytes; found {len(photos)} photo candidates')
if not photos:
    raise SystemExit('No public photo IDs found. Check that the Drive folder is shared as Anyone with the link can view.')
