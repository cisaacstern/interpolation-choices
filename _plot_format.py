
def _format(fig, ax, title, 
            m=0.02, bgc='w', axc='k', lblc='k', 
            cloud=False, last_frame=False,):
    ax.margins(m)
    ax.set_aspect(aspect=1)
    if last_frame==True:
        ax.set_xlabel('Easting, m (+32097)')
    ax.set_ylabel('Northing, m (+416814)')
    ax.set_title(title, color=axc, loc='left', pad=20)
    ax.xaxis.label.set_color(lblc)
    ax.yaxis.label.set_color(lblc)
    ax.tick_params(axis='x', colors=lblc)
    ax.tick_params(axis='y', colors=lblc)
    ax.spines['bottom'].set_color(axc)
    ax.spines['top'].set_color(axc) 
    ax.spines['right'].set_color(axc)
    ax.spines['left'].set_color(axc)
    ax.set_facecolor(bgc)
    fig.patch.set_facecolor(bgc)
    if cloud == True:
        xs = [320977, 320978, 320979, 320980]
        ys = [4168144, 4168145, 4168146, 4168147]
        ax.set_xticks(xs)
        ax.set_yticks(ys)
        ax.set_xticklabels([x - 320970 for x in xs])
        ax.set_yticklabels([y - 4168140 for y in ys])
    else:
        xs = [0, 44, 88, 132]
        ys = [0, 44, 88, 132]
        ax.set_xticks(xs)
        ax.set_yticks(ys)
        ax.set_xticklabels([7, 8, 9, 10])
        ax.set_yticklabels([4, 5, 6, 7])
    return ax