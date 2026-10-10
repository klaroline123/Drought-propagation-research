from pathlib import Path
import os,sys,json
import numpy as np
import pandas as pd
REPO=Path(__file__).resolve().parents[1]
PRODUCTS=['GRUN','ERA5','GLDAS']
NAMES={1:'target_support',2:'lead_auc',3:'usable_lead',4:'retrospective_prospective',5:'threshold_sensitivity'}
def setup(figure):
    global OUT,QC,DATA,SD
    OUT=REPO/'outputs/supplementary'/f'figure_{figure:02d}'
    QC=OUT/'qc'; DATA=SD=REPO/'figure_source_data/supplementary'/f'figure_{figure:02d}'
    for part in ['qc','02_FIGURES/PNG','02_FIGURES/PDF','02_FIGURES/SVG']:
        (OUT/part).mkdir(parents=True,exist_ok=True)
def prepare(i):
    panels={}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        patterns=[f'E_Fig{i:02d}{letter}_source_data.csv',f'E_Fig{i:02d}_{letter}.csv']
        for name in patterns:
            p=DATA/name
            if p.is_file(): panels[letter]=pd.read_csv(p)
    return panels
"""Plot stored corrected-branch outputs only. No model, AUC, L* or trend estimation."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.transforms import ScaledTranslation
from audit_panel_alignment import require_matplotlib_panel_alignment
plt.rcParams.update({'font.family':'Times New Roman','font.size':7,'axes.labelsize':7,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'axes.titlesize':8,'axes.linewidth':.55,'axes.spines.right':False,'axes.spines.top':False,'xtick.major.width':.5,'ytick.major.width':.5,'xtick.major.size':2.5,'ytick.major.size':2.5,'pdf.fonttype':42,'svg.fonttype':'none','legend.fontsize':6.5,'legend.frameon':False,'savefig.facecolor':'white'})
PC={'GRUN':'#C08760','ERA5':'#215B84','GLDAS':'#73998B'}
def canvas(cols=3,height=185,legend=True):
    f,a=plt.subplots(2,cols,figsize=(183/25.4,height/25.4));f.subplots_adjust(left=.12,right=.978,bottom=.15,top=.90,wspace=.80 if cols==3 else .48,hspace=.63)
    if legend:f.legend(handles=[Line2D([],[],color=PC[p],marker='o',ms=3,lw=1,label=p) for p in PRODUCTS],loc='upper center',bbox_to_anchor=(.54,.988),ncol=3)
    return f,a.ravel()
def label(ax,l,title):
    ax.text(0,1,l,transform=ax.transAxes+ScaledTranslation(-16/72,9/72,ax.figure.dpi_scale_trans),fontsize=9,fontweight='bold',ha='left',va='bottom',clip_on=False);ax.set_title(title,loc='left',pad=9);ax.set_label(l)
def note(f,s):f.text(.07,.032,s,fontsize=7,linespacing=1.5)
def finish(f,i):
    stem=f'E_Fig{i:02d}_{NAMES[i]}';f.canvas.draw()
    require_matplotlib_panel_alignment(f,json_out=str(QC/f'{stem}.alignment.json'),tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=True)
    for ext in ['pdf','svg']:f.savefig(OUT/f'02_FIGURES/{ext.upper()}/{stem}.{ext}')
    f.savefig(OUT/f'02_FIGURES/PNG/{stem}.png',dpi=600);f.savefig(QC/f'{stem}_preview.png',dpi=150);plt.close(f)
    print(stem+': SCIENTIFIC RECOMPUTATION: NONE; MODEL REFITTING: NONE')
def render(i):
    d=prepare(i)
    if i==1:
        f,a=canvas(cols=2,height=182)
        label(a[0],'a','Issue time and future-onset target')
        ax=a[0];ax.axhline(0,xmin=.04,xmax=.97,color='.6',lw=.6);ax.plot([-23,0],[.6,.6],color='#73998B',lw=3);ax.text(-21,.77,'Trailing predictors through t',fontsize=7)
        ax.plot([0,12],[0,0],color='#215B84',lw=2);ax.plot(0,0,'o',mfc='white',mec='#215B84',ms=5);ax.plot(12,0,'o',color='#215B84',ms=5)
        ax.text(3,.18,'(t, t + L]',fontsize=7);ax.text(-21,-.55,'O(t,L) = 1 if ≥1 eligible onset\nin the future interval; otherwise 0.',fontsize=7,linespacing=1.5)
        ax.set(xlim=(-25,14),ylim=(-1.1,1.15),xticks=[-23,0,12],xticklabels=['t − 23','t','t + 12'],yticks=[],xlabel='Month relative to issuance (L = 12 illustrated)');ax.spines['left'].set_visible(False)
        label(a[1],'b','Saved expanding training chronology');q=d['b'][d['b']['product'].eq('GRUN')]
        a[1].fill_between(q.test_year,q.training_start,q.training_end,color='.8',lw=0);a[1].plot(q.test_year,q.training_end,color='.3',lw=1);a[1].plot(q.test_year,q.test_year,'o',ms=2,color=PC['GRUN']);a[1].set(xlabel='Evaluation year',ylabel='Calendar year',xticks=[1986,2000,2013],yticks=[1952,1980,2000,2013],ylim=(1950,2016));a[1].text(.05,.1,'Training: 1952 through y − 6\nEvaluation: year y',transform=a[1].transAxes,fontsize=7,linespacing=1.5)
        label(a[2],'c','Reported pipeline grid support')
        label(a[3],'d','Reported issue–lead record totals')
        for j,p in enumerate(PRODUCTS):
            q=d['c'][d['c']['product'].eq(p)].iloc[0];a[2].plot(q.n_grids_used/1000,j,'o',color=PC[p],ms=4);a[2].text(q.n_grids_used/1000+.4,j,f'{q.n_grids_used:,}',va='center',fontsize=7)
            q=d['d'][d['d']['product'].eq(p)].iloc[0];a[3].plot(q.n_pos/1e6,j-.12,'o',color=PC[p],ms=4);a[3].plot(q.n_neg_kept/1e6,j+.12,'o',mfc='white',mec=PC[p],ms=4)
        a[2].set(yticks=range(3),yticklabels=PRODUCTS,ylim=(2.5,-.5),xlim=(57,70),xlabel='Pipeline grids (thousands)')
        a[3].set(yticks=range(3),yticklabels=PRODUCTS,ylim=(2.5,-.5),xlim=(0,125),xlabel='Issue–lead records (millions)')
        f.legend(handles=[Line2D([],[],color='.3',marker='o',ls='',label='Positive'),Line2D([],[],color='.3',marker='o',mfc='white',ls='',label='Retained negative')],loc='center',bbox_to_anchor=(.75,.495),ncol=2)
        note(f,'Leads L = 1–12 months · evaluation 1986–2013 · c–d: saved pipeline totals, not per-lead sample counts\nAll positives retained; 25% negative sampling. d counts repeat issuance months across leads.\nTraining-only scaling does not remove retrospective catalogue, support and eventual-severity information.')
    elif i==2:
        f,a=canvas(height=192)
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            label(ax,l,p+' · all severity deciles')
            for de in range(1,11):
                q=d[l][d[l].decile.eq(de)].sort_values('lead');co='#215B84' if de==1 else '#73998B' if de==10 else '.72';ax.plot(q.lead,q.auc,color=co,lw=1.2 if de in [1,10] else .55,ls='--' if de==1 else '-',zorder=3 if de in [1,10] else 1)
            ax.axhline(.5,color='.4',ls=':',lw=.6);ax.set(xlim=(.6,12.4),ylim=(.48,.73),xticks=[1,6,12],yticks=[.5,.6,.7],xlabel='Forecast lead L (months)',ylabel='Pooled decile AUC')
        f.legend(handles=[Line2D([],[],color='#215B84',ls='--',lw=1,label='Decile 1'),Line2D([],[],color='.72',lw=.8,label='Deciles 2–9'),Line2D([],[],color='#73998B',lw=1,label='Decile 10')],loc='center',bbox_to_anchor=(.55,.5),ncol=3)
        for ax,l,p in zip(a[3:],'def',PRODUCTS):
            label(ax,l,p+' · equal-decile average');q=d[l].sort_values('lead')
            ax.fill_between(q.lead,q.decile_min,q.decile_max,color='.85',lw=0);ax.fill_between(q.lead,q.ci_low,q.ci_high,color=PC[p],alpha=.30,lw=0);ax.plot(q.lead,q.auc,color=PC[p],lw=1.2)
            ax.axhline(.5,color='.4',ls=':',lw=.6);ax.set(xlim=(.6,12.4),ylim=(.48,.73),xticks=[1,6,12],yticks=[.5,.6,.7],xlabel='Forecast lead L (months)',ylabel='Macro-average AUC')
        note(f,'1986–2013 · a–c: all 10 deciles; no individual-decile AUC intervals saved\nd–f: colored band = 95% interval, 400 paired 4-year histogram draws; gray = stored decile min–max\nAUC is discrimination of eventual onset versus sampled negatives, not calibrated occurrence probability.')
    elif i==3:
        f,a=canvas(height=192)
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            label(ax,l,p+' · pooled usable lead');q=d[l].sort_values('decile');ax.fill_between(q.decile,q.ci_low,q.ci_high,color=PC[p],alpha=.25,lw=0);ax.plot(q.decile,q.Lstar,'o-',ms=3,color=PC[p],lw=1)
            for y in [0,12]:ax.axhline(y,color='.6',ls=':',lw=.6)
            ax.set(xlim=(.5,10.5),ylim=(-.6,12.6),xticks=[1,5,10],yticks=[0,6,12],xlabel='Eventual-severity decile',ylabel='Usable lead L* (months)')
        for ax,l,p in zip(a[3:],'def',PRODUCTS):
            label(ax,l,p+' · annual usable lead')
            for group,ls in [('LOW',':'),('MID','--'),('HIGH','-')]:
                q=d[l][d[l].group.eq(group)].sort_values('year');ax.plot(q.year,q.Lstar,color=PC[p],ls=ls,lw=1,marker='o' if group=='HIGH' else None,ms=2)
            for y in [0,12]:ax.axhline(y,color='.6',ls=':',lw=.6)
            ax.set(xlim=(1985,2014),ylim=(-.6,12.6),xticks=[1986,2000,2013],yticks=[0,6,12],xlabel='Evaluation year',ylabel='Usable lead L* (months)')
        f.legend(handles=[Line2D([],[],color='.3',ls=ls,lw=1,label=label_) for ls,label_ in [(':','LOW: deciles 1–5'),('--','MID: 6–8'),('-','HIGH: 9–10')]],loc='center',bbox_to_anchor=(.54,.5),ncol=3)
        note(f,'Primary AUC threshold T = 0.60 · dotted bounds: analysis floor 0 and evaluated-lead cap 12 months\na–c: 400-draw pooled-decile intervals; d–f: saved annual group values, no annual intervals supplied\nL* uses the last qualifying lead with adjacent-lead interpolation; the GRUN floor is not zero physical warning.')
    elif i==4:
        f,a=canvas(cols=2,height=188)
        for ax,l,title in zip(a,'abcd',['Retrospective PT components','Prospective L* components','Retrospective high − low','Prospective high − low']):label(ax,l,title);ax.axvline(0,color='.6',ls=':',lw=.6);ax.set(yticks=range(3),yticklabels=PRODUCTS,ylim=(2.5,-.5),xlabel='Trend (months / decade)')
        for j,p in enumerate(PRODUCTS):
            for panel,category,vals,x,lo,hi in [('a','severity_decile',[1,10],'slope','CI_low','CI_high'),('b','group',['LOW','HIGH'],'value','ci_low','ci_high')]:
                ax=a[0 if panel=='a' else 1]
                for k,v in enumerate(vals):
                    q=d[panel][d[panel]['product'].eq(p)&d[panel][category].eq(v)].iloc[0];y=j+(k-.5)*.27;ax.plot([q[lo],q[hi]],[y,y],color=PC[p],lw=1);ax.plot(q[x],y,'o',ms=4,color=PC[p],mfc='white' if k==0 else PC[p])
            for ax,l,col in [(a[2],'c','retro_gradient'),(a[3],'d','prospective_gradient')]:
                q=d[l][d[l]['product'].eq(p)].iloc[0];ax.plot(q[col],j,'o',ms=4,color=PC[p]);ax.annotate(f'{q[col]:+.4f}',(q[col],j),xytext=(5,7),textcoords='offset points',fontsize=7)
        a[0].set_xlim(-.10,.065);a[1].set_xlim(-.52,.88);a[2].set_xlim(-.09,.015);a[3].set_xlim(-.1,.92)
        a[2].set_xlabel('PT trend contrast (months / decade)');a[3].set_xlabel('L* trend contrast (months / decade)')
        f.legend(handles=[Line2D([],[],color='.3',marker='o',mfc='white',ls='',label='Low'),Line2D([],[],color='.3',marker='o',ls='',label='High')],loc='center',bbox_to_anchor=(.54,.5),ncol=2)
        note(f,'Retrospective: 1952–2014, decile 10 versus 1; prospective: 1986–2013, HIGH (9–10) versus LOW (1–5)\na–b: component 95% intervals (spatial bootstrap / ordinary Sen); c–d: stored contrasts, no contrast CI supplied\nDifferent periods, rank populations and groups: directional comparison only. T = 0.60; no new correlation.')
    elif i==5:
        f,a=canvas(height=197)
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            label(ax,l,p+' · threshold sensitivity');q=d[l].sort_values('threshold');ax.vlines(q.threshold,q.ci_low,q.ci_high,color=PC[p],lw=.9);ax.plot(q.threshold,q.slope,'o-',color=PC[p],ms=3,lw=1);ax.axhline(0,color='.5',lw=.6,ls=':');ax.axvline(.6,color='.7',lw=.6,ls='--');ax.set(xticks=[.55,.60,.65],xlim=(.54,.66),ylim=(-.7,2.2),xlabel='AUC threshold T',ylabel='HIGH L* trend (months / decade)')
        for ax,l,p in zip(a[3:],'def',PRODUCTS):
            label(ax,l,p+' · fixed-lead sensitivity');q=d[l].sort_values('lead');ax.vlines(q.lead,q.ci_low,q.ci_high,color=PC[p],lw=.8);ax.plot(q.lead,q.slope,'o-',ms=3,color=PC[p],lw=1);ax.axhline(0,color='.5',ls=':',lw=.6);ax.set(xticks=[1,3,6,9,12],xlim=(.5,12.5),ylim=(-.022,.031),xlabel='Forecast lead L (months)',ylabel='HIGH AUC trend (per decade)')
        note(f,'1986–2013 · HIGH = eventual-event deciles 9–10 · all bars: stored ordinary 95% Sen intervals\na–c: five predefined analysis thresholds; dashed line marks primary T = 0.60. No threshold optimization.\nd–f: fixed-L AUC trends, independent of the L* threshold definition. No scientific recomputation.')
    finish(f,i)
if __name__=='__main__':render(int(sys.argv[1]))
