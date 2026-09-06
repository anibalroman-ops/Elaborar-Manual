#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, copy, os, re, shutil, subprocess, sys, unicodedata, zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET

SVG="http://www.w3.org/2000/svg"; INK="http://www.inkscape.org/namespaces/inkscape"; SOD="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
ET.register_namespace("",SVG); ET.register_namespace("inkscape",INK); ET.register_namespace("sodipodi",SOD)
Q=lambda ns,t:f"{{{ns}}}{t}"
PW,PH=210.,297.; X0,X1,CW=18.,192.,174.; HR,FTR,SAFE=38.14,274.54,270.; C2,COL=108.,84.
P="#0A2D69"; S="#5B94D2"; L="#88B4E3"; VL="#EEF5FC"; TH="#DDEAF8"; R="#A8C4E6"; W="#FFFFFF"
SERIF="Noto Serif Display"; SANS="Noto Sans"; BS,BL=2.90,3.78
OPEN={3,7,13,15,18,25,30}
# SEMANTIC_PARSER_V2
OPEN_TITLES={
    3:"Disposiciones generales",
    7:"Ciclo institucional de evaluación y calificación",
    13:"Informe Anual de Actividades y Evidencias Verificables",
    15:"Metodología e instrumentos de evaluación",
    18:"Áreas académicas",
    25:"Retroalimentación",
    30:"ANEXOS TÉCNICOS",
}
PAGE_TITLES={5:"Gobernanza del sistema de evaluación",10:"Convenio de Desempeño Académico"}
FIGMODE={5:"hero",7:"hero",8:"hero",9:"hero",10:"pair",11:"pair",12:"pair",13:"hero",14:"hero",15:"hero",16:"pair",17:"hero",18:"hero",19:"hero",20:"hero",21:"pair",22:"hero",23:"hero",24:"pair",25:"pair",27:"pair",28:"hero",30:"hero"}

@dataclass
class Block: page:int; raw:str; figures:list[str]=field(default_factory=list); atoms:list[str]=field(default_factory=list)
@dataclass
class Issue: sev:str; page:Optional[int]; code:str; msg:str
class Log:
    def __init__(self): self.items=[]
    def add(self,s,p,c,m): self.items.append(Issue(s,p,c,m))
    def errors(self): return [i for i in self.items if i.sev=="ERROR"]

def f(v): return (f"{v:.3f}".rstrip("0").rstrip(".") or "0")
def E(tag,parent=None,**a):
    ns=INK if tag.startswith("inkscape:") else SOD if tag.startswith("sodipodi:") else SVG
    local=tag.split(":",1)[-1]; e=ET.Element(Q(ns,local))
    for k,v in a.items():
        if v is None: continue
        k=k.replace("__",":").replace("_","-")
        if k.startswith("inkscape:"): k=Q(INK,k.split(":",1)[1])
        elif k.startswith("sodipodi:"): k=Q(SOD,k.split(":",1)[1])
        e.set(k,str(v))
    if parent is not None: parent.append(e)
    return e

def cf(ch,fam=SANS):
    if ch.isspace(): return .30
    if ch in "ilI1|.,:;'´`!": return .25
    if ch in "MWQ@%&": return .82
    if ch in "mw": return .72
    if ch.isupper(): return .58 if fam==SANS else .62
    if ch.isdigit(): return .52
    return .34 if unicodedata.category(ch).startswith("P") else (.50 if fam==SANS else .53)
def measure(t,sz,fam=SANS,wt=400): return sum(cf(c,fam) for c in t)*sz*(1.035 if wt>=600 else 1)
def wrap(t,w,sz,fam=SANS,wt=400):
    words=re.sub(r"\s+"," ",t.strip()).split(); out=[]; cur=""
    for word in words:
        cand=word if not cur else cur+" "+word
        if not cur or measure(cand,sz,fam,wt)<=w: cur=cand
        else: out.append(cur); cur=word
    if cur: out.append(cur)
    return out

def norm(s):
    s=unicodedata.normalize("NFKD",s); s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9]+","_",s.upper()).strip("_")

def atoms(text):
    out=[]
    for para in [p.strip() for p in re.split(r"\n\s*\n",text) if p.strip()]:
        lines=[re.sub(r"\s+"," ",x.strip()) for x in para.splitlines() if x.strip()]
        buf=[]
        def flush():
            if buf:
                out.append(" ".join(buf)); buf.clear()
        for line in lines:
            special=(line=="•" or re.fullmatch(r"\d{1,3}(?:\.\d+)?",line) or
                     line.startswith("TÍTULO") or re.match(r"^Art(?:ículo|ículos)\b",line,re.I) or
                     re.match(r"^Art\.\s*\d+",line,re.I) or line in {"(continuación)","DISPOSICIONES TRANSITORIAS","ANÓTESE, COMUNÍQUESE Y REGÍSTRESE"})
            if special:
                flush(); out.append(line)
            else: buf.append(line)
        flush()
    final=[]; i=0
    while i<len(out):
        if out[i]=="•" and i+1<len(out): final.append("• "+out[i+1]); i+=2
        else: final.append(out[i]); i+=1
    return final

def parse(md):
    pat=re.compile(r"<!--\s*SOURCE_PAGE:\s*(\d+)\s*-->"); ms=list(pat.finditer(md)); out=[]
    for i,m in enumerate(ms):
        end=ms[i+1].start() if i+1<len(ms) else md.find("# INVENTARIO DE FIGURAS EXTERNAS",m.end()); end=len(md) if end<0 else end
        ch=md[m.end():end]; figs=[x.strip() for x in re.findall(r"<!--\s*FIGURE_REF:\s*([^>]+?)\s*-->",ch)]
        ch=re.sub(r"<!--.*?-->","",ch,flags=re.S); ch=re.sub(r"^##\s+BLOQUE DE CONTENIDO\s+\d+\s*$","",ch,flags=re.M)
        out.append(Block(int(m.group(1)),ch.strip(),figs,atoms(ch)))
    return out

class Assets:
    def __init__(self,root,build,log): self.root=root; self.build=build; self.log=log; self.a={}; self.index()
    def add(self,p):
        k=norm(p.stem)
        if k and k not in self.a: self.a[k]=p
    def index(self):
        for p in self.root.rglob("*.svg"):
            if p.name not in {"manual_desempeno_final.svg","avance_manual.svg"}: self.add(p)
        ex=self.build/"figuras_extraidas"; ex.mkdir(parents=True,exist_ok=True)
        for z in self.root.rglob("*.zip"):
            try:
                with zipfile.ZipFile(z) as zh:
                    for n in zh.namelist():
                        if n.lower().endswith(".svg"):
                            dst=ex/(norm(z.stem)+"__"+Path(n).name); dst.write_bytes(zh.read(n)); self.add(dst)
            except zipfile.BadZipFile: self.log.add("WARN",None,"ZIP_INVALIDO",z.name)
    def find(self,ref):
        k=norm(ref)
        if k in self.a: return self.a[k]
        c=[p for kk,p in self.a.items() if k in kk or kk in k]
        return c[0] if len(c)==1 else None

def prefix_ids(root,prefix):
    mp={}
    for n in root.iter():
        old=n.get("id")
        if old: mp[old]=prefix+"_"+old; n.set("id",mp[old])
    for n in root.iter():
        for a,v in list(n.attrib.items()):
            for old,new in mp.items(): v=v.replace(f"url(#{old})",f"url(#{new})"); v=f"#{new}" if v==f"#{old}" else v
            n.set(a,v)
def viewbox(root):
    if root.get("viewBox"):
        v=[float(x) for x in re.split(r"[ ,]+",root.get("viewBox").strip())]
        if len(v)==4:return v
    def d(k,default):
        m=re.match(r"([\d.]+)",root.get(k,str(default))); return float(m.group(1)) if m else default
    return [0,0,d("width",100),d("height",100)]

class Page:
    def __init__(self,n,log):
        self.n=n; self.log=log; self.g=E("g",id=f"p{n:02d}_content",inkscape__groupmode="layer",inkscape__label=f"Página {n:02d}"); self.maxy=0
        self.rect(0,0,PW,PH,W,"none",0,id=f"p{n:02d}_background")
    def rect(self,x,y,w,h,fill=W,stroke="none",sw=0,rx=0,id=None,parent=None): return E("rect",(parent if parent is not None else self.g),x=f(x),y=f(y),width=f(w),height=f(h),fill=fill,stroke=stroke,stroke_width=f(sw),rx=f(rx),id=id)
    def line(self,x1,y1,x2,y2,stroke=R,sw=.28,parent=None): return E("line",(parent if parent is not None else self.g),x1=f(x1),y1=f(y1),x2=f(x2),y2=f(y2),stroke=stroke,stroke_width=f(sw))
    def text(self,x,y,t,sz=BS,fam=SANS,wt=400,fill=P,anchor="start",parent=None,spacing=None):
        q=E("text",(parent if parent is not None else self.g),x=f(x),y=f(y),font_family=fam,font_size=f(sz),font_weight=str(wt),fill=fill,text_anchor=anchor)
        if spacing is not None:q.set("letter-spacing",f(spacing))
        sp=E("tspan",q,x=f(x),y=f(y)); sp.text=t; self.maxy=max(self.maxy,y+sz); return q
    def wrapped(self,x,y,w,t,sz=BS,line=BL,fam=SANS,wt=400,fill=P,parent=None):
        ls=wrap(t,w,sz,fam,wt); q=E("text",(parent if parent is not None else self.g),x=f(x),y=f(y),font_family=fam,font_size=f(sz),font_weight=str(wt),fill=fill)
        for i,s in enumerate(ls): sp=E("tspan",q,x=f(x),y=f(y+i*line)); sp.text=s
        end=y+max(line,len(ls)*line); self.maxy=max(self.maxy,end); return end
    def header(self,section=None):
        g=E("g",self.g,id=f"p{self.n:02d}_header"); self.text(18,18.4,"UNIVERSIDAD DE SANTIAGO DE CHILE",3.2,wt=700,parent=g); self.text(18,24.1,"FACULTAD DE INGENIERÍA",2.85,wt=500,fill=S,parent=g)
        self.wrapped(126,18.3,66,section or "Manual de Evaluación y Calificación del Desempeño Académico",2.55,3.35,parent=g); self.line(18,HR,192,HR,P,.32,g)
    def footer(self):
        g=E("g",self.g,id=f"p{self.n:02d}_footer"); self.line(18,FTR,192,FTR,P,.31,g); self.text(18,284,"Santiago de Chile · 2026",3.05,parent=g); self.text(192,286,str(self.n),8.1,SERIF,600,P,"end",g)
    def cover(self,a):
        self.text(18,19,"UNIVERSIDAD DE SANTIAGO DE CHILE",3.2,wt=700); self.text(18,24.8,"FACULTAD DE INGENIERÍA",2.9,wt=500,fill=S); self.line(18,34,192,34,P,.32)
        title=" ".join(a[:-1] if len(a)>1 else a); sub=a[-1] if len(a)>1 else ""; y=self.wrapped(18,79,154,title,11.85,13.4,SERIF,600)+8; self.line(18,y,54,y,S,1); y+=12
        if sub:self.wrapped(18,y,120,sub,3.45,4.5,wt=500)
        self.rect(18,185,174,42,VL,"none",0,2.4)
        for i,w in enumerate([34,52,73,97,126]): self.line(28,218-i*6.1,28+w,218-i*6.1,[R,L,S,P,P][i],.7 if i<3 else 1)
        self.line(18,FTR,192,FTR,P,.31); self.text(18,284,"Santiago de Chile · 2026",3.05)
    def opening(self,label,title,intro=None,num=None,y=49):
        if label:self.text(18,y,label.upper(),3.6,wt=700,fill=S,spacing=.35); y+=9
        tx,tw=(52,140) if num else (18,174)
        if num:self.text(18,y+22,num,31.5,SERIF,500)
        ye=self.wrapped(tx,y+(4 if num else 0),tw,title,11.85 if num else 9.4,13.1 if num else 10.3,SERIF,600); y=max(ye,y+37 if num else ye)+5; self.line(18,y,46,y,S,.9); y+=8
        if intro:y=self.wrapped(18,y,120 if self.n in OPEN else 174,intro,3.05,4.05)+5
        return y
    def article(self,x,y,w,h):
        y=self.wrapped(x,y,w,h,4.05,4.85,SERIF,600); self.line(x,y+.6,min(x+15,x+w),y+.6,S,.65); return y+5.5
    def bullets(self,x,y,w,items):
        for item in items:
            self.rect(x,y+.7,1.8,1.8,S,"none",0,.9); y=self.wrapped(x+4.2,y,w-4.2,item.lstrip("• "),2.72,3.4)+2
        return y
    def flow(self,a,y=46,two=True,maxy=SAFE):
        cols=[(18,COL),(108,COL)] if two else [(18,174)]; ci=0; x,w=cols[0]; i=0
        while i<len(a):
            atom=a[i]; k=kind(atom)
            if k=="article" and i+1<len(a) and kind(a[i+1]) in {"label","title"} and len(a[i+1])<=72:
                atom=atom+" · "+a[i+1]; i+=1
            est=height(atom,w,k)
            if y+est>maxy and ci+1<len(cols): ci+=1; x,w=cols[ci]; y=46 if two else y
            elif y+est>maxy:self.log.add("ERROR",self.n,"OVERFLOW_TEXT",atom[:90])
            if k=="article": y=self.article(x,y,w,atom)+4.2
            elif k=="title": y=self.wrapped(x,y,w,atom,5.25,6,SERIF,600)+4
            elif k=="label": y=self.wrapped(x,y,w,atom,2.75,3.35,wt=700,fill=S)+2.7
            elif k=="bullet": y=self.bullets(x,y,w,[atom])+.7
            elif k=="number": self.text(x,y+4.5,atom,5,SERIF,500,S); y+=8
            else:y=self.wrapped(x,y,w,atom)+3.3
            i+=1
        return y
    def figure(self,path,ref,x,y,w,h,idx):
        try:
            src=ET.parse(path).getroot(); prefix_ids(src,f"p{self.n:02d}_{norm(ref).lower()}"); vx,vy,vw,vh=viewbox(src); g=E("g",self.g,id=f"p{self.n:02d}_fig_{idx:02d}")
            nested=E("svg",g,x=f(x),y=f(y),width=f(w),height=f(h),viewBox=" ".join(f(v) for v in [vx,vy,vw,vh]),preserveAspectRatio="xMidYMid meet")
            for c in list(src):
                if c.tag!=Q(SOD,"namedview"): nested.append(copy.deepcopy(c))
            self.maxy=max(self.maxy,y+h); return y+h
        except Exception as e:self.log.add("ERROR",self.n,"FIGURA_ERROR",f"{path.name}: {e}"); return y

def kind(s):
    s=s.strip()
    if s.startswith("•") or re.match(r"^\d+\.\s+",s):return "bullet"
    if re.match(r"^Art(?:ículo|ículos)\b",s,re.I) or re.match(r"^Art\.\s*\d+",s,re.I):return "article"
    if re.fullmatch(r"\d{1,3}(?:\.\d+)?",s):return "number"
    if s.startswith("TÍTULO"):return "label"
    if len(s)<70 and s.upper()==s and any(c.isalpha() for c in s):return "title"
    if len(s)<48 and (s.endswith(":") or re.match(r"^[A-ZÁÉÍÓÚÑ][^.!?]{2,45}$",s)):return "label"
    return "body"
def height(s,w,k):
    if k=="article":return len(wrap(s,w,4.05,SERIF,600))*4.85+9
    if k=="title":return len(wrap(s,w,5.25,SERIF,600))*6+5
    if k=="label":return len(wrap(s,w,2.75,SANS,700))*3.35+4
    if k=="bullet":return len(wrap(s.lstrip("• "),w-4.2,2.72))*3.4+3
    if k=="number":return 8
    return len(wrap(s,w,BS))*BL+4

def split_intro(a):
    if not a:return [],[]
    cut=1
    for i,s in enumerate(a[:7]):
        if kind(s) in {"number","title","article"}:cut=i+1;continue
        if len(s)>90:cut=i+1;break
    cut=max(1,min(cut,5));return a[:cut],a[cut:]

def consume_heading(a,page,title,with_num=False):
    i=0; num=None; label=""; intro=None
    if with_num and i<len(a) and re.fullmatch(r"\d{1,2}",a[i]): num=a[i]; i+=1
    if i<len(a) and a[i].startswith("TÍTULO"): label=a[i]; i+=1
    if i<len(a):
        src=re.sub(r"\s+"," ",a[i]).strip(); ttl=re.sub(r"\s+"," ",title).strip()
        if src.casefold().startswith(ttl.casefold()):
            intro=src[len(ttl):].strip() or None; i+=1
    if intro is None and i<len(a) and kind(a[i])=="body" and len(a[i])>80:
        intro=a[i]; i+=1
    return num,label,title,intro,i

def toc_items(raw):
    ls=[re.sub(r"\s+"," ",x.strip()) for x in raw.splitlines() if x.strip()]
    if ls and ls[0].casefold()=="contenido": ls=ls[1:]
    items=[]; buf=[]
    for x in ls:
        if re.fullmatch(r"\d{2,3}",x) and buf:
            label=buf[0] if buf[0].startswith("Título") else ""
            title=" ".join(buf[1:] if label else buf); items.append((label,title,x)); buf=[]
        else: buf.append(x)
    return items," ".join(buf)

def render(b,assets,log):
    p=Page(b.page,log); a=b.atoms[:]
    if b.page==1:
        lines=[re.sub(r"\s+"," ",x.strip()) for x in b.raw.splitlines() if x.strip()]
        p.cover(lines); return p
    p.header(next((x for x in a[:5] if x.startswith("TÍTULO")),None)); p.footer()
    if b.page==2:
        y=p.opening("","Contenido",y=51); items,note=toc_items(b.raw)
        for j,(label,title,folio) in enumerate(items[:12]):
            col=0 if j<6 else 1; row=j if j<6 else j-6; x=18 if col==0 else 108; w=84; yy=84+row*27.2
            if label:p.text(x,yy,label.upper(),2.35,wt=700,fill=S,spacing=.18)
            p.wrapped(x,yy+5.2,w-13,title,3.15,3.8,SERIF,600)
            p.text(x+w,yy+6.2,folio,5.2,SERIF,600,S,"end")
            p.line(x,yy+22.2,x+w,yy+22.2,R,.24)
        if note:
            p.rect(18,247,174,18,VL,"none",0,2)
            p.wrapped(24,252,162,note,2.72,3.35,fill=P)
        return p
    y=46; used=0
    if b.page in OPEN_TITLES:
        num,label,title,intro,used=consume_heading(a,b.page,OPEN_TITLES[b.page],True)
        y=p.opening(label,title,intro,num)+3
    elif b.page in PAGE_TITLES:
        num,label,title,intro,used=consume_heading(a,b.page,PAGE_TITLES[b.page],False)
        y=p.opening(label,title,intro,None,y=48)+3
    if b.page==3:
        rem=a[used:]; items=[]; i=0
        while i<len(rem):
            if kind(rem[i])=="article":
                art=rem[i]; title=rem[i+1] if i+1<len(rem) else ""; folio=rem[i+2] if i+2<len(rem) and kind(rem[i+2])=="number" else ""
                items.append((art,title,folio)); i+=3 if folio else 2
            else:i+=1
        for j,(art,title,folio) in enumerate(items[:4]):
            x=18 if j%2==0 else 108; yy=y+(j//2)*48; p.rect(x,yy,84,40,VL,"none",0,2.2)
            p.text(x+6,yy+9,art.upper(),2.55,wt=700,fill=S,spacing=.18); p.wrapped(x+6,yy+16,60,title,3.8,4.6,SERIF,600)
            if folio:p.text(x+76,yy+31,folio,6.4,SERIF,600,S,"end")
        return p
    found=[]
    for ref in b.figures:
        q=assets.find(ref)
        if q:found.append((ref,q))
        else:log.add("WARN",b.page,"FIGURA_DIFERIDA",ref)
    rem=a[used:]; mode=FIGMODE.get(b.page)
    if mode and found:
        intro,rest=split_intro(rem); y=p.flow(intro,y,False,min(118,SAFE))+4 if intro else y
        if mode=="hero":
            h=min(104,max(62,205-y)); y=p.figure(found[0][1],found[0][0],18,y,174,h,1)+7
            for j,(ref,q) in enumerate(found[1:],2):
                if y+55<SAFE:y=p.figure(q,ref,18,y,174,52,j)+6
        elif len(found)==1:y=p.figure(found[0][1],found[0][0],18,y,174,67,1)+7
        else:
            y=max(p.figure(found[0][1],found[0][0],18,y,84,67,1),p.figure(found[1][1],found[1][0],108,y,84,67,2))+7
        if rest:p.flow(rest,y)
    else:p.flow(rem,y)
    return p

def rootdoc():
    r=ET.Element(Q(SVG,"svg"),{"width":"210mm","height":"297mm","viewBox":"0 0 210 297","version":"1.1","id":"manual_desempeno_final",Q(INK,"version"):"1.4",Q(SOD,"docname"):"manual_desempeno_final.svg"})
    E("defs",r,id="defs_manual"); nv=E("sodipodi:namedview",r,id="namedview_manual",pagecolor="#d1d1d1",inkscape__document_units="mm",showgrid="false"); return r,nv
def pos(n):i=n-1;return (i%5)*(PW+10),(i//5)*(PH+10)
def write(r,p):p.parent.mkdir(parents=True,exist_ok=True);ET.ElementTree(r).write(p,encoding="utf-8",xml_declaration=True)
def build_documents(blocks,assets,out,pages,log):
    r,nv=rootdoc(); files=[]
    for b in blocks:
        p=render(b,assets,log); px,py=pos(b.page); pid=f"page_{b.page:02d}"; E("inkscape:page",nv,x=f(px),y=f(py),width=f(PW),height=f(PH),id=pid,margin="0",bleed="0")
        g=copy.deepcopy(p.g);g.set("transform",f"translate({f(px)},{f(py)})");r.append(g)
        pr,pn=rootdoc();E("inkscape:page",pn,x="0",y="0",width=f(PW),height=f(PH),id=pid,margin="0",bleed="0");pr.append(copy.deepcopy(p.g));pf=pages/f"page_{b.page:03d}.svg";write(pr,pf);files.append(pf)
        if p.maxy>PH+.1:log.add("ERROR",b.page,"OBJECT_OUTSIDE_PAGE",f"y={p.maxy:.2f}")
    write(r,out);return files
def run(c):return subprocess.run(c,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def export(files,pdf,preview,build,log,inkscape):
    preview.mkdir(parents=True,exist_ok=True);pd=build/"pdf_pages";pd.mkdir(exist_ok=True);pdfs=[]
    for i,s in enumerate(files,1):
        png=preview/f"pagina_{i:03d}.png"; pp=pd/f"pagina_{i:03d}.pdf"
        a=run([inkscape,str(s),"--export-type=png",f"--export-filename={png}","--export-dpi=140"]); b=run([inkscape,str(s),"--export-type=pdf",f"--export-filename={pp}"])
        if a.returncode or not png.exists():log.add("ERROR",i,"PNG_EXPORT",a.stderr.strip())
        if b.returncode or not pp.exists():log.add("ERROR",i,"PDF_EXPORT",b.stderr.strip())
        else:pdfs.append(pp)
    if len(pdfs)==len(files):
        try:
            from pypdf import PdfReader,PdfWriter
            w=PdfWriter()
            for q in pdfs:
                for pg in PdfReader(str(q)).pages:w.add_page(pg)
            with pdf.open("wb") as fh:w.write(fh)
        except Exception as e:log.add("ERROR",None,"PDF_MERGE",str(e))
def validate(svg,n,log):
    try:r=ET.parse(svg).getroot()
    except Exception as e:log.add("ERROR",None,"SVG_PARSE",str(e));return
    if len(r.findall(f".//{Q(INK,'page')}"))!=n:log.add("ERROR",None,"PAGE_COUNT","Cantidad de inkscape:page incorrecta")
    ids=[]
    for q in r.iter():
        if q.get("id"):ids.append(q.get("id"))
        if q.tag==Q(SVG,"image"):log.add("WARN",None,"RASTER_IMAGE",q.get("id") or "sin id")
        if q.tag in {Q(SVG,"filter"),Q(SVG,"mask"),Q(SVG,"clipPath")}:log.add("WARN",None,"COMPLEX_EFFECT",q.tag.split("}")[-1])
        if q.tag==Q(SVG,"text") and q.get("font-size"):
            try:
                if float(re.match(r"[\d.]+",q.get("font-size")).group())<2.20:log.add("ERROR",None,"FONT_ABSOLUTE_MIN","Texto menor a 2.20 mm")
            except:pass
    if len(ids)!=len(set(ids)):log.add("ERROR",None,"DUPLICATE_IDS",str(len(ids)-len(set(ids))))
def report(path,blocks,assets,log,svg,pdf,preview):
    miss=[];found=[]
    for b in blocks:
        for ref in b.figures:(found if assets.find(ref) else miss).append((b.page,ref))
    out=["# Reporte de validación — Manual de Desempeño Académico","",f"- Páginas procesadas: **{len(blocks)}**.",f"- SVG: **{'OK' if svg.exists() else 'NO'}**.",f"- PDF: **{'OK' if pdf.exists() else 'NO'}**.",f"- Previews: **{len(list(preview.glob('*.png'))) if preview.exists() else 0}**.",f"- Figuras integradas automáticamente: **{len(found)} / {len(found)+len(miss)}**.","- Estado editorial: **la maquetación textual continúa aunque las figuras estén diferidas para inserción manual**.","","## Figuras pendientes de inserción manual",""]
    out += [f"- Página {p:02d}: `{r}`" for p,r in miss] or ["- Ninguna."]; out += ["","## Incidencias",""]
    out += [f"- **{i.sev}** · {'Página '+str(i.page) if i.page else 'Documento'} · `{i.code}` — {i.msg}" for i in log.items] or ["- Sin incidencias automáticas."]
    out += ["","## Controles","","- SVG multipágina A4 con `inkscape:page`.","- Texto en `<text>/<tspan>`.","- Figuras SVG vectoriales, sin rasterización por el generador.","- Retícula 18–192 mm y pie bajo 274,54 mm.","- Overflow y figuras faltantes se reportan; no se reduce tipografía silenciosamente.",""]
    path.write_text("\n".join(out),encoding="utf-8")
def main():
    a=argparse.ArgumentParser();a.add_argument("--root",type=Path,default=Path(__file__).resolve().parent);a.add_argument("--no-export",action="store_true");a.add_argument("--inkscape",default=os.getenv("INKSCAPE","inkscape"));z=a.parse_args();root=z.root.resolve()
    cp=root/"contenido_manual_desempeno.md";dp=root/"diseno_maestro_editorial.md";svg=root/"manual_desempeno_final.svg";pdf=root/"manual_desempeno_final.pdf";preview=root/"preview";rep=root/"reporte_validacion.md";builddir=root/".build_manual_svg";pages=builddir/"pages"
    if not cp.exists() or not dp.exists():print("Faltan archivos autoritativos",file=sys.stderr);return 2
    if builddir.exists():shutil.rmtree(builddir);pages.mkdir(parents=True)
    else:pages.mkdir(parents=True)
    if preview.exists():shutil.rmtree(preview)
    design=dp.read_text(encoding="utf-8"); content=cp.read_text(encoding="utf-8"); log=Log()
    for tok in ["PAGE_WIDTH","GRID_TWO_COLUMNS_EQUAL","Noto Serif Display","Noto Sans","SVG_EDITABILITY_RULES"]:
        if tok not in design:log.add("ERROR",None,"DESIGN_TOKEN_MISSING",tok)
    blocks=parse(content);assets=Assets(root,builddir,log);files=build_documents(blocks,assets,svg,pages,log);validate(svg,len(blocks),log)
    if not z.no_export:
        if not shutil.which(z.inkscape):log.add("ERROR",None,"INKSCAPE_MISSING",z.inkscape)
        else:export(files,pdf,preview,builddir,log,z.inkscape)
    report(rep,blocks,assets,log,svg,pdf,preview);print(f"Páginas={len(blocks)} errores={len(log.errors())} SVG={svg.name} PDF={'OK' if pdf.exists() else 'NO'}");return 1 if log.errors() else 0
if __name__=="__main__":raise SystemExit(main())
