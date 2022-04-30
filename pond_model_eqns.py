# Non-linear dynamic model of a storage pond
# Bill Tubbs, April 2022.
# For details and background, see:
#  - Non-linear-dynamic-model-storage-pond.ipynb
#

import numpy as np


# State-space model equations
def f(t, x, u, params):
    """Continuous-time dynamics
    """
    d, c, b = params['weir_height'], params['c'], params['weir_width']
    assert np.all(x < 0.33 * b), "Out of bounds"
    return c * (u - 3.33 * (b - 0.2 * x) * x ** 1.5 ) / (x + d) ** 2


def g(t, x, u, params):
    """Measurement function
    """
    return x


# Default system parameters
alpha = 10  # inclination of pond walls from vertical (deg)
params = {
    'weir_height': 5,  # height of weir from deepest point (m)
    'c': np.tan(np.deg2rad(alpha)) ** 2 / np.pi,
    'weir_width': 2  # width of the weir (m)
}


# Define normal operating point
u_nop, x_nop = 1, 0.28805


def run_tests():
    # Check function calculations
    assert(f(0, 0, 0, params) == 0)
    assert(f(110, 0, 0, params) == 0)
    try:
        f(0, 0.34 * params['weir_width'], 0, params)
    except AssertionError:
        pass
    else:
        raise AssertionError("Bounds error was not raised")

    t = 10
    assert(f(t, x_nop, u_nop, params) < 1e-6)
    y_nop = g(t, x_nop, u_nop, params)
    assert(y_nop == x_nop)

    # Check params have an effect
    params2 = params.copy()
    params2['c'] = params['c'] + 0.001
    assert(f(t, x_nop, u_nop, params) != f(t, x_nop, u_nop, params2))
    params2 = params.copy()
    params2['weir_height'] = params['weir_height'] + 0.01
    assert(f(t, x_nop, u_nop, params) != f(t, x_nop, u_nop, params2))
    params2 = params.copy()
    params2['weir_width'] = params['weir_height'] + 0.1
    assert(f(t, x_nop, u_nop, params) != f(t, x_nop, u_nop, params2))


run_tests()