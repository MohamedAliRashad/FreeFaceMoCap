---
layout: post
title: OneEuro Filter
subtitle: Always start simple
cover-img: /assets/img/path.jpg
thumbnail-img: /assets/img/mediapipe.png
share-img: /assets/img/mediapipe.png
tags: [filters]
---

## Introduction
In any industrial solution, **Stability** is the key for success and in our project we wanted to make the system as stable and robust as possible.

We chose to start simple in this part with the one-euro filter to see if it will suffice or not

To achieve this we used a low-pass filter (one-euro) to

## How it works

## Coding Tutorial

Here, we go through the code together for further understanding

In the [oneEuroFilter.py](https://github.com/MohamedAliRashad/FreeFaceMoCap/blob/main/Addon/FaceMeshTracking/oneEuroFilter.py) file, we can find two functions and a class:
1. 
```python
def smoothing_factor(t_e, cutoff):
    np = import_module('numpy')
    r = 2 * np.pi * cutoff * t_e
    return r / (r + 1)
```
In the `smoothing_factor` function, we evaluate the 

2. 
```python
def exponential_smoothing(a, x, x_prev):
    return a * x + (1 - a) * x_prev
```

3. 
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
we provide a frame counter represented in `self.frame_num` to keep track of time.

Then an if-else statement is made to lead the code between the initial state where we initialize the `OneEuroFilter` and the actual running of the algorithm.

After the transformation of points (done using the modifiers) we log the values of the three directions (x, y, z) into the filter for its processing to happen.


## Future works
1. 
2. 

## References
1. [Noise Filtering Using 1€ Filter](https://jaantollander.com/post/noise-filtering-using-one-euro-filter/)
2. [1€ Filter: A Simple Speed-based Low-pass Filter for
Noisy Input in Interactive Systems](https://dl.acm.org/doi/10.1145/2207676.2208639) - [Paper](https://hal.inria.fr/hal-00670496/document)