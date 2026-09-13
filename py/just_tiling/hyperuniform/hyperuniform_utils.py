"""
This file contains the functions and utilities used by making hyperuniform tile distribution.

> change_mask_nside
    input a mask with nside1, output mask with nside2
> move_on_sphere
    implement (dtheta, dphi) on (theta, phi)
    
"""


import numpy as np
import healpy as hp

def change_mask_nside(
    mask_in,
    nside_out,
    threshold=0.0,
    order_in="RING",
    order_out="RING",
):
    """
    change the resolution of HEALpix mask.
    if nside_out > nside_in (increasing the resolution), all pixels in masked region is set as mask (power=0 in hp.ud_grad)
    if nside_out < nside_in (decreasing the ersolution). a new pixel is set as mask according to the threshold

    parameters
    ----
    mask_in : bool array
        True = the areas in mask (not allowed, unobserved)
    nside_out : int
        target HEALPix nside。
    threshold : float
        the fraction threshold for treating new pixel as mask

        threshold=0.0:
            if new pixel contain any masked pixel, set as mask (conservative)

        threshold=0.5:
            if new pixel contain over half of masked pixel, set as mask

        threshold~1:
            set as mask only if almost all the pixels are masked
    """
    mask_in = np.asarray(mask_in, dtype=bool)

    nside_in = hp.get_nside(mask_in)

    if nside_in == nside_out:
        mask_out = mask_in.copy()
        return mask_out, ~mask_out

    masked_fraction = hp.ud_grade(
        mask_in.astype(np.float64),
        nside_out=nside_out,
        order_in=order_in,
        order_out=order_out,
        power=0,
    )

    if threshold <= 0:
        mask_out = masked_fraction > 0
    elif threshold >= 1:
        mask_out = masked_fraction >= 1.0 - 1e-12
    else:
        mask_out = masked_fraction >= threshold

    valid_out = ~mask_out

    return mask_out, valid_out



def move_on_sphere(theta, phi, grad_theta, grad_phi, step):
    """沿球面切向量移动，并通过指数映射保持在单位球面上。"""

    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    sin_phi = np.sin(phi)
    cos_phi = np.cos(phi)

    # 当前球面位置
    n = np.stack([
        sin_theta * cos_phi,
        sin_theta * sin_phi,
        cos_theta,
    ], axis=1)

    # theta 增大方向的单位切向量
    e_theta = np.stack([
        cos_theta * cos_phi,
        cos_theta * sin_phi,
        -sin_theta,
    ], axis=1)

    # phi 增大方向的单位切向量
    e_phi = np.stack([
        -sin_phi,
        cos_phi,
        np.zeros_like(phi),
    ], axis=1)

    # 三维切向位移
    tangent = step * (
        grad_theta[:, None] * e_theta
        + grad_phi[:, None] * e_phi
    )

    angle = np.linalg.norm(tangent, axis=1)

    tangent_unit = np.zeros_like(tangent)
    moving = angle > 0
    tangent_unit[moving] = (
        tangent[moving] / angle[moving, None]
    )

    # 球面指数映射
    n_new = (
        np.cos(angle)[:, None] * n
        + np.sin(angle)[:, None] * tangent_unit
    )

    theta_new, phi_new = hp.vec2ang(n_new)

    return theta_new, phi_new
