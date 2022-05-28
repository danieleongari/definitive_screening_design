"""DSD with two-levels categoricals.

Ported from JMP script to Matlab 04-Mar-2015
Jacob Albrecht, BMS

Ported to Python on Saturday 28-May-2022, 
when oudoor it was warm and sunny but my passion for open-source code kept me at home
Daniele Ongari

Copyright (c) 2015, Jacob Albrecht
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution
* Neither the name of Bristol-Myers Squibb nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
"""

import numpy as np
from sympy import isprime, legendre


def get_legendre(i, j, fld):
    """Generate legendre symbol given i,j and fld."""
    m = j - i
    modq = np.remainder(fld**2, fld.size)
    if m == 0:
        legendre = 0
    else:
        if np.any(modq == m):
            legendre = -1
        else:
            legendre = 1

    return legendre


def get_paley_matrix(q):
    """Construct paley matrix given prime number."""
    m = np.zeros((q, q))
    fld = np.arange(0, (q - 1) + 1)
    for jj in range(q):
        for j in range(jj, q):
            m[jj, j] = get_legendre(jj - 1, j - 1, fld)

    mt = np.transpose(m)
    if np.mod(q, 4) == np.remainder(3, 4):
        factor = -1
    else:
        factor = 1

    m = m + (np.multiply(mt, factor))
    paley_matrix = m

    return paley_matrix


def compute_dsd(nctn, ncat=0, designChoice="dsd", verbose=False):
    """DSD calculates definitive screening design conditions given an number 
    of continuous (nf) and categorical (ncat) factors, based on:

    Jones, B and Nachtsheim, C. (2011)
        "A Class of Three-Level Designs for Definitive Screening in the Presence of Second-Order Effects"
        Journal of Quality Technology, 43, 1-15

    Jones, B and Nachtsheim, C. (2013)
        "Definitive Screening Designs with Added Two-Level Categorical Factors"
        Journal of Quality Technology, 45, 121-129
    Usage:  f=dsd(nf,ncat,designChoice)

    Inputs: nctn: Number of continuous factors
            ncat: number of categorical factors
            designChoice:
                    1 or 'dsd': De-alias all two-factor interactions with
                        categorical factors. (Default)
                    2 or 'orth': Make orthogonal main-effects plan.

    Outputs: f: design matrix (-1,0,or 1) with a column for each of the
                three level continuous variables, 1 or 2 for two level
                categorical variables.

    Validated against the equivalent JMP10 addin for all 1736 permutations
    of (nf=3:30, ncat=0:30,designChoice=1:2)

    See also ROWEXCH, DAUGMENT, DCOVARY, X2FX, CORDEXCH
    """
    if designChoice not in ["dsd", "orth"]:
        raise Exception("Design Choice must be 'dsd' or 'orth'")

    f10 = np.array([
        [ 0,  1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  0, -1, -1, -1, -1,  1,  1,  1,  1], 
        [ 1, -1,  0, -1,  1,  1, -1, -1,  1,  1],
        [ 1, -1, -1,  0,  1,  1,  1,  1, -1, -1],
        [ 1, -1,  1,  1,  0, -1, -1,  1, -1,  1],
        [ 1, -1,  1,  1, -1,  0,  1, -1,  1, -1],
        [ 1,  1, -1,  1, -1,  1,  0, -1, -1,  1],
        [ 1,  1, -1,  1,  1, -1, -1,  0,  1, -1],
        [ 1,  1,  1, -1, -1,  1, -1,  1,  0, -1],
        [ 1,  1,  1, -1,  1, -1,  1, -1, -1,  0],
        [ 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1,  0,  1,  1,  1,  1, -1, -1, -1, -1],
        [-1,  1,  0,  1, -1, -1,  1,  1, -1, -1],
        [-1,  1,  1,  0, -1, -1, -1, -1,  1,  1],
        [-1,  1, -1, -1,  0,  1,  1, -1,  1, -1],
        [-1,  1, -1, -1,  1,  0, -1,  1, -1,  1],
        [ 1, -1,  1, -1,  1, -1,  0,  1,  1, -1],
        [-1, -1,  1, -1, -1,  1,  1,  0, -1,  1],
        [-1, -1, -1,  1,  1, -1,  1, -1,  0,  1],
        [-1, -1, -1,  1, -1,  1, -1,  1,  1,  0]
    ])
    f16_half = np.array([
        [-0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
        [-1,  0,  1,  1, -1,  1, -1, -1,  1, -1,  1,  1, -1,  1, -1, -1],
        [-1, -1,  0,  1,  1, -1,  1, -1,  1, -1, -1,  1,  1, -1,  1, -1],
        [-1, -1, -1,  0,  1,  1, -1,  1,  1, -1, -1, -1,  1,  1, -1,  1],
        [-1,  1, -1, -1,  0,  1,  1, -1,  1,  1, -1, -1, -1,  1,  1, -1],
        [-1, -1,  1, -1, -1,  0,  1,  1,  1, -1,  1, -1, -1, -1,  1,  1], 
        [-1,  1, -1,  1, -1, -1,  0,  1,  1,  1, -1,  1, -1, -1, -1,  1], 
        [-1,  1,  1, -1,  1, -1, -1,  0,  1,  1,  1, -1,  1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1,  0,  1,  1,  1,  1,  1,  1,  1],
        [-1,  1,  1,  1, -1,  1, -1, -1, -1,  0, -1, -1,  1, -1,  1,  1],
        [-1, -1,  1,  1,  1, -1,  1, -1, -1,  1,  0, -1, -1,  1, -1,  1],
        [-1, -1, -1,  1,  1,  1, -1,  1, -1,  1,  1,  0, -1, -1,  1, -1],
        [-1,  1, -1, -1,  1,  1,  1, -1, -1, -1,  1,  1,  0, -1, -1,  1],
        [-1, -1,  1, -1, -1,  1,  1,  1, -1,  1, -1,  1,  1,  0, -1, -1],
        [-1,  1, -1,  1, -1, -1,  1,  1, -1, -1,  1, -1,  1,  1,  0, -1],
        [-1,  1,  1, -1,  1, -1, -1,  1, -1, -1, -1,  1, -1,  1,  1,  0]
    ])
    f16 = np.vstack((f16_half, -1*f16_half))
    nf = nctn + ncat  # number of total factors

    if 2 * int(np.floor(nf / 2)) == nf:  # nf is even
        p = nf - 1
    else:  # nf is odd
        p = nf

    done = False
    while not done:
        if isprime(p):
            c = np.hstack((
                    np.vstack((np.zeros(1), np.ones((p, 1)))), 
                    np.vstack((np.ones((1, p)), get_paley_matrix(p)))
                    ))
            f = np.vstack((c, -c))
            done = True
        else:
            p = p + 2

    if verbose:
        print("Initial f")
        print(f)

    # Overvrite f for certain nf
    if nf == 9:
        f = f10[:,:9]
    elif nf == 10:
        f = f10
    elif nf == 16:
        f = f16
    elif nf == 15:
        f = f16[:,:15]
    elif nf == 26 or nf == 25:
        a = get_paley_matrix(13)
        ## starter vector for B
        strt = np.array([-1, -1,  1, -1,  1,  1,  1,  1,  1, -1,  1,  1, 1])
        b = np.array([])
        ## construct B
        for ii in range(13):
            if verbose:
                print(b)
            if b.size==0:
                b = np.transpose(strt)
            else:
                b = np.transpose(np.vstack((np.transpose(b), strt)))

            strt = np.roll(strt, (0, -1))  # circshift
        c = np.vstack((
                np.hstack((a, b)), 
                np.hstack((np.transpose(b),-1 * a))
        ))

        if nf == 26:
            f = np.vstack((c, -c))
        else:
            f = np.vstack((c, -c))

    nr, nc = f.shape  # Number of rows and columns before adding categoricals
    if nc > nf: # Reduce the number of columns
        f = f[:, :nf]

    # Add center at the end
    if ncat == 0:
        zero_nrows = 1
    elif ncat == 1:
        zero_nrows = 2
    elif ncat > 1:
        if designChoice == "dsd":
            zero_nrows = 2
        elif designChoice == "orth":
            zero_nrows = 4
    f = np.vstack((f, np.zeros((zero_nrows, nf))))

    if verbose:
        print("Before tmpf")
        print(f)

    tmpf = f.copy()
    for rowidx in range(int(nr/2)):
        tmpf[2 * rowidx, :] = f[rowidx, :]
        tmpf[2 * rowidx+1, :] = f[rowidx + int(nr/2), :]
    f = tmpf.copy()

    if verbose:
        print("Before designChoice")
        print(f)

    if designChoice == "dsd":
        B = np.array([
            [-1, -1, -1],
            [+1, +1, +1]
        ])
        for fidx in range(nctn, nf):
            if ncat > 1:
                colidx = np.remainder(fidx - nctn - 1, 3)
                f[nr:(nr+3), fidx] = B[:, colidx]
    elif designChoice == "orth":
        B = np.array([
            [-1, -1, -1, +1],
            [-1, -1, +1, -1],
            [-1, +1, -1, -1],
            [ 1, -1, -1, -1]
        ])
        for fidx in range(nctn, nf):
            if ncat > 1:
                colidx = np.remainder(fidx - nctn - 1, 4)
                f[nr:(nr+2), fidx] = B[:, colidx]


    if verbose:
        print("Before ncat>0")
        print(f)

    nr = f.shape[0] # Update nr

    # Add columns for categoricals
    if ncat > 0:
        minList2 = np.ones((ncat, 1))
        maxList2 = 2 * np.ones((ncat, 1))

        for fidx in range(nctn, nf):
            for rowidx in range(nr):
                if f[rowidx, fidx] == 1:
                    f[rowidx, fidx] = maxList2[fidx - nctn]
                if f[rowidx, fidx] == -1:
                    f[rowidx, fidx] = minList2[fidx - nctn]
                if f[rowidx, fidx] == 0:
                    if designChoice == "orth":
                        f[rowidx, fidx] = maxList2[fidx - nctn]
                    else:
                        # even rows are mins, odd rows are maxes
                        if (np.remainder(rowidx, 2) == 0):
                            f[rowidx, fidx] = minList2[fidx - nctn]
                        else:
                            f[rowidx, fidx] = maxList2[fidx - nctn]

    return f