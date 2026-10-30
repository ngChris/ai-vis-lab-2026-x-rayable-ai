# AI Interaction 001 — Support creating basic visualizations

**Context** Help to build a simple visualizations tool for the data

## 1. Prompt

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

## 2. AI Response

# --------------------------------------------------
# 4. Plot each pathology separately
# --------------------------------------------------

pathologies = [
    "Lung Opacity",
    "Fracture",
    "Nodule/Mass",
    "Pneumothorax"
]

# Align label columns to the requested pathology names.
# This avoids silently assuming the dataset's label order.
dataset_pathologies = list(dataset.pathologies)
label_indices = [
    dataset_pathologies.index(name) for name in pathologies
]

fig, axes = plt.subplots(
    2, 2, figsize=(15, 12), constrained_layout=True
)

axes = axes.ravel()

for j, pathology in enumerate(pathologies):
    ax = axes[j]
    col = label_indices[j]

    y = labels[:, col]

    # TorchXRayVision labels can use NaN for unknown labels.
    known = np.isfinite(y)
    positive = known & (y == 1)
    negative = known & (y == 0)
    unknown = ~known

    ax.scatter(
        embeddings_2d[negative, 0],
        embeddings_2d[negative, 1],
        c="#8A9BA8",
        s=28,
        alpha=0.55,
        edgecolors="none",
        label="Negative"
    )

    ax.scatter(
        embeddings_2d[positive, 0],
        embeddings_2d[positive, 1],
        c="#E45756",
        s=42,
        alpha=0.85,
        edgecolors="white",
        linewidths=0.35,
        label="Positive"
    )

    if unknown.any():
        ax.scatter(
            embeddings_2d[unknown, 0],
            embeddings_2d[unknown, 1],
            c="#D8D8D8",
            s=18,
            alpha=0.4,
            marker="x",
            label="Unknown"
        )

    ax.set_title(
        f"{pathology}\n"
        f"Positive: {positive.sum()} | "
        f"Negative: {negative.sum()} | "
        f"Unknown: {unknown.sum()}",
        fontsize=12
    )

    ax.set_xlabel("t-SNE dimension 1")
    ax.set_ylabel("t-SNE dimension 2")
    ax.grid(alpha=0.15)
    ax.legend(frameon=False, fontsize=9)

fig.suptitle(
    "DenseNet Feature Space of Chest X-rays",
    fontsize=17,
    fontweight="bold"
)

plt.show()

## 3. What we did

**Decision:** Modified

We copied some ideas but implemented most of the visualizations on our own as the provides implementation was too overengineered and difficult to read.

# AI Interaction 002 — Support creating basic visualizations

## 1. Prompt 

How could i build a widget in python with controls to allow the user switch projection methods ( PCA, UMAP, t-SNE)?

## 2. AI Response

Yes. For your project, I’d make the projection itself a reusable function and put a small control panel around it:
- Projection: PCA / UMAP / t-SNE
- Color by: prediction error, pathology, age, sex, AP/PA view
- Parameters: perplexity for t-SNE; n_neighbors and min_dist for UMAP
- Run/update button
- Hover/click: show the corresponding X-ray and metadata