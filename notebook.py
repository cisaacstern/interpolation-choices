# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#With-sunposition" data-toc-modified-id="With-sunposition-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>With sunposition</a></span></li><li><span><a href="#Vertical-version" data-toc-modified-id="Vertical-version-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Vertical version</a></span></li></ul></div>

# +
import os

import numpy as np
from scipy import ndimage
from scipy.io import savemat
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from interpolate import Interpolate
from sunposition import Sunposition
from _plot_format import _format
import config as c
# -

files = os.listdir('data')

# # With sunposition

sp = Sunposition(
        local_timezone=c.TIMEZONE,
        date_str=files[0][:8],
        lat_lon=c.LAT_LON,)
azi = sp.sunposition_df['azimuth'].iloc[0]

# +
# with sunposition
fig = plt.figure(figsize=(8.5,11)) 

gs = GridSpec(4, 3, figure=fig)

# 1--------------------------------------------------------------------------------
# pointcloud imshow
ax1 = fig.add_subplot(gs[0, :1])
pointcloud = Interpolate(filename=files[0], bounds=c.BOUNDS)
xyz = pointcloud.xyz
ax1.scatter(x=xyz[:,0], y=xyz[:,1], c=xyz[:,2], s=0.5, cmap='viridis')
ax1 = _format(fig=fig, ax=ax1, title="LiDAR Pointcloud", cloud=True)

# pointcloud cross-section
ax2 = fig.add_subplot(gs[0, 1:])

# TODO replace this with a description block
x = np.linspace(0, 10, 1000)
ax2.plot(x, np.sin(x))

# 2--------------------------------------------------------------------------------
# (no blur)
ax3 = fig.add_subplot(gs[1, :1])
res = int(np.ceil(np.sqrt(pointcloud.xyz.shape[0])))
grid = pointcloud.interpolate_grid(xyz=pointcloud.xyz, res=res, method='nearest')
ax3.imshow(grid, origin='lower')
ax3 = _format(fig=fig, ax=ax3, title="NN Interpolation ($\sigma$=0)")

# (no blur) - cross-section
ax4 = fig.add_subplot(gs[1, 1:])
grid_rot = ndimage.rotate(grid, azi, reshape=True)
y = grid_rot[120, :]
y = y[y != 0]
x = np.arange(0, y.shape[0])
ax4.plot(x, y)

# 3--------------------------------------------------------------------------------
# (sigma = 1 blur)
ax5 = fig.add_subplot(gs[2, :1])
sig1 = ndimage.gaussian_filter(grid, sigma=1)
ax5.imshow(sig1, origin='lower')
ax5 = _format(fig=fig, ax=ax5, title="NN Interpolation ($\sigma$=1)")


# (sigma = 1 blur) cross section
ax6 = fig.add_subplot(gs[2, 1:])
grid_rot = ndimage.rotate(sig1, azi, reshape=True)
y = grid_rot[120, :]
y = y[y != 0]
x = np.arange(0, y.shape[0])
ax6.plot(x, y)

# 4--------------------------------------------------------------------------------

ax7 = fig.add_subplot(gs[3, :1])
sig2 = ndimage.gaussian_filter(grid, sigma=2)
ax7.imshow(sig2, origin='lower')
ax7 = _format(fig=fig, ax=ax7, title="NN Interpolation ($\sigma$=2)", last_frame=True)

ax8 = fig.add_subplot(gs[3, 1:])
grid_rot = ndimage.rotate(sig2, azi, reshape=True)
y = grid_rot[120, :]
y = y[y != 0]
x = np.arange(0, y.shape[0])
ax8.plot(x, y)

plt.subplots_adjust(hspace=0.6)

plt.show()
# -

#

# # Vertical version

xyz.shape

# +
# with sunposition

for i in range(0,132):
    vline_x = i

    fig = plt.figure(figsize=(12,10)) 
    gs = GridSpec(3, 3, figure=fig)

    pointcloud = Interpolate(filename=files[0], bounds=c.BOUNDS)
    xyz = pointcloud.xyz

    # 2-4-------------------------------------------------------------------------------
    resolution = int(np.ceil(np.sqrt(pointcloud.xyz.shape[0])))

    ax3 = fig.add_subplot(gs[0, :1])
    ax4 = fig.add_subplot(gs[0, 1:])
    ax5 = fig.add_subplot(gs[1, :1])
    ax6 = fig.add_subplot(gs[1, 1:])
    ax7 = fig.add_subplot(gs[2, :1])
    ax8 = fig.add_subplot(gs[2, 1:])

    def plot_interpolation(ax, s, vline_x, r=resolution):
        grid = pointcloud.interpolate_grid(xyz=pointcloud.xyz, res=r, method='nearest')
        grid = ndimage.gaussian_filter(grid, sigma=s)
        ax.imshow(grid, origin='lower')
        ax.axvline(x=vline_x, color='darkviolet')
        ax = _format(fig=fig, ax=ax, title=f"Interpolation ($\sigma$={s})")
        return grid

    # cross-section

    def plot_cross_section(ax, grid, vline_x, s):
        y = grid[vline_x, :]
        x = np.arange(0, 132)
        ax.plot(x, y, color='darkviolet')
        ax.set_ylim(bottom=2945, top=2946)
        ax.set_ylabel('Elevation, m')
        ax.set_xlabel('Northing, m (+4168140)')
        ax.set_title(f'Cross section at Easting={np.around((vline_x/44)+32097, decimals=2)}m ($\sigma$={s})', 
                     loc='left', pad=10, size=14)
        ax.margins(0)
        xs = [0, 44, 88, 132]
        ax.set_xticks(xs)
        ax.set_xticklabels([4, 5, 6, 7])

    sig0 = plot_interpolation(ax=ax3, s=0, vline_x=vline_x)
    sig1 = plot_interpolation(ax=ax5, s=1, vline_x=vline_x)
    sig2 = plot_interpolation(ax=ax7, s=2, vline_x=vline_x)

    plot_cross_section(ax=ax4, grid=sig0, vline_x=vline_x, s=0)
    plot_cross_section(ax=ax6, grid=sig1, vline_x=vline_x, s=1)
    plot_cross_section(ax=ax8, grid=sig2, vline_x=vline_x, s=2)

    #

    plt.subplots_adjust(hspace=0.8, wspace=0.2)
    plt.suptitle('2019-06-23 CUES Pointcloud: Interpolations with various blur values', size=16)
    plt.show()

    #plt.savefig(f'figs/interpolation_{i}.png')
    plt.close('all')

# +
mdic0 = {"array": sig0, "label": "20190623_sigma0"}
savemat('mat/20190623_sigma0.mat', mdic0)

mdic1 = {"array": sig1, "label": "20190623_sigma1"}
savemat('mat/20190623_sigma1.mat', mdic1)

mdic2 = {"array": sig2, "label": "20190623_sigma2"}
savemat('mat/20190623_sigma2.mat', mdic2)
# -


