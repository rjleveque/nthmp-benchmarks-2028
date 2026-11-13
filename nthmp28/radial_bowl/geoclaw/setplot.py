
"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

"""

from numpy import *
import os
from clawpack.visclaw.legend_tools import add_legend

try:
    from nthmp28.radial_bowl import true_solution as TS
except:
    print('*** The git repository directory needs to be on your Python path')
    raise


if 0:
    q1d_dir = os.path.abspath('./1d_radial/_output')
    if not os.path.exists(q1d_dir):
        print(f"Directory {q1d_dir} not found")
        q1d_dir = None 
else:
    q1d_dir = None

#--------------------------
def setplot(plotdata=None):
#--------------------------

    """
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.

    """


    from clawpack.visclaw import colormaps, geoplot

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()


    plotdata.clearfigures()  # clear any old figures,axes,items data

    def set_drytol(current_data):
        # The drytol parameter is used in masking land and water and
        # affects what color map is used for cells with small water depth h.
        # The cell will be plotted as dry if h < drytol.
        # The best value to use often depends on the application and can
        # be set here (measured in meters):
        current_data.user["drytol"] = 1.e-3

    plotdata.beforeframe = set_drytol


    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugenos = 'all'
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos=gaugenos, format_string='ko', add_labels=True)


    land_cmap = colormaps.make_colormap({ 0.0:[0.1,0.4,0.0],
                                         0.25:[0.0,1.0,0.0],
                                          0.5:[0.8,1.0,0.5],
                                          1.0:[0.8,0.5,0.2]})

    #-----------------------------------------
    # Figure for pcolor plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='pcolor', figno=0)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Water surface / depth'
    plotaxes.scaled = True

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = -1
    plotitem.pcolor_cmax = 1
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = -3.0
    plotitem.pcolor_cmax = 3.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    def plot_shore(current_data):
        from pylab import linspace, cos, sin, plot, legend
        t = current_data.t

        rshore = TS.shoreline(t)
        print(f'rshore = {rshore:.3f}')

        theta = linspace(0, 2*pi, 1000)
        xshore = rshore * cos(theta)
        yshore = rshore * sin(theta)
        plot(xshore, yshore, 'yellow', linewidth=1.6, label='true shoreline')
        legend(loc='upper left', fontsize=9, labelcolor='yellow',
                facecolor='g')

    plotaxes.afteraxes = plot_shore

    # Add contour lines of bathymetry:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = linspace(-.1, 0.5, 20)
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid'}
    plotitem.amr_contour_show = [1]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

    #-----------------------------------------
    # Figure for transect plots
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='transect', figno=9)
    plotfigure.figsize = (12,5)
    plotaxes = plotfigure.new_plotaxes('pcolor')

    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,sqrt,grid,xlim,ylim, \
                    xticks,ylabel,where,nan
        from numpy import cos,pi,linspace,zeros,ones,hstack,sin
        from clawpack.pyclaw import Solution
        from clawpack.visclaw import gridtools
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        method = 'linear'
        rout = linspace(0, 2*TS.L, 1000)

        legend_info = []

        t = current_data.t

        h_true, u_true, v_true, eta_true = TS.qtrue(rout, zeros(rout.shape), t)
        plot(rout, eta_true, 'k--')
        plot(-rout, eta_true, 'k--')
        legend_info.append(('analytic solution', 'k', '--'))

        B_true = TS.Bfcn(rout, zeros(rout.shape))
        plot(rout, B_true,'g')
        plot(-rout, B_true,'g')
        legend_info.append(('topography', 'g', '-'))

        c = ['b','c','m']
        for k,alpha in enumerate([0,20,45]):
            xout = rout * cos(alpha*pi/180)
            yout = rout * sin(alpha*pi/180)
            h_out = gridtools.grid_output_2d(framesoln, 0, xout, yout,
                                             method=method)
            eta_out = gridtools.grid_output_2d(framesoln, -1, xout, yout,
                                               method=method)
            B_out = eta_out - h_out
            eta_out = where(h_out > 1e-3, eta_out, nan)
            plot(rout, eta_out, color=c[k])
            plot(-rout, eta_out, color=c[k])
            legend_info.append((f'for alpha={alpha:.1f} degrees', c[k], '-'))

        xlabel('x (meters)')
        ylabel('elevation (meters)')
        xlim(-240,240)
        ylim(-2.5,2.5)
        grid(True)

        if q1d_dir is not None:
            legend_info.append(('1D radial', 'r', '--'))

        add_legend(labels=[li[0] for li in legend_info],
                   colors=[li[1] for li in legend_info],
                   linestyles=[li[2] for li in legend_info],
                   loc='upper left', framealpha=1, fontsize=9)



    if q1d_dir is not None:
        # 1d radial solution:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.outdir = q1d_dir
        plotitem.plot_var = -1
        plotitem.plotstyle = '--'
        plotitem.kwargs = {'linewidth':2}
        plotitem.color = 'r'

        # 1d radial solution reflected:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.outdir = q1d_dir
        plotitem.plot_var = -1
        plotitem.plotstyle = '--'
        plotitem.color = 'r'
        plotitem.kwargs = {'linewidth':2}
        plotitem.MappedGrid = True
        plotitem.mapc2p = lambda x: -x


    plotaxes.afteraxes = plot_xsec
    plotaxes.title = 'radial transects at angles alpha to x-axis,'


    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')

    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = [-0.05, 0.05]
    plotaxes.title = 'Surface'
    plotaxes.grid = True

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = -1
    plotitem.plotstyle = 'b-'


    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = []             # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # make multiple frame png's at once
    plotdata.mp4_movie = True

    return plotdata
