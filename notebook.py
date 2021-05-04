# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

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

# +
files = os.listdir('data')

sp = Sunposition(
        local_timezone=c.TIMEZONE,
        date_str=files[0][:8],
        lat_lon=c.LAT_LON,
)
# -

sp.sunposition_df.head()

# +
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

# 2--------------------------------------------------------------------------------
# NN imshow (no blur)
ax3 = fig.add_subplot(gs[1, :1])
res = int(np.ceil(np.sqrt(pointcloud.xyz.shape[0])))
grid = pointcloud.interpolate_grid(xyz=pointcloud.xyz, res=res, method='nearest')
ax3.imshow(grid, origin='lower')
ax3 = _format(fig=fig, ax=ax3, title="NN Interpolation ($\sigma$=0)")

# NN imshow (no blur) - cross-section
ax4 = fig.add_subplot(gs[1, 1:])


# 3--------------------------------------------------------------------------------
# NN cross-section (sigma = 1 blur)
ax5 = fig.add_subplot(gs[2, :1])
sig1 = ndimage.gaussian_filter(grid, sigma=1)
ax5.imshow(sig1, origin='lower')
ax5 = _format(fig=fig, ax=ax5, title="NN Interpolation ($\sigma$=1)")


# NN imshow (sigma = 2 blur)
ax6 = fig.add_subplot(gs[2, 1:])

# 4--------------------------------------------------------------------------------

ax7 = fig.add_subplot(gs[3, :1])
sig2 = ndimage.gaussian_filter(grid, sigma=2)
ax7.imshow(sig2, origin='lower')
ax7 = _format(fig=fig, ax=ax7, title="NN Interpolation ($\sigma$=2)", last_frame=True)

ax8 = fig.add_subplot(gs[3, 1:])

plt.subplots_adjust(hspace=0.6)

plt.show()
# -

#

mdic = {"array": grid, "label": "20190623_NN"}
savemat('mat/20190623_NN.mat', mdic)


