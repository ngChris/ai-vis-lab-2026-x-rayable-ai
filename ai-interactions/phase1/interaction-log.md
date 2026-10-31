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

# AI Interaction 002 — Create a widget in IPython Notebook to switch projections

## 1. Prompt 

How could i build a widget in python with controls to allow the user switch projection methods ( PCA, UMAP, t-SNE)?

## 2. AI Response

Yes. For your project, I’d make the projection itself a reusable function and put a small control panel around it:
- Projection: PCA / UMAP / t-SNE
- Color by: prediction error, pathology, age, sex, AP/PA view
- Parameters: perplexity for t-SNE; n_neighbors and min_dist for UMAP
- Run/update button
- Hover/click: show the corresponding X-ray and metadata

Example: 

run_button.on_click(update_plot)

controls = widgets.VBox([
    method_dropdown,
    color_dropdown,
    neighbors_slider,
    min_dist_slider,
    perplexity_slider,
    run_button
])

display(widgets.HBox([
    controls,
    output
]))

## 3. What we did


# AI Interaction 003 — Help to understand the visualizations

# 1. Prompt

can you analyze and interpret this plots. The binary scatter plots show the ground truth label,s the model score shows how the model predicted.

# 2. AI Response

I would summarize the current findings in three points:
1. No clear disease-specific separation: The ground-truth labels overlap substantially in the UMAP projection. This indicates that the displayed representation does not yield an obvious separation of positive and negative cases for any of the three conditions.
2. Prediction scores vary throughout the embedding: The model assigns different scores to images across the projected space. However, the current score plots do not establish whether those predictions are correct.
3. The next step should focus on systematic errors: Comparing the labels and scores directly, then identifying false positives and false negatives, would provide a more informative investigation of model behavior.

What I would investigate next
For your current Phase I investigation, I recommend three analyses. They build directly on your existing visualizations and can produce stronger, more defensible findings.
Analysis 1: Overlay ground-truth labels and model scores
Create one plot per condition in which:
- All images are shown in light blue.
- Ground-truth-positive images are highlighted in red.
- The model score is represented by point size or an additional visual encoding.
An alternative is to create an interactive scatter plot in which hovering over a point reveals its ground-truth label and predicted score.

This makes it possible to examine individual examples while retaining the overall distribution.

For instance, you could investigate whether high-score images in the lower-right region are predominantly positive or negative.

Research question: Are the model's high-confidence predictions concentrated in regions containing ground-truth-positive images?
Analysis 2: Identify false positives and false negatives
This is my strongest recommendation.

Choose a classification threshold for each condition and divide the predictions into four groups:
Category	Ground truth	Model prediction	Interpretation
True positive	Positive	Positive	Correctly detected condition
False positive	Negative	Positive	Model predicts a condition absent from the label
True negative	Negative	Negative	Correctly predicts absence
False negative	Positive	Negative	Model misses a positive example


You can then color the UMAP projection by these four categories.

This would reveal whether errors are distributed uniformly or concentrated in particular regions.

For example, you might discover that false negatives are concentrated in a particular region of the embedding. If that pattern is systematic, you can examine the corresponding images to investigate what distinguishes them from correctly detected cases.

Alternatively, you might discover that false positives occur in regions containing many negative images, suggesting that the model's prediction behavior warrants further investigation there.

These are hypotheses to test, not findings that can already be established from your current figures.

Research question: Are classification errors concentrated in specific regions of the representation space?
Important note about the threshold
If your model outputs probabilities, a threshold of 0.5 is a possible starting point, but it is not necessarily appropriate for every condition.

Ideally, choose thresholds using validation data and report them explicitly. In medical image classification, the trade-off between sensitivity and specificity may be particularly important.
Analysis 3: Compare score distributions for positive and negative examples
The most direct way to assess whether the scores align with the labels is to compare their distributions.

For each condition, create a violin plot, box plot, or overlapping histogram of model scores for:
- Ground-truth-positive images.
- Ground-truth-negative images.
If the model separates the two groups well, positive examples should generally receive higher scores than negative examples.

If the distributions overlap substantially, the model may have difficulty distinguishing the groups.

This analysis is important because two-dimensional projections can obscure relationships that remain measurable in the original prediction scores.

You should also calculate:
- ROC-AUC, which measures how well the scores rank positive examples above negative examples.
- Precision and recall at a chosen threshold.
- Sensitivity and specificity, if clinically relevant.
- The number of positive and negative examples for each condition.
Because fracture and pneumothorax have relatively few positive examples in the displayed plots, the uncertainty around their evaluation metrics deserves particular attention.

## 3. What we did