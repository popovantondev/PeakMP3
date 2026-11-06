"""Verify source version, localized navigation, shared-kit parts and the licensed audio demo."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
LANDING={'ru':'index-ru.html','de':'index.html','en':'index-en.html'}
GUIDE={x:'Guide-'+x+'.html' for x in ('ru','de','en')}
HOME={'ru':'← На страницу программы','de':'← Zur Programmseite','en':'← Program page'}
class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set();self.title='';self._t=False
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='title':self._t=True
  if 'id' in attrs:self.ids.add(attrs['id'])
  self.refs.extend(attrs[k] for k in ('href','src') if k in attrs)
 def handle_endtag(self,tag):
  if tag=='title':self._t=False
 def handle_data(self,data):
  if self._t:self.title+=data
def main():
 d=json.loads((R/'public-release.json').read_text(encoding='utf-8'));errors=[]
 assert d['version']=='0.16.0' and d['shared_distribution']['application_versions']['PeakMP3']==d['version']
 for item in d['version_files']:
  m=re.search(item['pattern'],(R/item['path']).read_text(encoding='utf-8'));assert m and m[1]==d['version']
 titles={}
 kit=(R/'assets/kit/KIT_VERSION').read_text(encoding='utf-8').strip()
 for lang in ('ru','de','en'):
  for kind,names in (('index',LANDING),('Guide',GUIDE)):
   p=R/names[lang];text=p.read_text(encoding='utf-8');page=Page();page.feed(text)
   assert '<html lang="'+lang+'"' in text and d['version'] in text
   if kind=='Guide' and not re.search(r'<a\b[^>]*href="'+LANDING[lang]+r'"[^>]*>\s*'+HOME[lang]+r'\s*</a>',text):errors.append(p.name+': no button to the program page')
   for targetlang in ('ru','de','en'):assert names[targetlang] in page.refs,p.name+' lacks a link to '+names[targetlang]
   for ref in page.refs:
    u=urlsplit(ref)
    if u.scheme or u.netloc:continue
    target=p.parent/unquote(u.path) if u.path else p
    if not target.is_file():errors.append(str(p.name)+': missing '+ref)
    elif u.fragment and target.suffix=='.html':
     other=Page();other.feed(target.read_text(encoding='utf-8'))
     if u.fragment not in other.ids:errors.append(str(p.name)+': missing anchor '+ref)
   # shared kit: header, footer with legal pages, kit files with the current version
   for needle in ('assets/kit/kit.css?v='+kit,'assets/kit/kit.js?v='+kit,'assets/kit/programs.js?v='+kit,'assets/kit/kit-theme.js','class="ppk-nav-wrap"','data-ppk-open-search','data-ppk-theme','class="ppk-footer"','popovantondev/impressum.html','popovantondev/datenschutz.html','class="ppk-page peak-site"'):
    if needle not in text:errors.append(p.name+': missing '+needle)
   if 'about' in ' '.join(page.refs).lower().replace('about:blank',''):errors.append(p.name+': link to an about page')
   # the installer lives in the YouTubeDownloader release; every page explains why
   if d['release_url'] not in page.refs:errors.append(p.name+': no link to the shared release page')
   if page.title in titles:errors.append(p.name+': same <title> as '+titles[page.title])
   titles[page.title]=p.name
   if not page.title.strip():errors.append(p.name+': empty <title>')
   if lang=='de' and re.search(r'\b(du|dein(?!stall)\w*|dir|dich)\b',re.sub(r'<script.*?</script>','',text,flags=re.S),re.I):errors.append(p.name+': informal address (use "Sie")')
   if kind=='index':
    for needle in ('ppk-pill','ppk-btn-gh','ppk-bento','ppk-term','id="demo"','id="peak-demo"','id="demo-audio"','id="density-range"','Get-FileHash'):
     if needle not in text:errors.append(p.name+': missing '+needle)
  guide=(R/GUIDE[lang]).read_text(encoding='utf-8')
  assert 'id="integration"' in guide and 'id="calibration"' in guide
 # old address of the German landing page forwards to the root
 old=(R/'index-de.html').read_text(encoding='utf-8')
 assert 'url=index.html' in old and 'rel="canonical"' in old and '<html lang="de"' in old
 for name in ('index.html','index-en.html','index-ru.html'):assert name in old
 oldpage=Page();oldpage.feed(old)
 if oldpage.title in titles:errors.append('index-de.html: same <title> as '+titles[oldpage.title])
 for lang,files in d['readmes'].items():
  for f in files:
   if not (R/f).is_file():errors.append('missing README '+f)
 assert d['readmes']=={'de':['README.md'],'en':['README.en.md'],'ru':['README.ru.md']},d['readmes']
 for line in (R/'music/SHA256SUMS.txt').read_text().splitlines():
  digest,name=line.split('  ',1);assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,name
 tracks=json.loads((R/'music/tracks.json').read_text(encoding='utf-8'));assert len(tracks)==3
 for track in tracks:
  for density in range(11):
   p=R/'music'/track['id']/('density-'+str(density));assert p.with_suffix('.mp3').stat().st_size>10000
   data=json.loads(p.with_suffix('.json').read_text());assert data['fps']==32 and len(data['vu'])>700 and len(data['peaks'])==len(data['vu']) and len(data['wave'])==350
 assert 'CC BY 4.0' in (R/'music/CREDITS.md').read_text(encoding='utf-8')
 for md in ('README.md','README.en.md','README.ru.md','docs/release-notes.de.md','docs/release-notes.en.md','docs/release-notes.ru.md'):
  for ref in re.findall(r'\]\(([^)#\s]+)(?:#[^)]*)?\)',(R/md).read_text(encoding='utf-8')):
   if urlsplit(ref).scheme:continue
   if not (R/md).parent.joinpath(unquote(ref)).exists():errors.append(md+': missing '+ref)
 assert not any(p.name=='AGENTS.md' for p in R.rglob('*') if '.git' not in p.parts)
 if errors:raise SystemExit('\n'.join(errors))
 print('Verified PeakMP3 0.16.0, six localized pages, shared release, kit parts and 33 music/VU pairs.')
if __name__=='__main__':main()
