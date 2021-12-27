---
layout: post
title: MediaPipe for Face Tracking
subtitle: Start simple and small 
cover-img: /assets/img/path.jpg
thumbnail-img: /assets/img/mediapipe.png
share-img: /assets/img/mediapipe.png
tags: [story, tracking]
---

# Introduction to MediaPipe
Mediapipe was a solution made by Google to push the usage of Deep Learning in mainstream applications.

It offers a lot of high-performance tools based on intuitive vision problems like **Face Mesh Tracking** that we are using here.

# Why MediaPipe?

MediaPipe provides lightweight models that use CPU and GPU to achieve well-performance and effective usage of resources, which is very suitable for our Addon.

Besides that, MediaPipe’s API  is very simple and easy to use, which makes it a good choice to begin with.

# MediaPipe Face Mesh

MediaPipe Face Mesh is a computer vision technology that enables us to estimate and track landmarks on the face in real-time. Using these landmarks we can  model face reactions and expression changes in 3D space.

MediaPipe Face Mesh consist of two neural network models. The first is Face detection model (BlazeFace) which computes the face location so we can crop the face, the second is 3D face landmark model which operate on the cropped image to estimate 3D face landmarks.

For more details about MediaPipe Face Mesh checkout this post [MediaPipe Face Mesh](https://google.github.io/mediapipe/solutions/face_mesh.html)

# How we used MediaPipe?

We used MediaPipe Face Mesh model to extract 468 landmarks from the user’s face image (captured by the webcam) in real-time. Then the position of each point of the landmarks in 3D space is used to influence the movement of the Face [Armature](https://docs.blender.org/manual/en/latest/animation/armatures/introduction.html)

More about the mapping is discussed in this post: [landmark mapping](https://mohamedalirashad.github.io/FreeFaceMoCap/2021-12-26-landmarks-mapping/)

# References

[https://google.github.io/mediapipe/solutions/face_detection.html](https://google.github.io/mediapipe/solutions/face_detection.html)
