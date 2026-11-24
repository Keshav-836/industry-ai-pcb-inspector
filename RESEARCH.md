# Research

## The problem

One photo of a good board with named boxes, then new photos of the same board
from the same camera. Say which named parts are gone, offline, on a board I've
never seen (the reviewers name parts live at the demo).

So whatever I build has to work from **one reference photo with no training**.

## What I looked at

- **PCB-MC** (2026): the closest paper to this task. Notes that most PCB
  datasets don't label missing parts at their expected spot.
  https://arxiv.org/abs/2609.39427
- **DeepPCB**: template vs test image pairs, same idea as mine, but for copper
  defects on bare boards, not missing parts.
  https://github.com/tangsanli5201/DeepPCB
- **Khare & Bahel**: finds missing components by subtracting the test board from
  a correct one. Close to my approach.
  https://arxiv.org/abs/2102.10777
- **SSIM** (Wang et al., 2004): compares structure instead of raw pixels, so
  lighting matters less. https://ieeexplore.ieee.org/document/1284395
- **ORB + homography** (OpenCV): for lining up two photos.
  https://docs.opencv.org/4.x/d1/de0/tutorial_py_feature_homography.html
- **YOLO** and **PatchCore**: looked at as alternatives (see below).
  https://github.com/ultralytics/ultralytics / https://arxiv.org/abs/2106.08265

## Options I compared

| Option | Decision |
|---|---|
| Gemini / GPT-4V | No. Online APIs aren't allowed. |
| Train YOLO | No. Needs lots of labelled data and won't know the reviewers' parts. |
| Anomaly detection (PatchCore) | No. Needs many good images, I get one. Doesn't name the part. |
| Plain pixel subtraction | No. Breaks with a small camera shift or light change. |
| **Align, then compare each named box** | **Yes.** One photo, any board, no training, offline. |

## What I built

1. Line up the test photo with the reference (ORB + homography + RANSAC).
2. In each named box, measure the shape change (SSIM, brightness-normalised)
   and the colour change (LAB colour channels only).
3. Score = half of each. Above **0.35** = missing.

I picked 0.35 from real scores: missing parts were 0.58 and up, present parts
0.18 and below.

## Results

- Board 1: **8 / 8** correct (one photo shifted by 7 px)
- Board 2, a dense board: **3 / 3** correct with the same settings, including a tiny capacitor
- Brighter, darker, warmer and slightly rotated versions: no false alarms

## Limits

- A very different camera angle can break alignment; the app warns when that happens.
- A part swapped for a look-alike won't be flagged; the task is "missing", not "wrong".

## Data

No public dataset had one board photographed many times with parts removed, so I
made my own with ChatGPT. Details in [sample_images/PROMPTS.md](sample_images/PROMPTS.md).
