"""Render the existing audit Markdown to an archival PDF, without changing its prose."""
from pathlib import Path
import re, html, json, hashlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('Audit','C:/Windows/Fonts/calibri.ttf'))
pdfmetrics.registerFont(TTFont('AuditBold','C:/Windows/Fonts/calibrib.ttf'))
pdfmetrics.registerFont(TTFont('AuditItalic','C:/Windows/Fonts/calibrii.ttf'))
pdfmetrics.registerFont(TTFont('AuditMono','C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFontFamily('Audit',normal='Audit',bold='AuditBold',italic='AuditItalic',boldItalic='AuditBold')
navy=colors.HexColor('#16324a');teal=colors.HexColor('#087d89')
styles=getSampleStyleSheet()
body=ParagraphStyle('AuditBody',fontName='Audit',fontSize=10.5,leading=14.0,spaceAfter=6,textColor=colors.HexColor('#202d37'))
h1=ParagraphStyle('AuditTitle',parent=body,fontName='AuditBold',fontSize=23,leading=27,textColor=navy,spaceAfter=16,keepWithNext=True)
h2=ParagraphStyle('AuditSection',parent=body,fontName='AuditBold',fontSize=15,leading=19,textColor=navy,spaceBefore=15,spaceAfter=8,keepWithNext=True)
h3=ParagraphStyle('AuditSubsection',parent=body,fontName='AuditBold',fontSize=11.5,leading=15,textColor=teal,spaceBefore=10,spaceAfter=6,keepWithNext=True)
cell=ParagraphStyle('AuditCell',parent=body,fontSize=8.6,leading=11.4,spaceAfter=0)
head=ParagraphStyle('AuditTableHead',parent=cell,fontName='AuditBold',textColor=colors.white)
bullet=ParagraphStyle('AuditBullet',parent=body,leftIndent=16,firstLineIndent=-12)

def inline(text):
    text=text.replace('\u2011','-').replace('\u2010','-').replace('\u2013','-').replace('\u2014',' - ')
    parts=re.split(r'(`[^`]+`|\*\*.+?\*\*|\[[^\]]+\]\([^\)]+\))',text)
    out=[]
    for part in parts:
        if part.startswith('`') and part.endswith('`'):
            out.append('<font name="AuditMono" size="9">'+html.escape(part[1:-1])+'</font>')
        elif part.startswith('**') and part.endswith('**'):
            out.append('<b>'+html.escape(part[2:-2])+'</b>')
        elif re.fullmatch(r'\[[^\]]+\]\([^\)]+\)',part):
            m=re.fullmatch(r'\[([^\]]+)\]\(([^\)]+)\)',part)
            out.append('<link href="'+html.escape(m[2],quote=True)+'" color="#087d89">'+html.escape(m[1])+'</link>')
        else:out.append(html.escape(part))
    return ''.join(out)

def table(lines):
    rows=[[s.strip() for s in line.strip().strip('|').split('|')] for line in lines]
    rows=[r for r in rows if not all(re.fullmatch(r':?-+:?',s) for s in r)]
    width=A4[0]-84;n=len(rows[0])
    if n==4:
        ratios=([.07,.20,.46,.27] if rows[0][0]=='ID' else [.08,.36,.25,.31] if rows[0][0]=='Key' else
                [.22,.25,.30,.23] if rows[0][0]=='Surface' else [.46,.16,.19,.19])
    elif n==3:ratios=[.25,.38,.37]
    else:ratios=[1/n]*n
    data=[[Paragraph(inline(v),head if i==0 else cell) for v in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=[width*r for r in ratios],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('VALIGN',(0,0),(-1,-1),'TOP'),
                          ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
                          ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                          ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f1f5f7'),colors.white]),
                          ('LINEBELOW',(0,0),(-1,0),.7,teal),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#dce3e8'))]))
    return t

def footer(canvas,doc):
    canvas.saveState();canvas.setFont('Audit',8);canvas.setFillColor(colors.HexColor('#647582'))
    canvas.drawString(42,A4[1]-26,'PALO / CORRESPONDENCE MATRICES - ADVERSARIAL AUDIT')
    canvas.setStrokeColor(colors.HexColor('#dce3e8'));canvas.line(42,40,A4[0]-42,40)
    canvas.drawString(42,27,'13 October 2026 | Version-scoped review; see coverage limitations')
    canvas.drawRightString(A4[0]-42,27,str(doc.page));canvas.restoreState()

lines=(ROOT/'adversarial_audit.md').read_text(encoding='utf-8').splitlines()
story=[];i=0
while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('|'):
        block=[]
        while i<len(lines) and lines[i].startswith('|'):block.append(lines[i]);i+=1
        story.extend([table(block),Spacer(1,10)]);continue
    if line.startswith('#'):
        level=len(line)-len(line.lstrip('#'));story.append(Paragraph(inline(line[level:].strip()),h1 if level==1 else h2 if level==2 else h3));i+=1;continue
    if line.startswith('```'):
        i+=1;block=[]
        while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
        story.append(Preformatted('\n'.join(block),ParagraphStyle('Code',fontName='AuditMono',fontSize=8.5,leading=11)));i+=1;continue
    if re.match(r'^\d+\. ',line):
        story.append(Paragraph(inline(line),bullet));i+=1;continue
    block=[line];i+=1
    while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```')) and not re.match(r'^\d+\. ',lines[i]):block.append(lines[i]);i+=1
    story.append(Paragraph(inline(' '.join(block)),body))

dest=ROOT/'palo_adversarial_audit_2026-10-13.pdf'
doc=SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=47,bottomMargin=53,
                      title='Adversarial audit of PALO and Correspondence Matrices',author='Prepared for Brian',pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(dest);qa=ROOT/'pdf_qa';qa.mkdir(exist_ok=True)
pdf=pdfium.PdfDocument(str(dest));thumbs=[]
for j in range(len(pdf)):
    page=pdf[j];im=page.render(scale=1.1).to_pil();im.save(qa/f'page_{j+1:02}.png')
    thumb=im.copy();thumb.thumbnail((330,470));thumbs.append(thumb)
for first in range(0,len(thumbs),6):
    sheet=Image.new('RGB',(1020,1000),'#dce3e8');draw=ImageDraw.Draw(sheet)
    for k,im in enumerate(thumbs[first:first+6]):
        x=10+(k%3)*340;y=24+(k//3)*495;sheet.paste(im,(x,y));draw.text((x,y-17),f'Page {first+k+1}',fill='black')
    sheet.save(qa/f'contact_{first//6+1:02}.png')
text='\n'.join(p.extract_text() for p in reader.pages)
checks={'pdf_path':str(dest),'pages':len(reader.pages),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
        'source_sha256':hashlib.sha256((ROOT/'adversarial_audit.md').read_bytes()).hexdigest(),
        'nonempty_pages':all(len(p.extract_text().strip())>100 for p in reader.pages),
        'required_sections_present':all(t in text for t in ['Verdict and material findings','Versions and provenance','Per-direction recommendation','Reproduction results']),
        'replacement_glyph_present':'\ufffd' in text,'visual_review':'pending contact-sheet review'}
(ROOT/'pdf_build_checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,indent=2))
