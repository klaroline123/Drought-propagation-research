from pathlib import Path
import os,sys,json
import numpy as np
import pandas as pd
REPO=Path(__file__).resolve().parents[1]
PRODUCTS=['GRUN','ERA5','GLDAS']
CLOCKS=['nearest','peak','com']
LAYERS=['rootzone_sm_0_100','deep_sm_100_289','profile_sm_0_289']
NAMES={1:'PT_definitions',2:'paired_references',3:'soil_moisture',4:'timing_perturbation'}
def setup(figure):
    global OUT,QC,DATA,SD
    OUT=REPO/'outputs/supplementary'/f'figure_{figure:02d}'
    QC=OUT/'qc'; DATA=SD=REPO/'figure_source_data/supplementary'/f'figure_{figure:02d}'
    for part in ['qc','02_FIGURES/PNG','02_FIGURES/PDF','02_FIGURES/SVG']:
        (OUT/part).mkdir(parents=True,exist_ok=True)
def prepare(i):
    panels={}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        patterns=[f'B_Fig{i:02d}{letter}_source_data.csv',f'B_Fig{i:02d}_{letter}.csv']
        for name in patterns:
            p=DATA/name
            if p.is_file(): panels[letter]=pd.read_csv(p)
    return panels
"""Figures from saved Block B summaries. No event-level scientific computation."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import LogNorm
from matplotlib.transforms import ScaledTranslation
from audit_panel_alignment import require_matplotlib_panel_alignment
plt.rcParams.update({'font.family':'Times New Roman','font.size':7,'axes.labelsize':7,
 'xtick.labelsize':6.5,'ytick.labelsize':6.5,'axes.titlesize':8,'axes.linewidth':.55,
 'axes.spines.right':False,'axes.spines.top':False,'xtick.major.width':.5,'ytick.major.width':.5,
 'xtick.major.size':2.5,'ytick.major.size':2.5,'pdf.fonttype':42,'svg.fonttype':'none',
 'legend.fontsize':7,'legend.frameon':False,'savefig.facecolor':'white'})
PC={'GRUN':'#C08760','ERA5':'#215B84','GLDAS':'#73998B'}
CC={'nearest':'#577A99','peak':'#BA8055','com':'#357C74'}
CL={'nearest':'Nearest onset','peak':'Selected-event peak','com':'CoM'}
LS={'nearest':'--','peak':':','com':'-'}; MK={'nearest':'o','peak':'s','com':'D'}
LL=['Root zone (0–100 cm)','Deep (100–289 cm)','Profile (0–289 cm)']
def label(ax,l,title):
    t=ax.transAxes+ScaledTranslation(-17/72,8/72,ax.figure.dpi_scale_trans)
    ax.text(0,1,l,transform=t,fontweight='bold',fontsize=9,ha='left',va='bottom',clip_on=False)
    ax.set_title(title,loc='left',pad=8)
    ax.set_label(l)
def legend(fig,y=.97):
    fig.legend(handles=[Line2D([],[],color=CC[k],ls=LS[k],marker=MK[k],ms=3,lw=1,label=CL[k]) for k in CLOCKS],loc='upper center',bbox_to_anchor=(.52,y),ncol=3,handlelength=2.4,columnspacing=2)
def finish(fig,i,exclude=()):
    stem=f'B_Fig{i:02d}_{NAMES[i]}'
    fig.canvas.draw()
    require_matplotlib_panel_alignment(fig,json_out=str(QC/f'{stem}.alignment.json'),tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=True,exclude_axes=list(exclude))
    fig.savefig(OUT/f'02_FIGURES/PDF/{stem}.pdf')
    fig.savefig(OUT/f'02_FIGURES/SVG/{stem}.svg')
    fig.savefig(OUT/f'02_FIGURES/PNG/{stem}.png',dpi=600)
    import shutil
    shutil.copyfile(OUT/f'02_FIGURES/PNG/{stem}.png',QC/f'{stem}_preview.png')
    plt.close(fig)
    print(f'{stem}: SCIENTIFIC RECOMPUTATION: NONE; SOURCE STATUS: VERIFIED WITH NOTES')
def render(i):
    d=prepare(i)
    if i==1:
        fig,aa=plt.subplots(2,2,figsize=(183/25.4,150/25.4))
        fig.subplots_adjust(left=.10,right=.975,bottom=.13,top=.875,wspace=.30,hspace=.48)
        legend(fig);ax=aa[0,0];label(ax,'a','Three temporal reference definitions')
        ax.set_axis_off()
        lines=[('CoM','Positive-deficit temporal average', 'PT = H onset − sum(t × w) / sum(w)'),
               ('Nearest onset','Latest candidate onset', 'PT = H onset − max(candidate onset)'),
               ('Selected-event peak','Peak of greatest-severity candidate', 'PT = H onset − selected peak month')]
        for j,(name,desc,formula) in enumerate(lines):
            y=.91-j*.28;k=CLOCKS[[2,0,1][j]]
            ax.text(0,y,name,color=CC[k],fontweight='bold',fontsize=8)
            ax.text(0,y-.09,desc,fontsize=7)
            ax.text(0,y-.17,formula,fontsize=7)
        ax.text(0,.035,'Definition illustration; no event values shown.',fontsize=6.5,color='.4')
        for ax,l,p in zip([aa[0,1],aa[1,0],aa[1,1]],'bcd',PRODUCTS):
            z=d[l];label(ax,l,f'{p} · n = {int(z.n.iloc[0]):,}')
            ax.axvspan(0,24,color='#E6EBE9',zorder=0)
            for k in CLOCKS:
                q=z[z.clock==k];ax.step(q.bin_right_months,q.cumulative_percent,where='post',color=CC[k],ls=LS[k],lw=1.2)
            ax.set_xscale('symlog',linthresh=24,linscale=1)
            ax.set(xlim=(-100,150),ylim=(0,102),xticks=[-100,-24,0,12,24,150],xticklabels=['−100','−24','0','12','24','150'],yticks=[0,25,50,75,100],xlabel='Interval to H onset (months)',ylabel='Cumulative events (%)')
            ax.title.set_color(PC[p])
        fig.text(.10,.032,'Stored 0.5-month bins · x axis linear within ±24 months, logarithmic outside · shaded: CoM support',fontsize=7)
        finish(fig,i)
    elif i==2:
        fig,aa=plt.subplots(3,2,figsize=(183/25.4,223/25.4))
        fig.subplots_adjust(left=.10,right=.89,bottom=.085,top=.94,wspace=.38,hspace=.62)
        caxes=[]
        for ax,l,k in zip(aa[0],'ab',['nearest','peak']):
            z=d[l];x=np.sort(z.x_left.unique());y=np.sort(z.y_left.unique())
            v=z.pivot(index='x_left',columns='y_left',values='count').loc[x,y].to_numpy()
            xe=np.r_[x,z.x_right.max()];ye=np.r_[y,z.y_right.max()]
            im=ax.pcolormesh(xe,ye,np.ma.masked_less_equal(v.T,0),norm=LogNorm(1,50000),cmap='cividis',rasterized=False,shading='flat')
            ax.plot([0,24],[0,24],ls='--',lw=.7,color='#B95D50')
            ax.set(xlabel=f'{CL[k]} PT (months)',ylabel='CoM PT (months)',ylim=(-.25,24.25))
            label(ax,l,f'ERA5 · {CL[k]} vs CoM')
        bb=aa[0,1].get_position();cbax=fig.add_axes([.915,bb.y0,.012,bb.height]);caxes.append(cbax)
        cb=fig.colorbar(im,cax=cbax,ticks=[1,100,10000]);cb.set_ticklabels(['1','100','10,000']);cb.set_label('Events per saved bin',fontsize=6.5);cb.solids.set_rasterized(False)
        for ax,l,metric,title in [(aa[1,0],'c','rho','Rank correspondence'),(aa[1,1],'d','median_absolute_difference','Absolute event-paired difference')]:
            z=d[l]
            for j,p in enumerate(PRODUCTS):
                for k,off in [('nearest',-.13),('peak',.13)]:
                    q=z[(z['product']==p)&(z.clock==k)].iloc[0]
                    ax.plot(q[metric],j+off,marker=MK[k],mfc='white' if k=='nearest' else PC[p],mec=PC[p],ms=4)
            ax.set(yticks=range(3),yticklabels=PRODUCTS,ylim=(2.5,-.5),xlabel='Spearman ρ' if metric=='rho' else 'Median absolute difference (months)',xlim=(0,1) if metric=='rho' else (0,10))
            label(ax,l,title)
        fig.legend(handles=[Line2D([],[],color='.35',marker='o',mfc='white',ls='',label='Nearest vs CoM'),Line2D([],[],color='.35',marker='s',ls='',label='Peak vs CoM')],loc='center',bbox_to_anchor=(.49,.375),ncol=2,fontsize=6.5)
        for ax,l,k in zip(aa[2],'ef',['nearest','peak']):
            z=d[l];label(ax,l,f'ERA5 · CoM minus {"nearest" if k=="nearest" else "peak"}')
            for st,col,ls in [('Single antecedent','#909AA3','--'),('Multiple antecedents',PC['ERA5'],'-')]:
                q=z[z.structure==st].sort_values('x');ax.step(q.x,q.density,where='mid',color=col,ls=ls,lw=1.1)
            ax.axvline(0,color='.65',lw=.6);ax.set(xlabel='Signed PT difference (months)',ylabel='Probability density (month⁻¹)',xlim=(-105,65))
        fig.legend(handles=[Line2D([],[],color='#909AA3',ls='--',label='Single antecedent (n = 229,358)'),Line2D([],[],color=PC['ERA5'],label='Multiple antecedents (n = 2,906,476)')],loc='lower center',bbox_to_anchor=(.49,.006),ncol=2,fontsize=6.5)
        finish(fig,i,caxes)
    elif i==3:
        fig,aa=plt.subplots(2,3,figsize=(183/25.4,161/25.4))
        fig.subplots_adjust(left=.085,right=.98,bottom=.16,top=.87,wspace=.46,hspace=.65)
        legend(fig)
        lower=min(d[l].lo.min() for l in 'abc')-.035
        upper=max(d[l].hi.max() for l in 'abc')+.035
        for ax,l,title in zip(aa[0],'abc',LL):
            z=d[l];label(ax,l,title)
            for k in CLOCKS:
                q=z[z.clock==k].sort_values('month');ax.fill_between(q.month,q.lo,q.hi,color=CC[k],alpha=.15,lw=0);ax.plot(q.month,q['mean'],color=CC[k],ls=LS[k],lw=1.1)
            ax.axhline(0,color='.65',lw=.55);ax.axvline(0,color='.65',ls=':',lw=.55)
            ax.set(xlim=(-12,12),xticks=[-12,-6,0,6,12],ylim=(lower,upper),xlabel='Months relative to M reference',ylabel='Soil-moisture anomaly (z)')
        for ax,l,title in zip(aa[1],'def',['Distance to soil-deficit CoM','Distance to driest soil month','Observed minus seasonal control']):
            z=d[l];label(ax,l,title)
            for j,k in enumerate(CLOCKS):
                q=z[z.clock==k].set_index('layer').loc[LAYERS];x=q['mean'].to_numpy();lo=q.lo.to_numpy();hi=q.hi.to_numpy()
                ax.errorbar(x,np.arange(3)+(j-1)*.19,xerr=[x-lo,hi-x],color=CC[k],fmt=MK[k],ms=3.3,capsize=1.6,elinewidth=.8,lw=0)
            ax.set(yticks=range(3),yticklabels=['Root zone','Deep','Profile'],ylim=(2.5,-.5),xlabel='Mean absolute distance (months)' if l!='f' else 'Paired distance difference (months)')
            if l=='f':ax.axvline(0,color='.6',lw=.6);ax.set_xlim(-.7,.10)
            else:ax.set_xlim(0,12)
        fig.text(.085,.065,'ERA5 only · a–c: 196,597 events, 400 spatial-block draws · d–f: 189,254 events, 1,000 draws',fontsize=7)
        fig.text(.085,.039,'Bands / error bars: saved 95% intervals · process-consistency evidence; soil moisture is not PT ground truth',fontsize=7)
        finish(fig,i)
    elif i==4:
        fig,aa=plt.subplots(2,2,figsize=(183/25.4,156/25.4))
        fig.subplots_adjust(left=.105,right=.975,bottom=.12,top=.87,wspace=.32,hspace=.53)
        legend(fig)
        for ax,l,p in zip([aa[0,0],aa[0,1],aa[1,0]],'abc',PRODUCTS):
            z=d[l];label(ax,l,f'{p} · fixed matching')
            for k in CLOCKS:
                q=z[z.clock==k].set_index('parent_bin').loc[['1','2','3','4','5+']]
                ax.plot(range(5),q.mean_absolute_change,color=CC[k],ls=LS[k],marker=MK[k],ms=3,lw=1.1)
            ns=z[z.clock=='com'].set_index('parent_bin').loc[['1','2','3','4','5+'],'n']
            ax.set(xticks=range(5),xticklabels=[f'{b}\n{int(n):,}' for b,n in ns.items()],ylim=(0,.55),ylabel='Mean absolute timing change (months)',xlabel='Antecedent count / n events')
            ax.title.set_color(PC[p])
        ax=aa[1,1];label(ax,'d','ERA5 · perturbation amplitude')
        for k in CLOCKS:
            q=d['d'][d['d'].clock==k].sort_values('amplitude');ax.plot(q.amplitude,q.mean_absolute_change,color=CC[k],ls=LS[k],marker=MK[k],ms=3,lw=1.1)
        ax.set(xlim=(.2,1.05),xticks=[.25,.5,1],ylim=(0,.55),xlabel='Uniform-jitter half-width a (months)',ylabel='Mean absolute timing change (months)')
        fig.text(.105,.035,'Independent event shifts · 200 repetitions · means only; source caches contain no uncertainty intervals',fontsize=7)
        finish(fig,i)
if __name__=='__main__':render(int(sys.argv[1]))
