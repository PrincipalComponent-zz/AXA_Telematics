
# USEFUL METHOD USED FOR DEALING WITH SIGNAL FUNCTIONS AND TRAJECTORIES
import numpy as np
from scipy import stats
import math


def sg_filter(x, m, k=0):
    """
    x = Vector of sample times
    m = Order of the smoothing polynomial
    k = Which derivative
    """
    mid = len(x) / 2        
    a = x - x[mid]
    expa = lambda x: map(lambda i: i**x, a)    
    A = np.r_[map(expa, range(0,m+1))].transpose()
    Ai = np.linalg.pinv(A)

    return Ai[k]

def smooth(x, y, size=5, order=2, deriv=0):
    if deriv > order:
        raise Exception, "deriv must be <= order"

    n = len(x)
    m = size

    result = np.zeros(n)

    for i in xrange(m, n-m):
        start, end = i - m, i + m + 1
        f = sg_filter(x[start:end], order, deriv)
        result[i] = np.dot(f, y[start:end])

    if deriv > 1:
        result *= math.factorial(deriv)

    return result


def removeRotation(XY, removeBias = False):
    """ change of basis matrix so that the horizontal (x) axis is the vector between the first
        and last point

        Param: XY must be an N x 2 numpy array
        Return: Nx2 array of vectors in new basis

        Assumes all XY vectors start at origin (obvious from fn name)
    """
    if removeBias: XY = XY - XY[0,:]
    # calc the unit vectors of the new basis
    xdash = XY[-1]

    ydash = np.array( [-xdash[1], xdash[0] ])

    normXdash = np.linalg.norm(xdash)
    normYdash = np.linalg.norm(ydash)

    # adapt for round trip!!! 
    if normXdash > 0:
        u = xdash /normXdash
    else:
        u = np.array([1,0])
    if normYdash > 0:
        v = ydash / normYdash
    else:
        v = np.array([0,1])

    # change of basis 'matrix' - (x',y') = M(inv)(x,y)
    # Minv is just transpose of the new basis matrix M since rotn about origin
    Mdash = np.array([[u[0],u[1]],[v[0],v[1]]])

    # now transform aall the points t the new basis
    # Mdash * XY -> 2x2 x (2xN) hence transpose 
    XYnew = np.dot(Mdash, XY.T)

    # return it back as Nx2
    return XYnew.T


def group_by_func(categories, col_cat, col_toagg, functions, mincount = 15):
    """
        COL_CAT: column with categories in numerical
        COL_TOAGG: column to aggregate and apply functions to
        functions: array of string defining the functions to apply
    """
    num_colagg = col_toagg.shape[1] 
    res = np.zeros((len(categories), num_colagg * len(functions) + 1))
    res[:] = np.nan
    res[:,0] = categories

    for ival, val in enumerate(categories):
        idxes = col_cat == val
        counter = 1        
        # if val == 5:
        #     import pdb
        #     pdb.set_trace()
        for ca in range(num_colagg):
            ccc = col_toagg[idxes, ca]
            count = ccc.shape[0]
            if 'count' in functions:
                rr = ccc.shape[0]
                res[ival, counter] = rr
                counter += 1
            if 'count_pct' in functions:
                rr = ccc.shape[0]/float(col_toagg.shape[0])
                res[ival, counter] = rr
                counter += 1
            if count>mincount:
                if 'mean' in functions:
                    rr = np.nanmean(ccc)
                    res[ival, counter] = rr
                    counter += 1
                if 'median' in functions:
                    rr = np.nanmedian(ccc)
                    res[ival, counter] = rr
                    counter += 1
                if 'std' in functions:
                    rr = np.nanstd(ccc)
                    res[ival, counter] = rr
                    counter += 1
                if 'max' in functions:
                    rr = np.nanmax(ccc)
                    res[ival, counter] = rr
                    counter += 1
                if 'min' in functions:
                    rr = np.nanmin(ccc)
                    res[ival, counter] = rr
                    counter += 1
                aa = [s for s in functions if 'percentile' in s]
                if len(aa) > 0:
                    for percstr in aa:
                        perc = int(percstr.split('_')[1])
                        rr = np.nanpercentile(ccc, perc)
                        res[ival, counter] = rr
                        counter += 1

    return res

