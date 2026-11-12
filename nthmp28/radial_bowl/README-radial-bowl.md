(README-radial-bowl)=
# Radially-Symmetric Bowl Problems

The first problem considered has an exact solution developed by
https://doi.org/10.1017/S0022112081001882.

## Parabolic Bowl

The topography is defined by the parabola
$$
B(x,y) = -D_0 (1 - (x^2 + y^2))/L^2,
$$
where $D_0$ is the depth at $x=y=0$ and $L$ is the distance to the initial
shoreline (if the bowl is filled with water to $B \equiv 0$).

This is radially symmetric, $B(x,y) = \hat B(r) = -D_0(1-(r/L)^2)$,
where $r = \sqrt{x^2 + y^2}$.

## Radially Symmetric Solution

There is an exact solution that is radially symmetric with specified
initial elevation at the origin $\eta_0 = \hat\eta(0,t)$, given by the
following formulas (this works for any specified $\eta_0 < D_0$):
\begin{align}
\hat\eta(r,t) &= D_0 (\sqrt{(1-A^2)}/(1-A\cos(\omega t)) - 1 \\
    &\qquad - (r/L)^2  ((1-A^2)/(1-A\cos(\omega t))^2 - 1)), \\
\hat u(r,t) &= (0.5\omega r A \sin(\omega t)) / (1-A\cos(\omega t)).
\end{align}
where
\begin{align}
\omega &= \sqrt{8gD_0} / L^2, \quad (\text{with} ~g = 9.81)\\
A &= ((D_0 + \eta_0)^2 - D_0^2) / ((D_0 + \eta_0)^2 + D_0^2)
\end{align}
The water oscillates with period
$$
T = 2\pi/\omega.
$$
Note that $\hat u(r,t)$ is the radial velocity and in 2 dimensions the $x$
and $y$ velocities are given by the same formula with $r$ replaced by
$x$ or $y$ respectively.

### Choice of parameters

For the tests done so far with GeoClaw, the values $D_0 = 10$, $L = 200$,
and $\eta_0 = 2$ were used. This gives a wave with amplitude 2 meters
moving up and down on a beach with slope $\hat B'(r) = 2D_0 r/L^2 = 0.1$
at the initial shoreline $r=L=200$ meters from the origin.

### Sample results

These results show GeoClaw simulations out to $t = 10T = 488$ seconds
(10 periods).

These results were computed on the full domain $[-240, 240] \times
[-240, 240]$ with a uniform grid (AMR is not being used).  The same
results can be computed in 1/4 the time by restricting the domain to
a quadrant $[0, 240] \times [0, 240]$ and imposing solid wall boundary
conditions at $x=0$ and at $y=0$.

#### On 480 x 480 grid

The agreement is very good at early times, but by the end of 10 periods there
is visible disagreement:

:::{figure} ./geoclaw/_plots_480/frame0120fig9.png
:width: 600px
:align: center
:::

But note that the numerical solution stays radially symmetric (the transects
shown at 0, 20, and 45 degrees from the x-axis lie on top of one another).

:::{dropdown} Animation of 2D solution in parabolic bowl
:close:
```{figure} ./geoclaw/_plots_480/movie_fig0.mp4
:width: 600px
:align: center
```
:::

:::{dropdown} Animation of 1D transects of the 2D solution
:close:
```{figure} ./geoclaw/_plots_480/movie_fig9.mp4
:width: 600px
:align: center
```
:::

#### On 1440 x 1440 grid

Refining by a factor of 3 in each direction gives better agreement at
later times.  After 10 periods...


:::{figure} ./geoclaw/_plots_1440/frame0120fig9.png
:width: 600px
:align: center
:::

:::{dropdown} Animation of 2D solution in parabolic bowl
:close:
```{figure} ./geoclaw/_plots_1440/movie_fig0.mp4
:width: 600px
:align: center
```
:::

:::{dropdown} Animation of 1D transects of the 2D solution
:close:
```{figure} ./geoclaw/_plots_1440/movie_fig9.mp4
:width: 600px
:align: center
```
:::

## Variants

The tests shown above have also been solved using the 1D GeoClaw code with
source terms added for radial symmetry.  The results on a 1D grid with 240
points from $r=0$ to $r=240$ agree very well with the 2D transect results on
the 480 x 480 grid shown above, and similarly when each is refined by a factor
of 3.

This suggests that a fine grid 1D solution can be used as a reference solution'
for the 2D problem, also for different choices of (radially symmetric)
initial conditions for which the exact solution is not known, or for other
variants such as the addition of more realistic bottom friction, or dispersive
terms.

A few such experiments have been performed.

### Adding Friction

The exact solution of Thacker is in the absence of friction. If the usual
bottom friction is added with the standard Manning coefficient 0.025, then
two effects are visible in the simulations:

- At early times the main difference is seen as the water recedes at the shore,
with a thin layer of water stretching out behind and a much smoother
profile near the shore (with no friction the water surface hits the beach at
a non-zero angle).

- At later times, the oscillating wave decays in amplitude.

#### An initial experiment:

In these plots:
- The black dashed line is again
the exact solution to the original frictionless problem.
- The red dashed line is the radially symmetric solution computed with
GeoClaw using 240 points, with friction added.
- The solid lines are transects of the 2D solution (with friction) on
a 480 x 480 grid, at 3 different angles to the x-axis.

Here is a zoom of the shoreline after 1 period:

:::{figure} ./friction/geoclaw/_plots_480/zoom1T.png
:width: 600px
:align: center
:::

And here is a plot of the final surface after 10 periods.

:::{figure} ./friction/geoclaw/_plots_480/frame0120fig9.png
:width: 600px
:align: center
:::

:::{dropdown} Animation of 1D transects of the 2D solution
:close:
```{figure} ./friction/geoclaw/_plots_480/movie_fig9.mp4
:width: 600px
:align: center
```
:::

### Initial conditions giving a breaking wave

### Dispersive Version

## Sloshing Problem
