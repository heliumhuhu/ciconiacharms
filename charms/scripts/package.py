from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parents[1];release=root.parent/'CICONIA-CHARMS-v1.6.2.zip'
files=['package.json','package-lock.json','server.js','build.js','tsconfig.json','README.md','BRIEF.md','PROGRESS.md','SETUP.md','VALIDATION.md','tests/mechanics.test.js','tests/browser.py','tests/focus.py','tests/interruptions.py','tests/standalone.py','tests/geometry.py','tests/save-sequence.py','tests/catalogue.py','scripts/standalone.py','scripts/package.py']
files += ['public/'+n for n in ['index.html','boutique.css','boutique.js','rack.js','motion-config.js','products.js','bag.js','product-view.js']]
for folder in ['public/assets','public/vendor']:
 files += [str(p.relative_to(root)) for p in (root/folder).rglob('*') if p.is_file()]
with ZipFile(release,'w',ZIP_DEFLATED,compresslevel=9) as z:
 for n in files:z.write(root/n,'charms/'+n)
 z.write(root.parent/'CICONIA-CHARMS-v1.6.2.html','CICONIA-CHARMS-v1.6.2.html')
with ZipFile(release) as z:assert z.testzip() is None;print('PASS archive integrity:',len(z.namelist()),'files;',release.stat().st_size,'bytes')
