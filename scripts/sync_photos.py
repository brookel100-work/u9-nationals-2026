import json,re,urllib.request
from pathlib import Path
FOLDER='1BVAgKXl4OaPRS81Qn5B4GGV9azzGKO6X'
URL=f'https://drive.google.com/embeddedfolderview?id={FOLDER}#grid'
req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0'})
html=urllib.request.urlopen(req,timeout=30).read().decode('utf-8','ignore')
patterns=[r'https://drive\.google\.com/file/d/([A-Za-z0-9_-]{20,})',r'"([A-Za-z0-9_-]{25,})"[^\n]{0,160}(?:image/|\.jpe?g|\.png|\.webp|\.heic)',r'(?:data-id|data-target-id)="([A-Za-z0-9_-]{20,})"']
ids=[]
for pat in patterns:
    for x in re.findall(pat,html,re.I):
        if x!=FOLDER and x not in ids: ids.append(x)
# Filter obvious non-file tokens; Drive file IDs are normally long opaque IDs.
ids=[x for x in ids if 20 <= len(x) <= 80][:300]
photos=[{'id':x,'thumb':f'https://drive.google.com/thumbnail?id={x}&sz=w1200','view':f'https://drive.google.com/file/d/{x}/view'} for x in ids]
out='window.SA_U9_PHOTOS = '+json.dumps(photos,separators=(',',':'))+';\n'
Path('photo-data.js').write_text(out)
print(f'Found {len(photos)} photo candidates')
