from pathlib import Path
import os,sys,json
import numpy as np
import pandas as pd
REPO=Path(__file__).resolve().parents[1]
PRODUCTS=['GRUN','ERA5','GLDAS']
NAMES={1:'environmental_models',2:'regional_associations',3:'covariate_trajectories',4:'severity_trends',5:'severity_robustness'}
VARS=['forcing_mean_intensity','forcing_mass_24','n_candidates','met_onset_span_months','sm_pre_3_1','sm_recovery_fixed']
TREND=['forcing_intensity_sen_decade','forcing_mass_sen_decade','candidate_density_sen_decade','antecedent_extent_sen_decade','preH_soil_state_sen_decade','soil_recovery_fixed_sen_decade']
LABELS=['Deficit intensity','Cumulative deficit','Candidate number','History span','Pre-onset soil state','Soil recovery']
def setup(figure):
    global OUT,QC,DATA,SD
    OUT=REPO/'outputs/supplementary'/f'figure_{figure:02d}'
    QC=OUT/'qc'; DATA=SD=REPO/'figure_source_data/supplementary'/f'figure_{figure:02d}'
    for part in ['qc','02_FIGURES/PNG','02_FIGURES/PDF','02_FIGURES/SVG']:
        (OUT/part).mkdir(parents=True,exist_ok=True)
def prepare(i):
    panels={}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        patterns=[f'D_Fig{i:02d}{letter}_source_data.csv',f'D_Fig{i:02d}_{letter}.csv']
        for name in patterns:
            p=DATA/name
            if p.is_file(): panels[letter]=pd.read_csv(p)
    return panels
"""Display saved effects and intervals. No fits, correlations or resampling."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.transforms import ScaledTranslation
from audit_panel_alignment import require_matplotlib_panel_alignment
plt.rcParams.update({'font.family':'Times New Roman','font.size':7,'axes.labelsize':7,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'axes.titlesize':8,'axes.linewidth':.55,'axes.spines.right':False,'axes.spines.top':False,'xtick.major.width':.5,'ytick.major.width':.5,'xtick.major.size':2.5,'ytick.major.size':2.5,'pdf.fonttype':42,'svg.fonttype':'none','legend.fontsize':6.5,'legend.frameon':False,'savefig.facecolor':'white'})
PC={'GRUN':'#C08760','ERA5':'#215B84','GLDAS':'#73998B'}
def canvas(rows=2,cols=3,height=190,product_legend=True):
    fig,aa=plt.subplots(rows,cols,figsize=(183/25.4,height/25.4))
    fig.subplots_adjust(left=.13,right=.978,bottom=.15 if rows==2 else .12,top=.90 if rows==2 else .93,wspace=.90 if cols==3 else .46,hspace=.66 if rows==2 else .70)
    if product_legend:fig.legend(handles=[Line2D([],[],color=PC[p],marker='o',ms=3,lw=1,label=p) for p in PRODUCTS],loc='upper center',bbox_to_anchor=(.54,.988),ncol=3,columnspacing=2)
    return fig,aa.ravel()
def label(ax,l,title):
    ax.text(0,1,l,transform=ax.transAxes+ScaledTranslation(-16/72,9/72,ax.figure.dpi_scale_trans),fontweight='bold',fontsize=9,ha='left',va='bottom',clip_on=False)
    ax.set_title(title,loc='left',pad=9);ax.set_label(l)
def note(fig,text):fig.text(.08,.032,text,fontsize=7,linespacing=1.5)
def forest(ax,d,category,values,labels=None,x='beta',lo='CI_low',hi='CI_high',xlabel='Interaction (months / decade)',products=PRODUCTS):
    for j,p in enumerate(products):
        for k,v in enumerate(values):
            q=d[d['product'].eq(p)&d[category].eq(v)]
            if q.empty:continue
            q=q.iloc[0];y=k+(j-(len(products)-1)/2)*.18
            ax.plot([q[lo],q[hi]],[y,y],color=PC[p],lw=1)
            ax.plot(q[x],y,'o',color=PC[p],ms=3)
    ax.axvline(0,color='.5',lw=.6,ls=':');ax.set(yticks=range(len(values)),yticklabels=labels or values,ylim=(len(values)-.5,-.5),xlabel=xlabel)
def finish(fig,i):
    stem=f'D_Fig{i:02d}_{NAMES[i]}';fig.canvas.draw()
    require_matplotlib_panel_alignment(fig,json_out=str(QC/f'{stem}.alignment.json'),tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=True)
    fig.savefig(OUT/f'02_FIGURES/PDF/{stem}.pdf');fig.savefig(OUT/f'02_FIGURES/SVG/{stem}.svg');fig.savefig(OUT/f'02_FIGURES/PNG/{stem}.png',dpi=600)
    fig.savefig(QC/f'{stem}_preview.png',dpi=150)
    plt.close(fig);print(stem+': SCIENTIFIC RECOMPUTATION: NONE')
def render(i):
    d=prepare(i)
    if i==1:
        fig,a=canvas(height=212)
        label(a[0],'a','Spatial explanatory performance')
        vv=['F','S','B','F+S','F+S+B']
        for j,p in enumerate(PRODUCTS):
            q=d['a'][d['a']['product'].eq(p)].set_index('model').loc[vv];y=np.arange(5)+(j-1)*.20
            a[0].plot(q.spatial_block_cv_r2,y,'o',ms=3,color=PC[p]);a[0].plot(q.in_sample_r2,y,'o',ms=3,mfc='white',mec=PC[p])
        a[0].set(yticks=range(5),yticklabels=vv,ylim=(4.6,-.6),xlim=(-.001,.04),xticks=[0,.02,.04],xlabel='R²')
        label(a[1],'b','Nested-model increments')
        for j,p in enumerate(PRODUCTS):
            q=d['b'][d['b']['product'].eq(p)];a[1].plot(q.delta_cv_r2,np.arange(2)+(j-1)*.18,'o',color=PC[p],ms=3)
        a[1].set(yticks=[0,1],yticklabels=['Add S\nto F','Add B\nto F+S'],ylim=(1.5,-.5),xlim=(-.001,.03),xticks=[0,.01,.02,.03],xlabel='Change in CV R²');a[1].axvline(0,color='.5',lw=.6,ls=':')
        label(a[2],'c','GRUN · partial ranks')
        vv=VARS[:2]+['forcing_drought_months_24']+VARS[2:4]+['is_many_to_one']+VARS[4:]
        ll=['Intensity','Deficit','Dry months','Candidates','Span','Many-to-one','Pre-onset soil','Recovery']
        forest(a[2],d['c'],'variable',vv,ll,x='rho',lo='ci_low',hi='ci_high',xlabel='Partial rank association',products=['GRUN'])
        for ax,l,p in zip(a[3:],'def',PRODUCTS):
            label(ax,l,p+' · full model');forest(ax,d[l],'driver',TREND,['Intensity','Deficit','Candidates','Span','Pre-onset soil','Recovery'],x='standardized_beta',lo='ci_low',hi='ci_high',xlabel='Standardized coefficient',products=[p]);ax.set_xlim(-.2,.22)
        fig.legend(handles=[Line2D([],[],color='.3',marker='o',ls='',ms=3,label='Spatial CV'),Line2D([],[],color='.3',marker='o',mfc='white',ls='',ms=3,label='In-sample')],loc='center',bbox_to_anchor=(.51,.502),ncol=2)
        note(fig,'1952–2014 · F: deficit intensity + mass; S: candidate number + span; B: soil state + recovery\nc–f: stored 95% intervals, 500 spatial draws. Event partial ranks (c) differ from grid-trend models (d–f).\nAbsolute CV R² remains low. Pre-fold winsorization limits predictive interpretation; associations are not causal.')
    elif i==2:
        fig,a=canvas(height=182)
        for ax,l,v,title in zip(a,'abcdef',VARS,LABELS):
            label(ax,l,title)
            for p in PRODUCTS:
                q=d[l][d[l]['product'].eq(p)].sort_values('quantile');ax.plot(q['quantile'],q.rho,'o-',ms=3,color=PC[p],lw=1)
            ax.axhline(0,color='.5',lw=.6,ls=':');ax.set(xlim=(5,95),ylim=(-1,1),xticks=[10,50,90],xticklabels=['Q10','Q50','Q90'],yticks=[-1,0,1],xlabel='PT distribution position',ylabel='Across-region Spearman ρ')
        note(fig,'1952–2014 · 44 AR6 regions per product · stored Q10, Q25, Q50, Q75 and Q90 associations\nPT positions are quantiles across grid-year mean PT, not pooled events. Lines guide the eye.\nUnadjusted p values are retained in source data; no association intervals were stored.')
    elif i==3:
        fig,a=canvas(cols=2,height=188,product_legend=False)
        regimes=list(d['a'].regime.drop_duplicates());styles={regimes[0]:('#AA7054','-'),regimes[1]:('#527487','-'),regimes[2]:('#729580','-')}
        for ax,l,title,unit in zip(a[:3],'abc',['Cumulative deficit','Meteorological history span','Soil recovery'],['Deficit mass (index × months)','Onset span (months)','Soil anomaly difference (SD)']):
            label(ax,l,title)
            for reg,(co,ls) in styles.items():
                q=d[l][d[l].regime.eq(reg)].sort_values('year');ax.plot(q.year,q.value,color=co,lw=.8)
            ax.set(xlim=(1952,2014),xticks=[1960,1980,2000],xlabel='Year',ylabel=unit)
        label(a[3],'d','Annual support')
        for reg,(co,ls) in styles.items():
            q=d['d'][d['d'].regime.eq(reg)].sort_values('year');a[3].plot(q.year,q.n_events/1000,color=co,lw=.8);a[3].plot(q.year,q.n_grids/1000,color=co,lw=.8,ls='--')
        a[3].set(xlim=(1952,2014),xticks=[1960,1980,2000],xlabel='Year',ylabel='Events / active grids (thousands)')
        fig.legend(handles=[Line2D([],[],color=co,lw=1,label=reg) for reg,(co,ls) in styles.items()],loc='upper center',bbox_to_anchor=(.54,.985),ncol=3)
        fig.legend(handles=[Line2D([],[],color='.3',lw=1,label='Events'),Line2D([],[],color='.3',lw=1,ls='--',label='Active grids')],loc='center',bbox_to_anchor=(.76,.505),ncol=2)
        note(fig,'GRUN · 1952–2014 · annual equal-grid covariate means; unsmoothed saved values\nPT groups use inclusive annual pooled-event Q10–25, Q45–55 and Q75–90 bands.\nComplete-case cohort: 3,781,190 events, 65,544 grids. No annual uncertainty was saved.')
    elif i==4:
        fig,a=canvas(height=192)
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            label(ax,l,p+' · severity-bin trends')
            for bins,ls,alpha in [(10,'-',.19),(20,'--',.08)]:
                q=d[l][d[l].bins.eq(bins)].sort_values('severity_midpoint');ax.fill_between(q.severity_midpoint,q.CI_low,q.CI_high,color=PC[p],alpha=alpha,lw=0);ax.plot(q.severity_midpoint,q.sen_slope_months_decade,color=PC[p],ls=ls,lw=1)
            ax.axhline(0,color='.5',lw=.6,ls=':');ax.set(xlim=(0,1),ylim=(-.11,.11),xticks=[0,.5,1],xlabel='Within-grid severity rank',ylabel='PT trend (months / decade)')
        for ax,l,p in zip(a[3:],'def',PRODUCTS):
            label(ax,l,p+' · severity definitions');forest(ax,d[l],'model',['main','duration','peak'],['Cumulative','Duration\nadjusted','Peak'],products=[p]);ax.set_xlim(-.25,.035);ax.set_xticks([-.2,-.1,0])
        fig.legend(handles=[Line2D([],[],color='.3',lw=1,label='10 bins'),Line2D([],[],color='.3',lw=1,ls='--',label='20 bins')],loc='center',bbox_to_anchor=(.54,.503),ncol=2)
        note(fig,'1952–2014 · stored 95% intervals from 1,000 spatial block draws · main support ≥30 valid PT events/grid\na–c: equal-grid annual mean trends; d–f: grid fixed-effect time × rank interactions.\nSeverity ranks use the full within-grid catalogue. More-negative trends do not imply shorter absolute PT.')
    elif i==5:
        fig,a=canvas(rows=3,height=266)
        qs=[.1,.25,.5,.75,.9];cl=['#B4BCC2','#8397A5','#215B84','#5A8676','#274C3C']
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            label(ax,l,p+' · conditional PT')
            for qu,c in zip(qs,cl):
                q=d[l][d[l].TP_quantile.eq(qu)].sort_values('severity_decile');ax.plot(q.severity_decile,q.sen_slope_months_decade,color=c,lw=1)
            ax.axhline(0,color='.5',ls=':',lw=.6);ax.set(xticks=[1,5,10],xlim=(.5,10.5),ylim=(-.09,.1),xlabel='Severity decile',ylabel='Trend (months / decade)')
        fig.legend(handles=[Line2D([],[],color=c,lw=1,label=f'Q{int(q*100)}') for q,c in zip(qs,cl)],loc='center',bbox_to_anchor=(.54,.678),ncol=5)
        for ax,l,p in zip(a[3:6],'def',PRODUCTS):
            label(ax,l,p+' · support sensitivity');forest(ax,d[l],'setting',['Common grid','Min 20','Min 30','Min 50'],['Common\ngrid','Min 20','Min 30','Min 50'],x='beta_year_x_severity',products=[p]);ax.set_xlim(-.12,.04);ax.set_xticks([-.1,-.05,0])
        label(a[6],'g','High-minus-low contrasts');forest(a[6],d['g'],'quantile',[.1,.5,.9],['Q10','Q50','Q90'],x='high_minus_low_slope',xlabel='Contrast (months / decade)');a[6].set_xlim(-.16,.04);a[6].set_xticks([-.15,-.075,0])
        label(a[7],'h','Saved paired Q50 draws')
        for p in PRODUCTS:
            q=d['h'][d['h']['product'].eq(p)];a[7].plot(q.replicate,q.contrast,'.',color=PC[p],ms=1.5,alpha=.45)
        a[7].axhline(0,color='.5',lw=.6,ls=':');a[7].set(xlim=(0,501),xticks=[1,250,500],xlabel='Saved replicate',ylabel='Contrast (months / decade)')
        label(a[8],'i','Regional directions')
        q=d['i'].iloc[0];vv=[q.n_AR6_median_beta_negative,q.n_AR6_2of3_negative,q.n_AR6_3of3_negative]
        a[8].plot(vv,range(3),'o',color='.35',ms=4);a[8].set(yticks=range(3),yticklabels=['Median\nnegative','≥2 products\nnegative','3 products\nnegative'],ylim=(2.6,-.6),xlim=(0,44),xticks=[0,22,44],xlabel='AR6 regions (of 44)')
        for j,v in enumerate(vv):a[8].text(v+1.5,j,str(int(v)),va='center',fontsize=7)
        note(fig,'1952–2014 · a–c: stored point estimates; no individual-profile intervals saved\nd–f: 1,000 spatial draws; g–h: 500 paired temporal draws, 5-year blocks.\ni: equal-region direction counts, not area or significance. Product agreement is not independent replication.')
    finish(fig,i)
if __name__=='__main__':render(int(sys.argv[1]))
