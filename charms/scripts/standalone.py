"""Build an offline HTML with one copy of each JS module and embedded assets."""
from pathlib import Path
import base64,json,re,mimetypes
root=Path(__file__).resolve().parents[1]/'public'
def data(p):return 'data:'+(mimetypes.guess_type(str(p))[0] or 'application/octet-stream')+';base64,'+base64.b64encode(p.read_bytes()).decode()
def assets(text):
 for p in (root/'assets').rglob('*'):
  if p.is_file():
   name='/'+str(p.relative_to(root))
   if name in text:text=text.replace(name,data(p))
 return text
modules={}
def module(path):
 path=path.resolve();key=str(path.relative_to(root))
 if key in modules:return key
 def sub(m):
  rel=m.group(2);dep=root/rel.lstrip('/') if rel.startswith('/') else path.parent/rel
  return m.group(1)+'__MODULE_'+module(dep)+'__'+m.group(3)
 text=re.sub(r"(from\s*['\"])([./][^'\"]+)(['\"])",sub,path.read_text())
 modules[key]=assets(text)
 return key
entry=module(root/'boutique.js')
loader='const sources='+json.dumps(modules)+';const urls={};for(const [key,source] of Object.entries(sources)){const text=source.replace(/__MODULE_(.*?)__/g,(_,name)=>urls[name]);urls[key]=URL.createObjectURL(new Blob([text],{type:"text/javascript"}));}await import(urls['+json.dumps(entry)+']);'
html=(root/'index.html').read_text().replace('<link rel="stylesheet" href="/boutique.css">','<style>'+(root/'boutique.css').read_text()+'</style>').replace('<script type="module" src="/boutique.js"></script>','').replace('href="/"','href="#collection"')
html=assets(html).replace('</body>','<script type="module">'+loader.replace('</script','<\\/script')+'</script></body>')
out=root.parent.parent/'CICONIA-CHARMS-v1.6.3.html';out.write_text(html);print(out,out.stat().st_size)
