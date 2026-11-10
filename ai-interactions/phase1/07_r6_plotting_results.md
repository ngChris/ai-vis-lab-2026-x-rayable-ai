# AI Interaction — Analysis of the sixth research question output

**How sensitive does the model respond to certain data augmentations?**

# 1. Prompt
context: code of create_multi_pathology_viewer
I want to compare the changes in TP/FP/FN/TN.. the current report is simply too massive

# 2. AI Response
would remove the large create_multi_pathology_viewer entirely and create a compact comparative visualization of the confusion matrix instead.

For your augmentation analysis, two questions are particularly interesting:
1. How do TP, FP, FN, and TN change in absolute terms? For example, does changing the brightness lead to more false positives?
2. Which images change their classification? For example, how many images originally classified as TP become FN after augmentation?
I would use two heatmaps for this.

### 1. Comparing classifications across all augmentation methods

This can be displayed even more compactly using a heatmap. For each pathology, you can calculate the changes relative to the original images.

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_classification_counts(ground_truth, predictions, threshold=0.7):
    valid = np.isfinite(ground_truth) & np.isfinite(predictions)

    gt = ground_truth[valid] == 1
    pred = predictions[valid] >= threshold

    return {
        "TP": np.sum(gt & pred),
        "FP": np.sum(~gt & pred),
        "FN": np.sum(gt & ~pred),
        "TN": np.sum(~gt & ~pred)
    }


def plot_augmentation_comparison(results, ground_truth, pathology,
                                 dataset_label_indices_map,
                                 model=DENSENET121_RES244_CHEX_MODEL,
                                 threshold=0.7):

    gt_idx = dataset_label_indices_map[pathology]
    model_idx = model.pathologies.index(pathology)

    counts = {}

    for method, result in results.items():
        gt = np.asarray(ground_truth)[:, gt_idx]
        pred = np.asarray(result["predictions"])[:, model_idx]

        counts[method] = get_classification_counts(gt, pred, threshold)

    df = pd.DataFrame.from_dict(counts, orient="index")

counts, delta = plot_augmentation_comparison(
    results,
    ground_truth,
    pathology="Pneumothorax",
    dataset_label_indices_map=dataset_label_indices_map
)
```

Note: The function shown above is incomplete and does not yet calculate or return delta.

Prerequisite: results["original"] must contain the predictions for the unmodified images. Additionally, the original and augmented datasets must contain the same images in the same order.

### 2. Even more interesting: Classification transitions
The first heatmap only shows the net change. As a result, important effects may remain hidden.

Suppose ten images change from TP to FN after augmentation, while another ten change from FN to TP. The total number of TP and FN remains unchanged, even though twenty classifications have changed.

Therefore, I would additionally visualize a transition matrix.

Example: Original → Augmented
Original ↓ / Augmented →	TP	FP	FN	TN
TP	120	0	18	0
FP	0	42	0	15
FN	7	0	36	0
TN	0	11	0	290

Illustrative values. Rows represent the original classification; columns represent the classification after augmentation. The diagonal represents unchanged classifications.

```python
def plot_classification_transitions(
    original_predictions,
    augmented_predictions,
    ground_truth,
    threshold=0.7
):
    gt = np.asarray(ground_truth)
    original = np.asarray(original_predictions)
    augmented = np.asarray(augmented_predictions)

    valid = (
        np.isfinite(gt)
        & np.isfinite(original)
        & np.isfinite(augmented)
    )

    gt = gt[valid] == 1

    def classify(pred):
        positive = pred >= threshold
        return np.select(
            [gt & positive, ~gt & positive, gt & ~positive],
            ["TP", "FP", "FN"],
            default="TN"
        )

    before = classify(original[valid])
    after = classify(augmented[valid])

    labels = ["TP", "FP", "FN", "TN"]

    matrix = pd.crosstab(
        pd.Categorical(before, categories=labels),
        pd.Categorical(after, categories=labels),
        dropna=False
    )

    plt.figure(figsize=(5, 4))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("After augmentation")
    plt.ylabel("Original")
    plt.tight_layout()
    plt.show()

    return matrix
```

Example:

```python
pathology = "Pneumothorax"

gt_idx = dataset_label_indices_map[pathology]
pred_idx = DENSENET121_RES244_CHEX_MODEL.pathologies.index(pathology)

transitions = plot_classification_transitions(
    original_predictions=results["original"]["predictions"][:, pred_idx],
    augmented_predictions=results["brightness"]["predictions"][:, pred_idx],
    ground_truth=ground_truth[:, gt_idx]
)
```

### 3. Simplifying your function
Your compare_augmentations() function does not need the Downprojector or the visualization functions for this purpose. You can calculate the predictions once and subsequently analyze any pathology.

```python
def compare_augmentations(
    datasets,
    model=DENSENET121_RES244_CHEX_MODEL
):
    results = {}

    for method, dataset in datasets.items():
        print(f"Processing: {method}")

        features, predictions = process_augmented_dataset(dataset, model)

        results[method] = {
            "predictions": predictions
        }

    return results
```
If you still need features for your PCA/kNN comparison, I would naturally keep them as well.

My recommendation for your X-Rayable-AI project: Use the first heatmap to provide an overview of all augmentations and the transition matrix for a more detailed analysis of individual methods.

The transitions TP → FN and TN → FP are particularly interesting because they show which previously correct decisions become incorrect after augmentation.

It is also important to reuse the original ground-truth labels only for label-preserving augmentations. For X-ray images, strong cropping or flipping, for example, may change the clinical meaning.


# 3. What we did
We replaced the large visualization output with heatmaps showing changes in TP, FP, FN, and TN using a threshold of 0.7.
We also compared prediction scores before and after augmentation across different pathologies.
Additionally to classification transition matrices, we added ROC and Precision–Recall curves to see whether the model's discriminative performance changes.
Finally, we combined everything into a dashboard to make comparisons easier.