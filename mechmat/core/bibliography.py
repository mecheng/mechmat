from mechcite import Bibliography
from pkg_resources import resource_filename

bib = Bibliography()
bib_file = resource_filename('mechmat', 'resources/sources.bib')
bib.load_bib(bib_file, bib.loaded)
