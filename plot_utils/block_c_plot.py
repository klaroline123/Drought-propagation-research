from pathlib import Path
import os,sys,json
import numpy as np
import pandas as pd
REPO=Path(__file__).resolve().parents[1]
PRODUCTS=['GRUN','ERA5','GLDAS']
NAMES={1:'global_mean_reference',2:'quantile_width',3:'multiplicity_standardization',4:'regional_composition',5:'period_coverage',6:'boundary_window'}
def setup(figure):
    global OUT,QC,DATA,SD
    OUT=REPO/'outputs/supplementary'/f'figure_{figure:02d}'
    QC=OUT/'qc'; DATA=SD=REPO/'figure_source_data/supplementary'/f'figure_{figure:02d}'
    for part in ['qc','02_FIGURES/PNG','02_FIGURES/PDF','02_FIGURES/SVG']:
        (OUT/part).mkdir(parents=True,exist_ok=True)
def prepare(i):
    panels={}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        patterns=[f'C_Fig{i:02d}{letter}_source_data.csv',f'C_Fig{i:02d}_{letter}.csv']
        for name in patterns:
            p=DATA/name
            if p.is_file(): panels[letter]=pd.read_csv(p)
    return panels
"""Display-only figures from authoritative stored summaries."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.transforms import ScaledTranslation
from audit_panel_alignment import require_matplotlib_panel_alignment
plt.rcParams.update({'font.family':'Times New Roman','font.size':7,'axes.labelsize':7,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'axes.titlesize':8,'axes.linewidth':.55,'axes.spines.right':False,'axes.spines.top':False,'xtick.major.width':.5,'ytick.major.width':.5,'xtick.major.size':2.5,'ytick.major.size':2.5,'pdf.fonttype':42,'svg.fonttype':'none','legend.fontsize':6.5,'legend.frameon':False,'savefig.facecolor':'white'})
PC={'GRUN':'#C08760','ERA5':'#215B84','GLDAS':'#73998B'}
def label(ax,l,title):
    ax.text(0,1,l,transform=ax.transAxes+ScaledTranslation(-16/72,9/72,ax.figure.dpi_scale_trans),fontweight='bold',fontsize=9,ha='left',va='bottom',clip_on=False)
    ax.set_title(title,loc='left',pad=9);ax.set_label(l)
def canvas(cols=3,height=184):
    fig,aa=plt.subplots(2,cols,figsize=(183/25.4,height/25.4))
    fig.subplots_adjust(left=.115,right=.978,bottom=.15,top=.90,wspace=.82 if cols==3 else .43,hspace=.60)
    fig.legend(handles=[Line2D([],[],color=PC[p],marker='o',ms=3,lw=1,label=p) for p in PRODUCTS],loc='upper center',bbox_to_anchor=(.53,.987),ncol=3,columnspacing=2)
    return fig,aa.ravel()
def note(fig,text):fig.text(.08,.035,text,fontsize=7,linespacing=1.5)
def lines(ax,d,col):
    for p in PRODUCTS:
        q=d[d['product'].eq(p)].sort_values('year');ax.plot(q.year,q[col],color=PC[p],lw=.85)
    ax.set(xlim=(1952,2014),xticks=[1960,1980,2000],xlabel='Year')
def forest(ax,d,category,values,labels=None,x='slope_per_decade',lo='block_ci_low',hi='block_ci_high',xlabel='Trend (months / decade)',products=PRODUCTS):
    for j,p in enumerate(products):
        for k,v in enumerate(values):
            q=d[d['product'].eq(p)&d[category].eq(v)]
            if q.empty:continue
            q=q.iloc[0];y=k+(j-(len(products)-1)/2)*.18
            ax.plot([q[lo],q[hi]],[y,y],color=PC[p],lw=1)
            ax.plot(q[x],y,'o',color=PC[p],ms=3)
    ax.axvline(0,color='.5',lw=.6,ls=':');ax.set(yticks=range(len(values)),yticklabels=labels or values,ylim=(len(values)-.5,-.5),xlabel=xlabel)
def finish(fig,i):
    stem=f'C_Fig{i:02d}_{NAMES[i]}';fig.canvas.draw()
    require_matplotlib_panel_alignment(fig,json_out=str(QC/f'{stem}.alignment.json'),tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=True)
    fig.savefig(OUT/f'02_FIGURES/PDF/{stem}.pdf');fig.savefig(OUT/f'02_FIGURES/SVG/{stem}.svg');fig.savefig(OUT/f'02_FIGURES/PNG/{stem}.png',dpi=600)
    plt.close(fig);print(stem+': SCIENTIFIC RECOMPUTATION: NONE')
def render(i):
    d=prepare(i)
    if i==1:
        fig,a=canvas(2,170)
        label(a[0],'a','Equal-grid annual CoM mean');lines(a[0],d['a'],'mean_PT');a[0].set_ylabel('Mean PT (months)')
        label(a[1],'b','Common-cohort reference trends');forest(a[1],d['b'],'variant',['clock_CoM','clock_nearest','clock_peak'],['CoM','Nearest onset','Selected peak'],lo='ci_low',hi='ci_high')
        label(a[2],'c','Event-weighted mean sensitivity');forest(a[2],d['c'],'variant',['observed_event','fixed_m_event'],['Observed','Fixed mixture'],lo='ci_low',hi='ci_high')
        label(a[3],'d','Paired reference slope differences');forest(a[3],d['d'],'variant',['clock_nearest__minus__clock_CoM','clock_peak__minus__clock_CoM'],['Nearest − CoM','Peak − CoM'],lo='ci_low',hi='ci_high',xlabel='Slope difference (months / decade)')
        note(fig,'1952–2014 · bars: stored 95% residual block intervals (499 draws, 5-year blocks)\nEqual-grid estimates: a, b, d; event-weighted estimates: c. All references end at H onset.')
    elif i==2:
        fig,a=canvas(height=187)
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            q=d[l].sort_values('quantile');label(ax,l,p+' · quantile profile')
            ax.fill_between(q['quantile'],q.ci_low,q.ci_high,color=PC[p],alpha=.2,lw=0);ax.plot(q['quantile'],q.slope,color=PC[p],lw=1)
            ax.axhline(0,color='.5',lw=.6,ls=':');ax.set(xlabel='Event quantile',ylabel='Trend (months / decade)',xticks=[.1,.5,.9],ylim=(-.28,.25))
        label(a[3],'d','Three width measures');forest(a[3],d['d'],'metric',['width_q90_q10','iqr','mad'],['Q90−Q10','IQR','MAD'],x='sen',lo='sen_lo',hi='sen_hi')
        label(a[4],'e','Annual outer width');lines(a[4],d['e'],'width_q90_q10');a[4].set_ylabel('Q90−Q10 (months)')
        label(a[5],'f','Regional clock agreement');z=d['f'];cl=['tau_earliest_onset','tau_nearest_onset','tau_strongest_onset','tau_strongest_peak']
        for j,p in enumerate(PRODUCTS):
            q=z[z['product'].eq(p)].set_index('alternative_clock').loc[cl]
            a[5].plot(q.direction_sign_agreement,np.arange(4)+(j-1)*.18,'o',color=PC[p],ms=3)
        a[5].set(xlim=(-.03,1.03),xticks=[0,.5,1],yticks=range(4),yticklabels=['Earliest\nonset','Nearest\nonset','Strongest\nonset','Strongest\npeak*'],ylim=(3.6,-.6),xlabel='Direction agreement (fraction)')
        note(fig,'1952–2014 · a–c: pointwise 500-draw block intervals; d: ordinary Sen intervals\nf: widths across grid-year means within AR6 regions; zero slopes excluded from agreement.\n*Strongest-peak clock ends at H peak. Agreement varies by reference and is not significance.')
    elif i==3:
        fig,a=canvas(height=191)
        vv=['observed','fixed_m_full','exact_m_common_observed','exact_m_fixed','multiplicity_residual'];ll=['Observed','Fixed 4','Exact\nobserved','Exact\nfixed','OLS\nresidual']
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            label(ax,l,p+' · outer-width trends');forest(ax,d[l],'variant',vv,ll,products=[p]);ax.set_xlim(-.40,.11)
        label(a[3],'d','Saved slope attenuation');z=d['d']
        for j,p in enumerate(PRODUCTS):
            q=z[z['product'].eq(p)].iloc[0];a[3].plot([q.binned_attenuation_percent,q.exact_attenuation_percent],[j-.12,j+.12],color=PC[p],lw=.7);a[3].plot(q.binned_attenuation_percent,j-.12,'o',color=PC[p],ms=4);a[3].plot(q.exact_attenuation_percent,j+.12,'s',mfc='white',mec=PC[p],ms=4)
        a[3].set(yticks=range(3),yticklabels=PRODUCTS,ylim=(2.5,-.5),xlim=(0,100),xticks=[0,50,100],xlabel='Attenuation (%)');fig.legend(handles=[Line2D([],[],color='.3',marker='o',ls='',label='Four strata'),Line2D([],[],color='.3',marker='s',mfc='white',ls='',label='Exact m')],loc='center',bbox_to_anchor=(.53,.493),ncol=2,fontsize=6.5)
        label(a[4],'e','Fixed-mixture central widths');forest(a[4],d['e'],'metric',['IQR','MAD'])
        label(a[5],'f','GRUN · annual outer widths')
        for v,ls,la in [('observed','-','Observed'),('fixed_m_full','--','Fixed 4'),('exact_m_fixed',':','Exact fixed')]:
            q=d['f'][d['f'].variant.eq(v)].sort_values('year');a[5].plot(q.year,q.Q90_Q10,color=PC['GRUN'],ls=ls,lw=1,label=la)
        a[5].set(xlabel='Year',ylabel='Q90−Q10 (months)',xticks=[1960,1980,2000]);a[5].legend(loc='upper right')
        note(fig,'1952–2014 · pooled event distributions · stored 95% block intervals (499 draws)\nExact m = 1–7 uses restricted observed support. Attenuation is descriptive, not a causal fraction.\nResidual analysis adjusts annual width for annual mean multiplicity; first-stage uncertainty is not propagated.')
    elif i==4:
        fig,a=canvas(height=292);fig.subplots_adjust(hspace=.32,bottom=.12,top=.93)
        regions=sorted(d['a'].ar6)
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            q=d[l].set_index('ar6').loc[regions];label(ax,l,p+' · regional widths');ax.plot(q.sen_dec,range(44),'o',color=PC[p],ms=2.6)
            ax.axvline(0,color='.5',lw=.6,ls=':');ax.set(yticks=range(44),yticklabels=regions,ylim=(43.7,-.7),xlim=(-1.6,.9),xticks=[-1.5,-.5,.5],xlabel='Trend (months / decade)')
        label(a[3],'d','Common-region weighting');forest(a[3],d['d'],'variant',['common_region_observed','fixed_region'],['Observed','Fixed weights'])
        label(a[4],'e','Mean regional width');forest(a[4],d['e'],'metric',['mean_regional_width','mean_common_regional_width'],['Available\nregions','Common\nregions'])
        label(a[5],'f','Variance components');forest(a[5],d['f'],'metric',['within_variance','between_variance'],['Within','Between'],xlabel='Trend (months² / decade)')
        note(fig,'1952–2014 · a–c: W24 sampled widths across grid-year means in 44 AR6 regions; direction only\nd–f: stored 95% block intervals. d: weights fixed on common-region event support (including UNASSIGNED).\ne: arithmetic average of regional widths, not the width of an equal-region mixture. f: variance, not quantile width.')
    elif i==5:
        fig,a=canvas(height=194)
        periods=['1952-2014','1952-1978','1979-2014']
        for ax,l,p in zip(a[:3],'abc',PRODUCTS):
            label(ax,l,p+' · period dependence');q=d[l]
            for k,v in enumerate(['all','stable80']):
                for j,per in enumerate(periods):
                    r=q[q.variant.eq(v)&q.period.eq(per)].iloc[0];y=j+(k-.5)*.24;ax.plot([r.block_ci_low,r.block_ci_high],[y,y],color=PC[p],lw=1);ax.plot(r.slope_per_decade,y,'o' if k==0 else 's',color=PC[p],mfc=PC[p] if k==0 else 'white',ms=3.5)
            ax.axvline(0,color='.5',ls=':',lw=.6);ax.set(yticks=range(3),yticklabels=['1952–2014','1952–1978','1979–2014'],ylim=(2.5,-.5),xlim=(-1.05,.5),xticks=[-1,-.5,0,.5],xlabel='Trend (months / decade)')
        fig.legend(handles=[Line2D([],[],color='.4',marker='o',ls='',label='All valid PT events'),Line2D([],[],color='.4',marker='s',mfc='white',ls='',label='Stable80 grids')],loc='center',bbox_to_anchor=(.53,.493),ncol=2)
        label(a[3],'d','Input coverage strata');forest(a[3],d['d'],'variant',['coverage_complete','coverage_incomplete'],['Complete','Incomplete'])
        label(a[4],'e','Annual PT-grid support')
        for p in PRODUCTS:
            q=d['e'][d['e']['product'].eq(p)].sort_values('year');a[4].plot(q.year,q.valid_PT_grid_count/1000,color=PC[p],lw=.9);a[4].plot(q.year,q.stable_active_grid_count/1000,color=PC[p],lw=.9,ls='--')
        a[4].set(xlabel='Year',ylabel='Grids (thousands)',xticks=[1960,1980,2000])
        label(a[5],'f','Annual event support')
        for p in PRODUCTS:
            q=d['f'][d['f']['product'].eq(p)].sort_values('year');a[5].plot(q.year,q.valid_PT_event_count/1000,color=PC[p],lw=.9);a[5].plot(q.year,q.all_HD_event_count/1000,color=PC[p],lw=.9,ls=':')
        a[5].set(xlabel='Year',ylabel='Events (thousands)',xticks=[1960,1980,2000])
        note(fig,'a–d: event Q90−Q10 trends with stored 95% block intervals · d: 1952–2014\nStable80: complete 780-month inputs; ≥51 / 22 / 29 active PT years (full / early / late); ≥30 PT events.\ne: solid, all PT grids; dashed, active stable80 grids. f: solid, valid PT events; dotted, all H events.')
    else:
        fig,a=canvas(height=190)
        label(a[0],'a','Distance from the upper bound');lines(a[0],d['a'],'gap90');a[0].set_ylabel('24 − Q90 (months)')
        label(a[1],'b','Near-bound occupancy')
        for p in PRODUCTS:
            q=d['b'][d['b']['product'].eq(p)].sort_values('year')
            for v,ls in [('frac_within_1m',':'),('frac_within_2m','--'),('frac_within_3m','-')]:a[1].plot(q.year,q[v],color=PC[p],ls=ls,lw=.8)
        a[1].set(xlabel='Year',ylabel='Fraction of valid PT events',xticks=[1960,1980,2000],ylim=(0,.03));a[1].legend(handles=[Line2D([],[],color='.3',ls=ls,label=str(n)+' month'+('' if n==1 else 's')) for n,ls in [(1,':'),(2,'--'),(3,'-')]],loc='upper right',fontsize=6.5)
        label(a[2],'c','Occupancy–width association')
        for j,p in enumerate(PRODUCTS):
            q=d['c'][d['c']['product'].eq(p)].iloc[0];a[2].plot(q.spearman_rho,j-.12,'o',color=PC[p],ms=4);a[2].plot(q.detrended_spearman_rho,j+.12,'s',mfc='white',mec=PC[p],ms=4)
        a[2].set(yticks=range(3),yticklabels=PRODUCTS,ylim=(2.5,-.5),xlim=(0,1),xticks=[0,.5,1],xlabel='Spearman ρ');a[2].legend(handles=[Line2D([],[],color='.3',marker='o',ls='',label='Raw'),Line2D([],[],color='.3',marker='s',mfc='white',ls='',label='Detrended')],loc='lower left')
        for ax,l,p in zip(a[3:],'def',PRODUCTS):
            label(ax,l,p+' · range sensitivity');q=d[l]
            for j,per in enumerate(['1952-2014','1953-2014']):
                r=q[q.period.eq(per)].sort_values('window_months');x=r.window_months+(j-.5)*.8
                ax.vlines(x,r.ci_low,r.ci_high,color=PC[p],lw=.8);ax.plot(x,r.slope_per_decade,'o' if j==0 else 's',mfc=PC[p] if j==0 else 'white',mec=PC[p],ms=3.5)
            ax.axhline(0,color='.5',lw=.6,ls=':');ax.set(xlabel='History range (months)',ylabel='Trend (months / decade)',xticks=[18,24,30,36],ylim=(-.4,.16))
        note(fig,'a–c: full frozen 24-month CoM cohort, 1952–2014; c: occupancy within 3 months vs Q90−Q10\nd–f: pooled-event Q90−Q10 in the existing AR6 sample; stored 95% block intervals\nFilled circles: 1952–2014; open squares: saved 1953–2014 sensitivity. Window effects are not eliminated.')
    finish(fig,i)
