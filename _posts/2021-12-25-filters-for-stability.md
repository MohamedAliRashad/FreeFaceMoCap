---
layout: post
title: OneEuro Filter
subtitle: Wizards of Control
cover-img: /assets/img/filter.png
thumbnail-img: /assets/img/jitter.jpg
share-img: /assets/img/jitter.jpg
tags: [filters]
---

> All stable processes we shall predict. All unstable processes we shall control
>
> -- <cite>John von Neumann</cite>

## Introduction

In any industrial solution, **Stability** is one of the major keys for success. And we wanted our tool to be as stable and fast as possible.

Mediapipe as a tool for inferring facial keypoints is nice but it suffers from **jittering** (shakiness) and we wanted for content creators to not go through the headache of filtering the data themselves and do it for them.

Fortunately, there is a lot of filters to fix this problem and one of its simplest approaches 

One of these filters is the **one-euro filter** and it's one of the simplest approaches for such problem.

## How it works

The 1€ Filter is a low pass filter for real-time noisy stream of frames. its an exponential smoothing function that uses the hyperparameter alpha to smooth the transition between frames and make it more stable.

<center>
<img src="https://latex.codecogs.com/svg.latex?%5CLARGE%20Y_i%20%3D%20%5Calpha%20X_i%20&plus;%20%281%20-%20%5Calpha%29X_%7Bi-1%7D">
</center>

**Note**: The equation starts from second frame (i > 2)

The **smoothing factor** (alpha) is calculated using this simple equation, where *fc* is the cut off frequency of the filter

<center>
<img src="https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Calpha%20%3D%20%5Cfrac%7B2%20%5Cpi%20f_c%7D%7B2%20%5Cpi%20f_c%20&plus;%201%7D 
">
</center>

## Coding Tutorial

In the [oneEuroFilter.py](https://github.com/MohamedAliRashad/FreeFaceMoCap/blob/main/Addon/FaceMeshTracking/oneEuroFilter.py) file, we can find two functions and a class:

**First function** is for calculating the alpha (the `smoothing_factor`)
```python
def smoothing_factor(t_e, cutoff):
    np = import_module('numpy')
    r = 2 * np.pi * cutoff * t_e
    return r / (r + 1)
```

**Second function** is for calculating the output of filter
```python
def exponential_smoothing(a, x, x_prev):
    return a * x + (1 - a) * x_prev
```

**The 1€ Filter class** takes different hyper parameters  
```python
class OneEuroFilter:
    def __init__(self, t0, x0, dx0=0.0, min_cutoff=0.00001, beta=20,
                 d_cutoff=1.0):
        """Initialize the one euro filter."""
        np = import_module('numpy')

        self.min_cutoff = np.ones_like(x0) * min_cutoff
        self.beta = np.ones_like(x0) * beta
        self.d_cutoff = np.ones_like(x0) * d_cutoff
        # Previous values.
        self.x_prev = np.array(x0)
        self.dx_prev = np.ones_like(x0) * dx0
        self.t_prev = t0

    def __call__(self, t, x):
        """Compute the filtered signal."""
        np = import_module('numpy')
        t_e = t - self.t_prev

        # The filtered derivative of the signal.
        a_d = smoothing_factor(t_e, self.d_cutoff)
        dx = (x - self.x_prev) / t_e
        dx_hat = exponential_smoothing(a_d, dx, self.dx_prev)

        # The filtered signal.
        cutoff = self.min_cutoff + self.beta * np.abs(dx_hat)
        a = smoothing_factor(t_e, cutoff)
        x_hat = exponential_smoothing(a, x, self.x_prev)

        # Memorize the previous values.
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t

        return x_hat
```

In the [captureFace.py](https://github.com/MohamedAliRashad/FreeFaceMoCap/blob/main/Addon/Operators/captureFace.py) we use the `OneEuroFilter` as follows

```python
if self.frame_num > 0:
    landmarks = transform_landmarks(
        self.results, None,  initial=False)

    x = self.one_euro_x(
        self.frame_num, landmarks[:, 0]).reshape((65, 1))
    y = self.one_euro_y(
        self.frame_num, landmarks[:, 1]).reshape((65, 1))
    z = self.one_euro_z(
        self.frame_num, landmarks[:, 2]).reshape((65, 1))

    armature = self.np.append(
        x, self.np.append(y, z, axis=1), axis=1)
    # transformation
    add_landmark_empties(armature, None)
    rotate_head_with_axes()

else:
    armature = Config.armature_points
    self.one_euro_x = OneEuroFilter(self.frame_num, armature[:, 0])
    self.one_euro_y = OneEuroFilter(self.frame_num, armature[:, 1])
    self.one_euro_z = OneEuroFilter(self.frame_num, armature[:, 2])

self.frame_num += 1
```

## Future works
1. Try [Kalman filter](https://www.intechopen.com/chapters/63164) and its variants
1. Try [Particle Filters](https://towardsdatascience.com/particle-filter-a-hero-in-the-world-of-non-linearity-and-non-gaussian-6d8947f4a3dc)

## References
1. [Noise Filtering Using 1€ Filter](https://jaantollander.com/post/noise-filtering-using-one-euro-filter/)
2. [1€ Filter: A Simple Speed-based Low-pass Filter for
Noisy Input in Interactive Systems](https://hal.inria.fr/hal-00670496/document)