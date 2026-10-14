"""Replace only the title-page byline, preserving the original reviewed PDF layout.

The installed compiler lacks logreq.sty. Reuse the embedded Latin Modern Roman
font and author glyph run from the successfully rebuilt companion manuscript.
The separate corrected TeX/bibliography remains available for future rebuilding.
"""
from pathlib import Path
import copy, json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, FloatObject, NameObject

OUT=Path(__file__).resolve().parent
original=PdfReader(OUT/'original_site_pdfs/hierarchical-concepts-r1-v0.3.pdf')
donor=PdfReader(OUT/'prepared_website/public/manuscripts/observation-refinement-r2-v0.5.pdf')

def author_run(reader):
    stream=ContentStream(reader.pages[0].get_contents(),reader)
    font=None
    for index,(args,operator) in enumerate(stream.operations):
        if operator==b'Tf':
            font,size=args
        if operator==b'TJ' and 'Brian' in str(args):
            return stream,index,args,font,size,reader.pages[0]['/Resources']['/Font'][font].get_object()
    raise ValueError('No author run')

def width(args,font,size):
    widths=font['/Widths']
    first=int(font['/FirstChar'])
    total=0
    for part in args[0]:
        if isinstance(part,(int,float)):
            total-=float(part)
        else:
            data=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
            total+=sum(float(widths[c-first]) for c in data)
    return total*float(size)/1000

_,index,old_args,old_font,old_size,old_font_obj=author_run(original)
_,_,new_args,_,new_size,new_font_obj=author_run(donor)
assert float(old_size)==float(new_size)
assert 'Theory' in str(new_args)
dx=(width(old_args,old_font_obj,old_size)-width(new_args,new_font_obj,new_size))/2
writer=PdfWriter(clone_from=original)
page=writer.pages[0]
new_font_name=NameObject('/AuthorBrianTheory')
page['/Resources']['/Font'][new_font_name]=new_font_obj.clone(writer)
stream=ContentStream(page.get_contents(),writer)
stream.operations[index:index+1]=[
    ([FloatObject(dx),FloatObject(0)],b'Td'),
    ([new_font_name,FloatObject(new_size)],b'Tf'),
    (copy.deepcopy(new_args),b'TJ'),
    ([NameObject(old_font),FloatObject(old_size)],b'Tf'),
    ([FloatObject(-dx),FloatObject(0)],b'Td'),
]
page.replace_contents(stream)
writer.add_metadata({'/Author':'Brian Theory'})
target=OUT/'prepared_website/public/manuscripts/hierarchical-concepts-r2-v0.3.pdf'
writer.write(target)
after=PdfReader(target)
assert len(after.pages)==len(original.pages)==9
assert 'Brian Theory' in after.pages[0].extract_text()
assert 'Brian Droncheff' not in after.pages[0].extract_text()
assert all(a.get_contents().get_data()==b.get_contents().get_data() for a,b in zip(original.pages[1:],after.pages[1:]))
(OUT/'hierarchical_pdf_correction.json').write_text(json.dumps(dict(method='Original reviewed PDF; replace only first-page author glyph run and Author metadata',font='Embedded Latin Modern Roman from corrected companion',horizontal_centering_adjustment_pt=dx,unchanged_page_content_streams=list(range(2,10)),source_rebuild_status='Local compiler missing logreq.sty; no package installed'),indent=2),encoding='utf-8')
print(target)
