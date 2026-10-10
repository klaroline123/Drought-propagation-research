from pathlib import Path
import os,sys,json
import numpy as np
import pandas as pd
REPO=Path(__file__).resolve().parents[1]
PRODUCTS={'GRUN':'GRUN_try','ERA5':'ERA5_try','GLDAS':'GLADS_try'}
def setup(figure):
    global OUT,QC,DATA,SD
    OUT=REPO/'outputs/supplementary'/f'figure_{figure:02d}'
    QC=OUT/'qc'; DATA=SD=REPO/'figure_source_data/supplementary'/f'figure_{figure:02d}'
    for part in ['qc','02_FIGURES/PNG','02_FIGURES/PDF','02_FIGURES/SVG']:
        (OUT/part).mkdir(parents=True,exist_ok=True)
def prepare(i):
    panels={}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        patterns=[f'A_Fig{i:02d}{letter}_source_data.csv',f'A_Fig{i:02d}_{letter}.csv']
        for name in patterns:
            p=DATA/name
            if p.is_file(): panels[letter]=pd.read_csv(p)
    return panels
"""Block A descriptive figures from panel source tables; Python-only rendering."""
from pathlib import Path
import os,sys,json
sys.dont_write_bytecode=True
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize,ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import cartopy.crs as ccrs
import cartopy.io.shapereader as shp
from audit_panel_alignment import require_matplotlib_panel_alignment
plt.rcParams.update({'font.family':'Times New Roman','font.size':7,'axes.labelsize':7,'axes.titlesize':7,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'legend.fontsize':6.5,'axes.linewidth':.55,'xtick.major.width':.55,'ytick.major.width':.55,'xtick.major.size':2.5,'ytick.major.size':2.5,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
P=['GRUN','ERA5','GLDAS'];C={'GRUN':'#C08760','ERA5':'#215B84','GLDAS':'#73998B'};MARK={'GRUN':'o','ERA5':'s','GLDAS':'^'}
WIDTH=183/25.4
COAST=list(shp.Reader(REPO/'assets/geography/ne_110m_coastline.shp').geometries())
NAMES={1:'data_support',2:'MI_timescale',3:'catalogue_structure',4:'history_range',5:'antecedent_structure'}
def csv(i,l):return pd.read_csv(DATA/f'A_Fig{i:02d}{l}_source_data.csv')
def title(ax,l,s):
 ax.text(0,1.085,l,transform=ax.transAxes,fontsize=8,fontweight='bold',ha='left',va='bottom',clip_on=False)
 ax.text(.085,1.085,s,transform=ax.transAxes,fontsize=7,ha='left',va='bottom',clip_on=False)
def axis(fig,rect,l,s):
 ax=fig.add_axes(rect,label=l);title(ax,l,s);return ax
def mapaxis(fig,rect,i,l,s,cmap,norm):
 ax=fig.add_axes(rect,projection=ccrs.Robinson(),label=l);ax.set_global()
 ax.set_facecolor('#F7F7F5');ax.add_geometries(COAST,ccrs.PlateCarree(),facecolor='none',edgecolor='#777777',linewidth=.25,zorder=3)
 z=np.load(DATA/f'A_Fig{i:02d}{l}_source_data.npz');yy,xx=np.where(np.isfinite(z['value']))
 # Every supported cell is shown at its centre; no data thinning. Compact
 # vector markers avoid exporting259200 mostly blank quadrilaterals per map.
 m=ax.scatter(z['lon'][xx],z['lat'][yy],c=z['value'][yy,xx],s=.22,marker='s',linewidths=0,transform=ccrs.PlateCarree(),cmap=cmap,norm=norm,rasterized=False,zorder=2)
 ax.spines['geo'].set_linewidth(.4);ax.spines['geo'].set_edgecolor('#777777');title(ax,l,s)
 return ax,m
def lines(ax,d,x,y,scale=1):
 for p in P:
  q=d[d['product'].eq(p)].sort_values(x);ax.plot(q[x],q[y]*scale,color=C[p],marker=MARK[p],markersize=3,markeredgewidth=.5,lw=1.1,label=p)
def legend(fig,y=.999):
 handles=[Line2D([],[],color=C[p],marker=MARK[p],ms=3,lw=1,label=p) for p in P]
 fig.legend(handles=handles,ncol=3,loc='upper right',bbox_to_anchor=(.98,y),frameon=False,handlelength=1.6,columnspacing=1.4,borderaxespad=0)
def cbar(fig,m,rect,label,ticks=None):
 ax=fig.add_axes(rect);b=fig.colorbar(m,cax=ax,orientation='horizontal',ticks=ticks)
 if b.solids is not None:b.solids.set_rasterized(False)
 b.outline.set_linewidth(.4);b.set_label(label,fontsize=6.5,labelpad=2);b.ax.tick_params(labelsize=6,length=2,pad=1);return ax
def finish(fig,i,axes,rows,cols):
 stem=f'A_Fig{i:02d}_{NAMES[i]}'
 # Free-positioned maps and plots have different evidence roles; compare only
 # the explicitly listed repeated rows/columns. Thin colourbar axes are not panels.
 fig.canvas.draw()
 require_matplotlib_panel_alignment(fig,axes=axes,panel_ids=[a.get_label() for a in axes],row_groups=rows,column_groups=cols,json_out=QC/f'{stem}.alignment.json',tolerance_pt=1.5,require_panel_labels=True)
 fig.savefig(OUT/'02_FIGURES/PDF'/f'{stem}.pdf',dpi=600)
 fig.savefig(OUT/'02_FIGURES/SVG'/f'{stem}.svg',dpi=600)
 fig.savefig(OUT/'02_FIGURES/PNG'/f'{stem}.png',dpi=600)
 import shutil
 shutil.copyfile(OUT/'02_FIGURES/PNG'/f'{stem}.png',QC/f'{stem}_preview.png')
 plt.close(fig)
 print(f'A_Fig{i:02d}: exported PNG600dpi, vector PDF and editable SVG')
 print('SCIENTIFIC RECOMPUTATION: NONE\nSOURCE STATUS: VERIFIED WITH NOTES')
 return stem
def figure1():
 fig=plt.figure(figsize=(WIDTH,6.9));axes=[];h=.39*WIDTH/1.971655/6.9;ys=[.735,.415,.095]
 for l,p,y in zip('abc',P,ys):
  n=pd.read_csv(DATA/f'A_Fig01{l}_map_summary.csv').valid_cells.iloc[0]
  a,m=mapaxis(fig,[.065,y,.39,h],1,l,f'{p} | {n:,} eligible cells',ListedColormap([C[p]]),Normalize(0,1));axes.append(a)
 a=axis(fig,[.585,ys[0],.39,h],'d','SRI completeness among eligible cells');axes.append(a)
 d=csv(1,'d');d=d[d['index'].eq('SRI1')];thresholds=[50,80,90,95,99,100]
 for p in P:
  q=d[d['product'].eq(p)].set_index('threshold_percent').loc[thresholds];a.plot(range(6),q.percent_eligible,color=C[p],marker=MARK[p],ms=3,lw=1.1)
 a.set_xticks(range(6),[str(v) for v in thresholds]);a.set_xlabel('Minimum complete months (%)');a.set_ylabel('Eligible cells (%)');a.set_ylim(0,103)
 for l,y,kind in [('e',ys[1],'Meteorological'),('f',ys[2],'Hydrological')]:
  a=axis(fig,[.585,y,.39,h],l,kind+' catalogue processing');axes.append(a);d=csv(1,l)
  for p in P:
   q=d[d['product'].eq(p)].set_index('stage').loc[['original','pooled','final']];a.plot(range(3),q.n_events/1e6,color=C[p],marker=MARK[p],ms=3,lw=1.1)
  a.set_xticks(range(3),['Original','Pooled','Retained']);a.set_ylabel('Events (millions)');a.set_ylim(bottom=0);a.set_xlim(-.15,2.15)
 legend(fig);fig.text(.065,.02,'Product-specific catalogue support; 1950–2014. Blank map cells are outside eligibility.',fontsize=6.5)
 return finish(fig,1,axes,[['a','d'],['b','e'],['c','f']],[['a','b','c'],['d','e','f']])
def figure2():
 fig=plt.figure(figsize=(WIDTH,6.2));axes=[];h=.39*WIDTH/1.971655/6.2
 for l,p,y in zip('abc',P,[.72,.41,.10]):
  n=pd.read_csv(DATA/f'A_Fig02{l}_map_summary.csv').valid_cells.iloc[0];a,m=mapaxis(fig,[.065,y,.39,h],2,l,f'{p} | {n:,} MI-valid cells','cividis',Normalize(1,36));axes.append(a)
 cbar(fig,m,[.11,.063,.30,.009],'Selected SPEI accumulation (months)',[1,12,24,36])
 a=axis(fig,[.585,.57,.39,.35],'d','Accumulation-scale distribution');axes.append(a);lines(a,csv(2,'d'),'scale_months','percent');a.set_xlabel('Selected SPEI scale (months)');a.set_ylabel('MI-valid cells (%)');a.set_xlim(1,36);a.set_xticks([1,6,12,18,24,30,36]);a.set_ylim(bottom=0)
 a=axis(fig,[.585,.12,.39,.35],'e','Cumulative grid fractions');axes.append(a);lines(a,csv(2,'e'),'scale_months','cumulative_percent');a.set_xlabel('Selected SPEI scale (months)');a.set_ylabel('Cumulative cells (%)');a.set_xlim(1,36);a.set_xticks([1,12,24,36]);a.set_ylim(0,103);a.axvline(36,color='.55',lw=.55,ls='--')
 legend(fig);fig.text(.585,.035,'36 months is the candidate-range boundary,\nnot a physical-memory estimate.',fontsize=6.5)
 return finish(fig,2,axes,[],[['a','b','c'],['d','e']])
def figure3():
 fig=plt.figure(figsize=(WIDTH,7.9));axes=[]
 a=axis(fig,[.075,.795,.89,.145],'a','Hydrological events in five-year intervals');axes.append(a);d=csv(3,'a');d['year_mid']=(d.period_start+d.period_end)/2;lines(a,d,'year_mid','n_events',1e-3);a.set_ylabel('Events (thousands)');a.set_xticks([1952,1962,1972,1982,1992,2002,2012],['1950–54','1960–64','1970–74','1980–84','1990–94','2000–04','2010–14']);a.set_ylim(bottom=0)
 h=.40*WIDTH/1.971655/7.9
 vmax=max(pd.read_csv(DATA/f'A_Fig03{l}_map_summary.csv')['max'].iloc[0] for l in 'bcd')
 for l,p,y in zip('bcd',P,[.55,.315,.08]):
  a,m=mapaxis(fig,[.065,y,.40,h],3,l,p+' | retained events per cell','YlOrBr',Normalize(0,vmax));axes.append(a)
 cbar(fig,m,[.11,.045,.31,.008],'Events per cell, 1950–2014')
 a=axis(fig,[.675,.08,.26,.63],'e','AR6 catalogue totals');axes.append(a)
 for text in a.texts:text.set_y(1.02)
 d=csv(3,'e');order=sorted(d.AR6.unique());z=d.pivot(index='AR6',columns='product',values='n_HD').reindex(index=order,columns=P)
 im=a.pcolormesh(np.arange(4)-.5,np.arange(len(order)+1)-.5,z.to_numpy()/1000,cmap='YlOrBr',vmin=0,shading='flat',rasterized=False);a.set_xlim(-.5,2.5);a.set_ylim(len(order)-.5,-.5);a.set_xticks(range(3),P);a.set_yticks(range(len(order)),order,fontsize=6);a.tick_params(axis='y',length=0,pad=3);a.spines[['left','bottom']].set_visible(False)
 cbar(fig,im,[.685,.04,.24,.008],'Events (thousands)')
 legend(fig);return finish(fig,3,axes,[],[['b','c','d']])
def figure4():
 fig=plt.figure(figsize=(WIDTH,3.6));axes=[]
 for l,x,ttl in [('a',.085,'Full catalogue | all H events'),('b',.585,'Fixed common-36m coverage cohort')]:
  a=axis(fig,[x,.37,.37,.43],l,ttl);axes.append(a);d=csv(4,l)
  lines(a,d,'window_months','coverage_percent' if l=='a' else 'event_weighted_pct');a.set_xlabel('Antecedent history (months)');a.set_ylabel('Associated events (%)');a.set_ylim(90,100);a.set_yticks([90,95,100]);a.set_xticks([18,21,24,27,30,36] if l=='a' else [12,18,24,36]);a.axvline(24,lw=.6,color='.6',ls='--',zorder=0)
  text=[]
  for p in P:
   q=d[d['product'].eq(p)].iloc[0];n=q.n_H if l=='a' else q.n_targets;text.append(f'{p}: {int(n):,} events; {int(q.n_grids):,} cells')
  fig.text(x,.13,'\n'.join(text),fontsize=6.5,linespacing=1.5)
 legend(fig,.97);fig.text(.085,.025,'Dashed line: operational 24-month choice. Distinct cohorts; curves must not be joined.',fontsize=6.5)
 return finish(fig,4,axes,[['a','b']],[])
def figure5():
 fig=plt.figure(figsize=(WIDTH,8.6));axes=[];h=.39*WIDTH/1.971655/8.6;ys=[.785,.54,.295]
 for l,p,y in zip('abc',P,ys):
  a,m=mapaxis(fig,[.065,y,.39,h],5,l,p+' | multiple / all H','viridis',Normalize(0,1));axes.append(a)
 cbar(fig,m,[.11,.255,.30,.007],'Multiple-antecedent fraction',[0,.5,1])
 a=axis(fig,[.585,ys[0],.39,h],'d','Antecedent composition');axes.append(a);d=csv(5,'d');cats=['No antecedent','Single antecedent','Multiple antecedents'];cs=['#D5D8D9','#94B7BD','#326779'];left=np.zeros(3)
 for cat,col in zip(cats,cs):
  vals=d[d.category.eq(cat)].set_index('product').loc[P,'percent'].to_numpy();a.barh(range(3),vals,left=left,color=col,height=.55,label=cat);left+=vals
 for j,p in enumerate(P):a.text(99,j,f"{d[(d['product']==p)&d.category.eq(cats[2])].percent.iloc[0]:.2f}%",ha='right',va='center',color='white',fontsize=6.5)
 a.set_yticks(range(3),P);a.invert_yaxis();a.set_xlim(0,100);a.set_xlabel('All hydrological events (%)')
 fig.legend(handles=[Patch(facecolor=col,label=label) for col,label in zip(cs,['None','Single','Multiple'])],loc='upper left',bbox_to_anchor=(.065,.999),ncol=3,frameon=False,borderaxespad=0,fontsize=6.5,handlelength=1.1,columnspacing=1)
 a=axis(fig,[.585,ys[1],.39,h],'e','Number of candidate antecedents');axes.append(a);d=csv(5,'e');lines(a,d,'n_candidates','fraction',100);a.set_ylabel('All H events (%)');a.set_xlabel('Antecedents per hydrological event');a.set_ylim(bottom=0);a.set_xticks(np.arange(0,int(d.n_candidates.max())+1,2));a.set_xlim(-.25,d.n_candidates.max()+.25)
 a=axis(fig,[.585,ys[2],.39,h],'f','Annual multiple-antecedent fraction');axes.append(a);d=csv(5,'f')
 for p in P:
  q=d[d['product'].eq(p)];a.plot(q.year,100*q.all_HD_many_fraction,color=C[p],lw=1.1,label=p)
 a.set_xlabel('Onset year');a.set_ylabel('Multiple / all H (%)');a.set_xlim(1952,2014);a.set_xticks([1960,1980,2000,2014])
 a=axis(fig,[.075,.075,.89,.12],'g','Regional multiple-antecedent fractions');axes.append(a);d=csv(5,'g');order=sorted(d.AR6.unique())
 for j,p in enumerate(P):
  q=d[d['product'].eq(p)].set_index('AR6').loc[order];a.plot(np.arange(len(order))+(j-1)*.22,100*q.multiple_fraction,ls='',marker=MARK[p],ms=2.7,color=C[p])
 a.set_xticks(range(len(order)),order,rotation=90,fontsize=6);a.set_xlim(-.6,len(order)-.4);a.set_ylabel('Multiple / all H (%)');a.set_ylim(0,102);a.set_yticks([0,50,100]);a.tick_params(axis='x',length=2,pad=2)
 legend(fig);return finish(fig,5,axes,[['a','d'],['b','e'],['c','f']],[['a','b','c'],['d','e','f']])
def render(i,prepare=False):
 if prepare:raise ValueError("Only frozen panel inputs are supported")
 return globals()[f'figure{i}']()
if __name__=='__main__':
 for i in ([int(sys.argv[1])] if len(sys.argv)>1 else range(1,6)):render(i)
