from contextlib import contextmanager
import matplotlib.pyplot as plt 
import pandas as pd

def make_cpi(pkg):
    # Convert CPI to be referenced to current dollars
    cpi=pkg.reference('cpi').dataframe()
    cpi['date'] = pd.to_datetime(cpi.DATE)
    cpiy = cpi.groupby(cpi.date.dt.year).CPIAUCSL.mean()
    cpiy = (cpiy/cpiy.max()).reset_index()
    cpiy.columns = ['year','cpi']
    return cpiy

@contextmanager
def new_plot(title, source=None, figsize=(10,8), xlabel=None, ylabel=None, x_label_rot=0, y_label_rot=90,
            panes=1):
    
    
    
    if panes == 1:
        fig, ax = plt.subplots(figsize=figsize)
    elif panes == 2:
        fig, ax = plt.subplots(2, figsize=figsize)
    elif panes == 3:
        fig = plt.figure(figsize=figsize)
        ax = [
            plt.subplot2grid((2, 2), (0, 0)),
            plt.subplot2grid((2, 2), (0, 1)),
            plt.subplot2grid((2, 2), (1, 0), colspan=2)
        ]
    else:
        fig, ax = plt.subplots(panes, figsize=figsize)
    
    fig.suptitle(title, fontsize=20)
    
    yield fig, ax
    
    if panes==1:
        ax = [ax]
        
    if isinstance(xlabel, str):
        xlabel = [xlabel]*len(ax)
    if isinstance(ylabel, str):
        ylabel = [ylabel]*len(ax)
    
    if source: 

        fig.text(1,0, "Source: "+source, horizontalalignment='right',verticalalignment='top')
        #fig.text(1,-.18, "Source: "+source,
        #    horizontalalignment='right',verticalalignment='top', transform=ax.transAxes)
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    for a,x,y in zip(ax, xlabel, ylabel):
        if x:
            a.set_xlabel(x, rotation=x_label_rot)

        if y:
            a.set_ylabel(y, rotation=y_label_rot)