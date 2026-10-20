"""Verify source version, localized navigation and the licensed audio demo."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if 'id' in attrs:self.ids.add(attrs['id'])
  self.refs.extend(attrs[k] for k in ('href','src') if k in attrs)
def main():
 d=json.loads((R/'public-release.json').read_text(encoding='utf-8'));errors=[]
 assert d['version']=='0.16.0' and d['shared_distribution']['application_versions']['PeakMP3']==d['version']
 for item in d['version_files']:
  m=re.search(item['pattern'],(R/item['path']).read_text(encoding='utf-8'));assert m and m[1]==d['version']
 for lang in ('ru','de','en'):
  for prefix in ('index-','Guide-'):
   p=R/(prefix+lang+'.html');text=p.read_text(encoding='utf-8');page=Page();page.feed(text)
   assert '<html lang="'+lang+'"' in text and d['version'] in text
   for targetlang in ('ru','de','en'):assert prefix+targetlang+'.html' in page.refs
   for ref in page.refs:
    u=urlsplit(ref)
    if u.scheme or u.netloc:continue
    target=p.parent/unquote(u.path) if u.path else p
    if not target.is_file():errors.append(str(p.name)+': missing '+ref)
    elif u.fragment and target.suffix=='.html':
     other=Page();other.feed(target.read_text(encoding='utf-8'))
     if u.fragment not in other.ids:errors.append(str(p.name)+': missing anchor '+ref)
  guide=(R/('Guide-'+lang+'.html')).read_text(encoding='utf-8')
  assert 'id="integration"' in guide and 'id="calibration"' in guide
 for line in (R/'music/SHA256SUMS.txt').read_text().splitlines():
  digest,name=line.split('  ',1);assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,name
 tracks=json.loads((R/'music/tracks.json').read_text(encoding='utf-8'));assert len(tracks)==3
 for track in tracks:
  for density in range(11):
   p=R/'music'/track['id']/('density-'+str(density));assert p.with_suffix('.mp3').stat().st_size>10000
   data=json.loads(p.with_suffix('.json').read_text());assert data['fps']==32 and len(data['vu'])>700 and len(data['peaks'])==len(data['vu']) and len(data['wave'])==350
 assert 'CC BY 4.0' in (R/'music/CREDITS.md').read_text(encoding='utf-8')
 assert not any(p.name=='AGENTS.md' for p in R.rglob('*') if '.git' not in p.parts)
 if errors:raise SystemExit('\n'.join(errors))
 print('Verified PeakMP3 0.16.0, six localized pages, shared release and 33 music/VU pairs.')
if __name__=='__main__':main()
