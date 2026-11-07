# AI Interaction 000 — Support creating basic visualizations

**Context** Help to build a simple visualizations tool for the data in Python.

## 1. Prompt

```
import torchxrayvision as xrv
import skimage, torch, torchvision
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import rotate

def load_model():
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    model.eval()
    return model

def load_dataset():
    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),xrv.datasets.XRayResizer(224)])
    d_nih = xrv.datasets.NIH_Google_Dataset(imgpath="./nih_data", transform=transform)
    return d_nih


i want to create a scatter plot to better understand how the model behaves. pls add a suitable downprojection method and visualze the datapoints meaninfully. use color to distinguish between classes.

```

## 2. AI Response

[Setup AI Response](./00_interaction-log-setup_ai_output.md)

## 3. What we did

**Decision:** Modified

We copied some ideas but implemented most of the visualizations on our own as the provides implementation was too overengineered and difficult to read.

