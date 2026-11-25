"""
xray_dashboard
==============

Library version of ``r0_dataset_overiew_dashboard.ipynb`` (matplotlib edition).

Contents
--------
- Loading of the torchxrayvision model and dataset (CheXpert by default).
- Metadata extraction (gender, age, view).
- Model predictions aligned to the dataset's pathology order.
- Confusion matrix / ROC / PR evaluation figure.
- ``Downprojector`` (PCA, t-SNE, UMAP, supervised UMAP) with caching.
- Matplotlib drawing functions + figure functions for embedding spaces.
- An ipywidgets viewer and a multi-pathology comparison subplot.

Hover tooltips
--------------
Matplotlib has no built-in hover. If ``mplcursors`` is installed
(``pip install mplcursors``) and an interactive backend is active
(``%matplotlib widget`` via ``ipympl``), scatter points show the same
metadata tooltip the plotly version had. With the static inline backend the
plots work, just without tooltips.

Nothing heavy runs on import. Typical notebook usage::

    %matplotlib widget        # or: %matplotlib inline (no hover)

    import xray_dashboard as xd

    ctx = xd.build_context(image_path="./chest_data", max_number_of_data=10_000)
    xd.print_dataset_stats(ctx)

    xd.show_confusion_roc_pr_curves(ctx.labels, ctx.scores, ctx.pathologies, ctx.threshold)

    dp = xd.Downprojector(ctx.flat_features())
    xd.create_viewer(ctx, dp, xd.visualize_space)
    xd.create_viewer(ctx, dp, xd.visualize_space_prediction_scores)
    xd.create_viewer(ctx, dp, xd.visualize_classification_outcome)

    xd.create_subplot_for_visualization_fn(
        ctx, dp, "S-UMAP",
        [xd.visualize_space_prediction_scores_traces, xd.visualize_classification_outcome_traces],
        ["Model Confidence", "Classification outcomes"],
        output_file=f"{xd.HTML_OUTPUT_FOLDER}/pathology_comparison.png",
    )
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np
import pandas as pd
import torch
import torchvision
import torchxrayvision as xrv

import matplotlib.pyplot as plt
from matplotlib import cm as mpl_cm
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.transforms import blended_transform_factory

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import (
    auc,
    average_precision_score,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
)
import umap.umap_ as umap

__all__ = [
    # constants
    "DEVICE", "RANDOM_STATE", "MAX_NUMBER_OF_DATA", "THRESHOLD", "MODEL_NAME",
    "DATASET_IMAGE_PATH", "DATASET_XRAYTORCH_CLASS", "HTML_OUTPUT_FOLDER",
    "PROJECTION_METHODS",
    # loading
    "load_model", "load_dataset", "get_model_pathologies",
    "get_patient_gender", "get_patient_age", "get_dataset_views",
    "create_image_feature_space_and_label", "get_model_to_dataset_indices",
    # predictions
    "calculate_model_predictions_score", "convert_to_dataset_label_list",
    # context
    "XRayContext", "build_context", "print_dataset_stats",
    # evaluation
    "assert_input_valid", "show_confusion_roc_pr_curves",
    # projection
    "Downprojector",
    # visualization
    "XRayVisualizationData", "VisualizationFunction", "make_visualization_data",
    "create_hover_template", "enable_hover",
    "visualize_space_traces", "visualize_space",
    "visualize_space_prediction_scores_traces", "visualize_space_prediction_scores",
    "visualize_classification_outcome_traces", "visualize_classification_outcome",
    "create_viewer", "create_subplot_for_visualization_fn",
]

# ---------------------------------------------------------------------------
# 1 Constants and defaults
# ---------------------------------------------------------------------------

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Fixed seed for reproducibility
RANDOM_STATE = 42

# From the ~65 000 images we only load a subset
MAX_NUMBER_OF_DATA = 10000

# or use 0.5
THRESHOLD = 0.7

MODEL_NAME = "densenet121-res224-chex"

# The path where the images for the dataset are stored.
DATASET_IMAGE_PATH = "./chest_data"
# DATASET_IMAGE_PATH = './nih_data_small'

# xrv.datasets.NIH_Dataset / xrv.datasets.NIH_Google_Dataset
DATASET_XRAYTORCH_CLASS = xrv.datasets.CheX_Dataset

HTML_OUTPUT_FOLDER = "html_plots/r0"

PROJECTION_METHODS = ["PCA", "t-SNE", "UMAP", "S-UMAP"]


# ---------------------------------------------------------------------------
# 2 Model
# ---------------------------------------------------------------------------

def load_model(model_weights: str = MODEL_NAME, device: torch.device = DEVICE):
    model = xrv.models.DenseNet(weights=model_weights)
    model.eval()
    return model.to(device)


def get_model_pathologies(model) -> list[str]:
    return [str(p) for p in model.pathologies if p != ""]


# ---------------------------------------------------------------------------
# 3 Dataset
# ---------------------------------------------------------------------------

def load_dataset(
    image_path: str = DATASET_IMAGE_PATH,
    dataset_class=DATASET_XRAYTORCH_CLASS,
    unique_patients: bool = True,
    views: tuple[str, ...] = ("PA", "AP"),
    verbose: bool = True,
):
    transform = torchvision.transforms.Compose(
        [xrv.datasets.XRayCenterCrop(), xrv.datasets.XRayResizer(224)]
    )
    dataset = dataset_class(
        imgpath=image_path,
        transform=transform,
        views=list(views),
        unique_patients=unique_patients,
    )
    if verbose:
        print(f"found {len(dataset)} images")
    return dataset


def _metadata(dataset) -> pd.DataFrame:
    metadata = getattr(dataset, "csv", None)
    if metadata is None:
        raise ValueError("Dataset has no `csv` metadata attribute.")
    return metadata


def get_patient_gender(dataset) -> np.ndarray:
    """0.0 = male, 1.0 = female, 2.0 = unknown."""
    metadata = _metadata(dataset)

    def normalize_gender(value):
        value = str(value).strip().lower()
        if value in ("m", "male"):
            return 0.0
        if value in ("f", "female"):
            return 1.0
        return 2.0

    column = "Sex" if "Sex" in metadata else "Patient Gender"
    return metadata[column].map(normalize_gender).to_numpy()


def get_patient_age(dataset) -> np.ndarray:
    """Integer ages; -1 where the value cannot be parsed."""
    metadata = _metadata(dataset)

    def parse_age(value):
        try:
            return int(float(str(value).strip()))
        except ValueError:
            # TODO: handle properly
            return -1

    column = "Age" if "Age" in metadata else "Patient Age"
    return metadata[column].map(parse_age).to_numpy()


def get_dataset_views(dataset) -> np.ndarray:
    """Lower-cased view strings, e.g. 'ap' / 'pa'."""
    metadata = _metadata(dataset)
    column = "AP/PA" if "AP/PA" in metadata else "View Position"
    return metadata[column].map(lambda v: str(v).strip().lower()).to_numpy()


def create_image_feature_space_and_label(
    dataset,
    dataset_pathologies: list[str],
    dataset_label_indices_map: Optional[dict[str, int]] = None,
):
    """Return ``(images[N, 224, 224] float32, labels[N, n_pathologies])``.

    NaN labels are replaced with 0. Labels are reordered to match
    ``dataset_pathologies``.
    """
    if dataset_label_indices_map is None:
        dataset_label_indices_map = {n: i for i, n in enumerate(dataset_pathologies)}

    source_indices, target_indices = [], []
    for org_index, path in enumerate(dataset.pathologies):
        if path in dataset_label_indices_map:
            source_indices.append(org_index)
            target_indices.append(dataset_label_indices_map[path])
    source_indices = np.asarray(source_indices)
    target_indices = np.asarray(target_indices)

    n_labels = len(dataset_pathologies)
    image_features, labels = [], []

    for i in range(len(dataset)):
        sample = dataset[i]
        image_features.append(np.asarray(sample["img"], dtype=np.float32).squeeze())

        label = np.nan_to_num(np.asarray(sample["lab"]).reshape(-1))
        adapted = np.zeros(n_labels, dtype=label.dtype)
        adapted[target_indices] = label[source_indices]
        labels.append(adapted)

    return np.asarray(image_features, dtype=np.float32), np.stack(labels)


def get_model_to_dataset_indices(model, dataset_label_indices_map: dict[str, int]) -> dict[int, int]:
    return {
        model_idx: dataset_label_indices_map[pathology]
        for model_idx, pathology in enumerate(model.pathologies)
        if pathology in dataset_label_indices_map
    }


# ---------------------------------------------------------------------------
# 4 Model predictions
# ---------------------------------------------------------------------------

def calculate_model_predictions_score(
    feature_space: np.ndarray,
    model,
    batch_size: int = 32,
    device: Optional[torch.device] = None,
) -> np.ndarray:
    """Raw model outputs, shape ``(N, n_model_pathologies)`` in model order."""
    model.eval()
    if device is None:
        device = next(model.parameters()).device

    images = torch.as_tensor(feature_space, dtype=torch.float32).reshape(-1, 1, 224, 224)

    all_outputs = []
    with torch.no_grad():
        for start in range(0, len(images), batch_size):
            batch = images[start:start + batch_size].to(device)
            all_outputs.append(model(batch).cpu().numpy())

    return np.concatenate(all_outputs, axis=0)


def convert_to_dataset_label_list(
    model_prediction_score: np.ndarray,
    dataset_labels_list: np.ndarray,
    dataset_to_model_indices_map: dict[int, int],
) -> np.ndarray:
    """Reorder model outputs into the dataset's label columns."""
    converted = np.zeros_like(dataset_labels_list, dtype=np.float32)
    for dataset_idx, model_idx in dataset_to_model_indices_map.items():
        converted[:, dataset_idx] = model_prediction_score[:, model_idx]
    return converted


def assert_input_valid(y_true: np.ndarray, y_scores: np.ndarray):
    assert y_true.shape == y_scores.shape, f"Shape mismatch: {y_true.shape} vs {y_scores.shape}"
    assert y_true.ndim == 2, f"Expected 2D arrays, got {y_true.ndim}D"


# ---------------------------------------------------------------------------
# Context: everything the notebook kept as globals
# ---------------------------------------------------------------------------

@dataclass
class XRayContext:
    model: object
    dataset: object
    pathologies: list[str]
    label_indices_map: dict[str, int]
    indices_label_map: dict[int, str]
    model_to_dataset_indices_map: dict[int, int]
    dataset_to_model_indices_map: dict[int, int]
    image_features: np.ndarray          # (N, 224, 224)
    labels: np.ndarray                  # (N, n_pathologies)
    gender: np.ndarray                  # (N,)
    ages: np.ndarray                    # (N,)
    views: np.ndarray                   # (N,)
    scores: np.ndarray                  # (N, n_pathologies), dataset order
    threshold: float = THRESHOLD
    predictions: np.ndarray = field(init=False)

    def __post_init__(self):
        self.predictions = (self.scores >= self.threshold).astype(int)

    def set_threshold(self, threshold: float):
        self.threshold = threshold
        self.predictions = (self.scores >= threshold).astype(int)

    def flat_features(self) -> np.ndarray:
        """Images flattened to ``(N, 224*224)`` for the Downprojector."""
        return self.image_features.reshape(len(self.image_features), -1)


def build_context(
    image_path: str = DATASET_IMAGE_PATH,
    dataset_class=DATASET_XRAYTORCH_CLASS,
    model_name: str = MODEL_NAME,
    model=None,
    max_number_of_data: int = MAX_NUMBER_OF_DATA,
    threshold: float = THRESHOLD,
    random_state: int = RANDOM_STATE,
    unique_patients: bool = True,
    sample_with_replacement: bool = True,
    batch_size: int = 32,
    device: torch.device = DEVICE,
    verbose: bool = True,
) -> XRayContext:
    """Run the notebook's full load → align → predict pipeline.

    ``sample_with_replacement=True`` reproduces the notebook exactly (it can
    pick the same image more than once); set ``False`` for unique images.
    """
    rng = np.random.default_rng(random_state)

    if model is None:
        model = load_model(model_name, device=device)
    model_pathologies = get_model_pathologies(model)

    dataset = load_dataset(image_path, dataset_class, unique_patients, verbose=verbose)

    # Filter out pathologies the model does not predict and align labels
    pathologies = [str(p) for p in dataset.pathologies if p in model_pathologies]
    xrv.datasets.relabel_dataset(pathologies, dataset)

    n = min(max_number_of_data, len(dataset))
    idxs = rng.choice(len(dataset), size=n, replace=sample_with_replacement)
    dataset = xrv.datasets.SubsetDataset(dataset, idxs=idxs)

    label_indices_map = {name: i for i, name in enumerate(pathologies)}
    indices_label_map = {i: name for name, i in label_indices_map.items()}

    if verbose:
        print(f"Loaded {len(dataset)} images")
        print(f"There are now {len(dataset.pathologies)} pathologies.")

    gender = get_patient_gender(dataset)
    ages = get_patient_age(dataset)
    views = get_dataset_views(dataset)

    image_features, labels = create_image_feature_space_and_label(
        dataset, pathologies, label_indices_map
    )

    model_to_dataset = get_model_to_dataset_indices(model, label_indices_map)
    dataset_to_model = {v: k for k, v in model_to_dataset.items()}

    raw_scores = calculate_model_predictions_score(image_features, model, batch_size, device)
    scores = convert_to_dataset_label_list(raw_scores, labels, dataset_to_model)

    return XRayContext(
        model=model,
        dataset=dataset,
        pathologies=pathologies,
        label_indices_map=label_indices_map,
        indices_label_map=indices_label_map,
        model_to_dataset_indices_map=model_to_dataset,
        dataset_to_model_indices_map=dataset_to_model,
        image_features=image_features,
        labels=labels,
        gender=gender,
        ages=ages,
        views=views,
        scores=scores,
        threshold=threshold,
    )


def print_dataset_stats(ctx: XRayContext):
    print("Dataset statistics")
    print("=" * 50)
    print(f"Total number of samples: {len(ctx.dataset)}")
    print(f"Number of pathologies: {len(ctx.pathologies)}")
    print()
    for i, pathology in enumerate(ctx.pathologies):
        col = ctx.labels[:, i]
        print(
            f"{pathology:25s} "
            f"positive: {np.sum(col == 1):5d} | "
            f"negative: {np.sum(col == 0):5d} | "
            f"uncertain: {np.sum(col == -1):5d}"
        )



# ---------------------------------------------------------------------------
# 5 Confusion matrix and ROC/PR curves
# ---------------------------------------------------------------------------

def show_confusion_roc_pr_curves(
    y_true: np.ndarray,
    y_scores: np.ndarray,
    pathology_names: list[str],
    threshold: float = THRESHOLD,
    show: bool = True,
) -> dict:
    """Per-pathology metrics plus the figure under ``results["figure"]``."""
    n_pathologies = len(pathology_names)
    assert_input_valid(y_true, y_scores)

    fig, axes = plt.subplots(
        n_pathologies, 3,
        figsize=(15, max(6.5, 4.2 * n_pathologies)),
        squeeze=False,
        layout="constrained",
    )
    column_titles = ["Confusion Matrix", "ROC Curve", "Precision-Recall Curve"]
    for col, title in enumerate(column_titles):
        axes[0, col].set_title(title, fontsize=13, fontweight="bold", pad=12)

    results = {}

    for i, pathology in enumerate(pathology_names):
        ax_cm, ax_roc, ax_pr = axes[i]
        true = y_true[:, i]
        scores = y_scores[:, i]
        pred = (scores >= threshold).astype(int)

        cm = confusion_matrix(true, pred, labels=[0, 1])
        tn, fp, fn, tp = cm.ravel()

        if len(np.unique(true)) != 2:
            raise RuntimeError(
                f"{pathology}: ROC/PR curves need exactly two label values, "
                f"got {np.unique(true).tolist()}"
            )

        fpr, tpr, roc_thresholds = roc_curve(true, scores)
        roc_auc = auc(fpr, tpr)
        precision, recall, pr_thresholds = precision_recall_curve(true, scores)
        ap = average_precision_score(true, scores)
        prevalence = np.mean(true)

        results[pathology] = {
            "confusion_matrix": cm,
            "TN": tn, "FP": fp, "FN": fn, "TP": tp,
            "fpr": fpr, "tpr": tpr, "roc_thresholds": roc_thresholds, "roc_auc": roc_auc,
            "precision": precision, "recall": recall, "pr_thresholds": pr_thresholds,
            "average_precision": ap,
            "prevalence": prevalence,
        }

        # Confusion matrix (row 0 = Actual Negative on top, like the plotly version)
        ax_cm.imshow(cm, cmap="Blues", aspect="auto")
        vmax = cm.max() if cm.max() > 0 else 1
        for r in range(2):
            for c in range(2):
                ax_cm.text(
                    c, r, f"{cm[r, c]}", ha="center", va="center", fontsize=12,
                    color="white" if cm[r, c] > vmax / 2 else "black",
                )
        ax_cm.set_xticks([0, 1], ["Predicted Negative", "Predicted Positive"])
        ax_cm.set_yticks([0, 1], ["Actual Negative", "Actual Positive"])
        ax_cm.set_xlabel("Predicted")

        # ROC
        ax_roc.plot(fpr, tpr, lw=2.5, color="C0")
        ax_roc.plot([0, 1], [0, 1], ls="--", color="gray", lw=1)
        ax_roc.set_xlim(0, 1)
        ax_roc.set_ylim(0, 1)
        ax_roc.set_xlabel("False Positive Rate")
        ax_roc.set_ylabel("True Positive Rate")

        # Precision-recall
        ax_pr.plot(recall, precision, lw=2.5, color="C0")
        ax_pr.axhline(prevalence, ls="--", color="gray", lw=1)
        ax_pr.text(
            0.98, prevalence, f"Prevalence = {prevalence:.3f}",
            transform=blended_transform_factory(ax_pr.transAxes, ax_pr.transData),
            ha="right", va="bottom", fontsize=9, color="dimgray",
        )
        ax_pr.set_xlim(0, 1)
        ax_pr.set_ylim(0, 1)
        ax_pr.set_xlabel("Recall")
        ax_pr.set_ylabel("Precision")

        for ax in (ax_roc, ax_pr):
            ax.grid(alpha=0.3)
            ax.spines[["top", "right"]].set_visible(False)

        # Row label with AUC / AP on the left
        auc_text = "AUC = N/A" if np.isnan(roc_auc) else f"AUC = {roc_auc:.3f}"
        ap_text = "AP = N/A" if np.isnan(ap) else f"AP = {ap:.3f}"
        for text, va, weight, size in (
            (pathology, "bottom", "bold", 11),
            (f"{auc_text} | {ap_text}", "top", "normal", 9),
        ):
            ax_cm.annotate(
                text, xy=(0, 0.5), xycoords="axes fraction",
                xytext=(-100, 0), textcoords="offset points",
                ha="right", va=va, fontsize=size, fontweight=weight,
            )

    fig.suptitle(
        f"Multi-Label Chest X-Ray Model Evaluation\nClassification threshold = {threshold}",
        fontsize=14,
    )

    if show:
        plt.show()

    results["figure"] = fig
    return results


# ---------------------------------------------------------------------------
# 6 Downprojection
# ---------------------------------------------------------------------------

class Downprojector:
    """Projects a feature matrix to 2D and caches the results.

    ``image_features`` must be 2D, e.g. ``ctx.flat_features()``.
    """

    def __init__(self, image_features: np.ndarray, random_state: int = RANDOM_STATE):
        self.projection_cache: dict = {}
        self.image_features = image_features
        self.random_state = random_state

    def get_feature_matrix(self, feature_space: str = "feature") -> np.ndarray:
        return self.image_features

    def prepare_pca_features(self, feature_space: str = "feature") -> dict:
        cache_key = f"{feature_space}_pca"
        if cache_key in self.projection_cache:
            return self.projection_cache[cache_key]

        X = self.get_feature_matrix(feature_space)
        # Keep at most 50 dimensions before expensive non-linear reduction.
        n_components = min(50, X.shape[0], X.shape[1])
        pca = PCA(n_components=n_components, random_state=self.random_state)
        X_pca = pca.fit_transform(X)

        self.projection_cache[cache_key] = {"data": X_pca, "pca": pca}
        return self.projection_cache[cache_key]

    def _umap(self, n_samples: int):
        return umap.UMAP(
            n_components=2,
            n_neighbors=min(15, max(2, n_samples - 1)),
            min_dist=0.1,
            metric="euclidean",
            random_state=self.random_state,
        )

    def calculate_projection(
        self,
        feature_space: str,
        method: str,
        target_labels: Optional[np.ndarray] = None,
        label_name: Optional[str] = None,
        dataset_label_to_index_map: Optional[dict[str, int]] = None,
    ) -> np.ndarray:
        # Only supervised UMAP depends on the label; unsupervised methods are
        # cached once regardless of which pathology is selected.
        if method == "S-UMAP":
            cache_key = f"{feature_space}_{method}_{label_name}"
        else:
            cache_key = f"{feature_space}_{method}"

        if cache_key in self.projection_cache:
            return self.projection_cache[cache_key]

        if method == "PCA":
            X = self.get_feature_matrix(feature_space)
            embedding = PCA(n_components=2, random_state=self.random_state).fit_transform(X)

        elif method == "t-SNE":
            X_pca = self.prepare_pca_features(feature_space)["data"]
            # t-SNE requires perplexity < number of samples.
            perplexity = min(30, max(5, (X_pca.shape[0] - 1) // 3))
            embedding = TSNE(
                n_components=2,
                perplexity=perplexity,
                init="pca",
                learning_rate="auto",
                random_state=self.random_state,
            ).fit_transform(X_pca)

        elif method == "UMAP":
            X_pca = self.prepare_pca_features(feature_space)["data"]
            embedding = self._umap(X_pca.shape[0]).fit_transform(X_pca)

        elif method == "S-UMAP":
            if target_labels is None:
                raise ValueError("Supervised UMAP needs target labels")
            if label_name is None:
                raise ValueError("Supervised UMAP needs a label name / pathology")
            if dataset_label_to_index_map is None:
                raise ValueError("Supervised UMAP needs dataset_label_to_index_map")

            X_pca = self.prepare_pca_features(feature_space)["data"]
            Y = target_labels[:, dataset_label_to_index_map[label_name]]
            embedding = self._umap(X_pca.shape[0]).fit_transform(X_pca, Y)

        else:
            raise ValueError(f"Unknown projection method: {method}")

        self.projection_cache[cache_key] = embedding
        return embedding



# ---------------------------------------------------------------------------
# 7 Generic viewer data contract
# ---------------------------------------------------------------------------

@dataclass
class XRayVisualizationData:
    feature_space: np.ndarray           # 2D embedding (N, 2)
    projection_method: str

    model_score_predictions: np.ndarray
    ground_truth: np.ndarray
    dataset_label_indices_map: dict

    dataset_gender_list: np.ndarray
    dataset_ages: np.ndarray

    selected_pathology: str
    threshold: float
    y_true: np.ndarray = None
    y_pred: np.ndarray = None
    y_scores: np.ndarray = None

    def __post_init__(self):
        label_idx = self.dataset_label_indices_map[self.selected_pathology]
        self.y_true = np.asarray(self.ground_truth[:, label_idx])
        self.y_scores = np.asarray(self.model_score_predictions[:, label_idx])
        self.y_pred = (self.y_scores >= self.threshold).astype(int)


# A visualization function takes the data and either shows a figure
# (``visualize_*``) or draws onto a given matplotlib Axes and returns the
# list of scatter artists (``visualize_*_traces(data, ax=...)``).
VisualizationFunction = Callable[..., object]


def make_visualization_data(
    ctx: XRayContext,
    embedding: np.ndarray,
    projection_method: str,
    pathology: str,
    threshold: Optional[float] = None,
) -> XRayVisualizationData:
    return XRayVisualizationData(
        feature_space=embedding,
        projection_method=projection_method,
        model_score_predictions=ctx.scores,
        ground_truth=ctx.labels,
        dataset_label_indices_map=ctx.label_indices_map,
        dataset_gender_list=ctx.gender,
        dataset_ages=ctx.ages,
        selected_pathology=pathology,
        threshold=ctx.threshold if threshold is None else threshold,
    )


_GENDER_NAMES = {0.0: "Male", 1.0: "Female", 2.0: "Unknown"}


def create_hover_template(data: XRayVisualizationData, mask: np.ndarray, name: str = ""):
    """Return ``(customdata, formatter)`` for the points selected by ``mask``.

    ``formatter(i)`` builds the tooltip text for the i-th point of the masked
    subset (same fields as the plotly hovertemplate). Used by ``enable_hover``.
    """
    coords = data.feature_space[mask]
    customdata = np.column_stack((
        data.y_true[mask],
        data.y_scores[mask],
        data.y_pred[mask],
        np.asarray(data.dataset_ages)[mask],
        np.asarray(data.dataset_gender_list)[mask],
    ))

    def formatter(i: int) -> str:
        gt, score, pred, age, gender = customdata[i]
        return (
            f"{name}\n"
            f"Component 1: {coords[i, 0]:.3f}\n"
            f"Component 2: {coords[i, 1]:.3f}\n"
            f"Ground truth: {gt:g}\n"
            f"Prediction score: {score:.3f}\n"
            f"Binary prediction: {int(pred)}\n"
            f"Age: {int(age)} years\n"
            f"Gender: {_GENDER_NAMES.get(float(gender), gender)}"
        )

    return customdata, formatter


def enable_hover(artists: list):
    """Attach metadata tooltips to scatter artists (needs ``mplcursors``).

    Returns the cursor, or ``None`` if ``mplcursors`` is not installed.
    Tooltips only appear with an interactive backend (e.g. ``%matplotlib widget``).
    """
    try:
        import mplcursors
    except ImportError:
        return None
    hoverable = [a for a in artists if getattr(a, "hover_formatter", None) is not None]
    if not hoverable:
        return None
    cursor = mplcursors.cursor(hoverable, hover=True)

    @cursor.connect("add")
    def _on_add(sel):
        sel.annotation.set_text(sel.artist.hover_formatter(sel.index))
        sel.annotation.get_bbox_patch().set(alpha=0.9, fc="white")

    return cursor


def _gender_finding_categories(data: XRayVisualizationData) -> dict[str, np.ndarray]:
    y_true = data.y_true
    gender = np.asarray(data.dataset_gender_list)
    return {
        "Finding present · Male": (y_true == 1) & (gender == 0),
        "Finding present · Female": (y_true == 1) & (gender == 1),
        "Finding absent · Male": (y_true == 0) & (gender == 0),
        "Finding absent · Female": (y_true == 0) & (gender == 1),
    }


_SEX_SYMBOLS = {"Male": "o", "Female": "^"}

# plotly marker size 7 px ≈ matplotlib s=28 (points²)
_MARKER_SIZE = 28
_MARKER_SIZE_LARGE = 45


def _scatter(ax, data, mask, name, **kwargs):
    """Scatter the masked points, label them and attach a hover formatter."""
    _, formatter = create_hover_template(data, mask, name)
    artist = ax.scatter(
        data.feature_space[mask, 0],
        data.feature_space[mask, 1],
        label=name,
        rasterized=True,
        **kwargs,
    )
    artist.hover_formatter = formatter
    return artist


def _legend_handles(artists: list) -> list:
    return [getattr(a, "legend_proxy", a) for a in artists]


def _style_axes(ax, projection_method: str):
    ax.set_xlabel(f"{projection_method} 1")
    ax.set_ylabel(f"{projection_method} 2")
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)


def _new_scatter_figure():
    return plt.subplots(figsize=(10, 7.5), layout="constrained")


def _finish_scatter_figure(fig, ax, artists, title, projection_method, legend_title, show):
    ax.set_title(title, fontsize=13)
    _style_axes(ax, projection_method)
    ax.legend(
        handles=_legend_handles(artists), title=legend_title,
        loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=4, frameon=False,
    )
    fig.hover_cursor = enable_hover(artists)  # keep a reference alive
    if show:
        plt.show()
    return fig


# ---------------------------------------------------------------------------
# 8 Embedding by ground truth and gender
# ---------------------------------------------------------------------------

def visualize_space_traces(data: XRayVisualizationData, ax=None) -> list:
    ax = plt.gca() if ax is None else ax
    colors = {"Finding present": "#D55E00", "Finding absent": "#0072B2"}
    artists = []
    for category, mask in _gender_finding_categories(data).items():
        status, sex = category.split(" · ")
        artists.append(_scatter(
            ax, data, mask, category,
            color=colors[status],
            marker=_SEX_SYMBOLS[sex],
            s=_MARKER_SIZE,
            alpha=0.75 if status == "Finding present" else 0.25,
            linewidths=0,
        ))
    return artists


def visualize_space(data: XRayVisualizationData, show: bool = True):
    fig, ax = _new_scatter_figure()
    artists = visualize_space_traces(data, ax=ax)
    return _finish_scatter_figure(
        fig, ax, artists,
        f"Distribution of Chest X-ray Embeddings by {data.selected_pathology} and Gender",
        data.projection_method, "Pathology Status and Gender", show,
    )


# ---------------------------------------------------------------------------
# 9 Embedding coloured by model score
# ---------------------------------------------------------------------------

def visualize_space_prediction_scores_traces(
    data: XRayVisualizationData, ax=None, colorbar: bool = True
) -> list:
    ax = plt.gca() if ax is None else ax
    norm = Normalize(vmin=0, vmax=1)
    cmap = plt.get_cmap("viridis")
    artists = []
    for category, mask in _gender_finding_categories(data).items():
        status, sex = category.split(" · ")
        alpha = 0.75 if status == "Finding present" else 0.25
        artist = _scatter(
            ax, data, mask, category,
            c=data.y_scores[mask],
            cmap=cmap,
            norm=norm,
            marker=_SEX_SYMBOLS[sex],
            s=_MARKER_SIZE,
            alpha=alpha,
            linewidths=0,
        )
        # Colour encodes the score, so the legend shows only the marker shape.
        artist.legend_proxy = Line2D(
            [], [], ls="", marker=_SEX_SYMBOLS[sex], color="gray",
            alpha=max(alpha, 0.5), markersize=7, label=category,
        )
        artists.append(artist)

    if colorbar:  # only one colour bar per axes
        ax.figure.colorbar(
            mpl_cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax,
            label="Model score", shrink=0.75, aspect=25,
        )
    return artists


def visualize_space_prediction_scores(data: XRayVisualizationData, show: bool = True):
    fig, ax = _new_scatter_figure()
    artists = visualize_space_prediction_scores_traces(data, ax=ax)
    return _finish_scatter_figure(
        fig, ax, artists,
        f"{data.projection_method} Projection Colored by {data.selected_pathology} Model Score",
        data.projection_method, "Pathology Status and Gender", show,
    )


# ---------------------------------------------------------------------------
# 10 Embedding coloured by TP / TN / FP / FN
# ---------------------------------------------------------------------------

_OUTCOME_COLORS = {
    "True Positive": "#009E73",
    "True Negative": "#0072B2",
    "False Positive": "#D55E00",
    "False Negative": "#CC79A7",
}


def visualize_classification_outcome_traces(data: XRayVisualizationData, ax=None) -> list:
    ax = plt.gca() if ax is None else ax
    y_true, y_pred = data.y_true, data.y_pred
    categories = {
        "True Positive": (y_true == 1) & (y_pred == 1),
        "True Negative": (y_true == 0) & (y_pred == 0),
        "False Positive": (y_true == 0) & (y_pred == 1),
        "False Negative": (y_true == 1) & (y_pred == 0),
    }
    artists = []
    for category, mask in categories.items():
        color = _OUTCOME_COLORS[category]
        artists.append(_scatter(
            ax, data, mask, category,
            color=color,
            s=_MARKER_SIZE_LARGE if "False" in category else _MARKER_SIZE,
            alpha=0.8,
            edgecolors=color,
            linewidths=0.5,
        ))
    return artists


def visualize_classification_outcome(data: XRayVisualizationData, show: bool = True):
    fig, ax = _new_scatter_figure()
    artists = visualize_classification_outcome_traces(data, ax=ax)
    return _finish_scatter_figure(
        fig, ax, artists,
        f"Classification Outcomes in {data.projection_method} Embedding Space – {data.selected_pathology}",
        data.projection_method, "Classification Outcome", show,
    )


# ---------------------------------------------------------------------------
# Interactive viewer (requires Jupyter + ipywidgets)
# ---------------------------------------------------------------------------

def create_viewer(
    ctx: XRayContext,
    downprojector: Downprojector,
    visualization_fn: VisualizationFunction,
    projection_methods: list[str] = PROJECTION_METHODS,
):
    """Dropdowns for projection + pathology, threshold slider, plot button."""
    import ipywidgets as widgets
    from IPython.display import clear_output, display

    plot_output = widgets.Output()
    progress_output = widgets.Output()

    plot_button = widgets.Button(
        description="Create selection plot", button_style="primary", icon="refresh"
    )
    pathology_dropdown = widgets.Dropdown(
        options=ctx.pathologies,
        value=ctx.pathologies[0],
        description="Pathology:",
        layout=widgets.Layout(width="350px"),
    )
    projection_dropdown = widgets.Dropdown(
        options=projection_methods,
        value=projection_methods[0],
        description="Projection:",
        layout=widgets.Layout(width="300px"),
    )
    threshold_input = widgets.FloatSlider(
        value=ctx.threshold, min=0.0, max=1.0, step=0.1, description="Threshold"
    )
    state = {"figure": None}

    def create_selection_plot(_=None):
        pathology = pathology_dropdown.value
        projection_method = projection_dropdown.value
        threshold = float(threshold_input.value)

        with progress_output:
            clear_output(wait=True)
            embedding = downprojector.calculate_projection(
                "feature",
                projection_method,
                target_labels=ctx.labels,
                label_name=pathology,
                dataset_label_to_index_map=ctx.label_indices_map,
            )

        with plot_output:
            clear_output(wait=True)
            if state["figure"] is not None:
                plt.close(state["figure"])  # don't pile up open figures
            state["figure"] = visualization_fn(
                make_visualization_data(ctx, embedding, projection_method, pathology, threshold)
            )

    plot_button.on_click(create_selection_plot)

    ui = widgets.VBox([
        widgets.HBox([projection_dropdown]),
        widgets.HBox([pathology_dropdown]),
        threshold_input,
        plot_button,
        progress_output,
        plot_output,
    ])
    display(ui)
    return ui


# ---------------------------------------------------------------------------
# 11 Comparison subplot across pathologies
# ---------------------------------------------------------------------------

def create_subplot_for_visualization_fn(
    ctx: XRayContext,
    downprojector: Downprojector,
    projection_method: str,
    visualization_fns: list[VisualizationFunction],
    visualization_names: list[str],
    pathologies: Optional[list[str]] = None,
    threshold: Optional[float] = None,
    save: bool = True,
    show: bool = True,
    output_file: str = "pathology_comparison.png",
    dpi: int = 150,
):
    """One row per pathology, one column per ``*_traces`` function.

    ``output_file`` can be any format matplotlib supports (.png, .pdf, .svg).
    """
    pathologies = ctx.pathologies if pathologies is None else pathologies
    n_rows, n_cols = len(pathologies), len(visualization_fns)

    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(max(7 * n_cols, 14), max(4 * n_rows, 8)),
        squeeze=False,
        layout="constrained",
    )

    legend_entries: dict[str, object] = {}  # label -> handle, deduplicated
    all_artists = []

    for row, pathology in enumerate(pathologies):
        embedding = downprojector.calculate_projection(  # cached
            "feature",
            projection_method,
            target_labels=ctx.labels,
            label_name=pathology,
            dataset_label_to_index_map=ctx.label_indices_map,
        )
        xray_data = make_visualization_data(ctx, embedding, projection_method, pathology, threshold)

        for col, (visualization_fn, name) in enumerate(zip(visualization_fns, visualization_names)):
            ax = axes[row, col]
            artists = visualization_fn(xray_data, ax=ax)
            ax.set_title(f"{pathology} - {name}", fontsize=11)
            _style_axes(ax, projection_method)
            all_artists.extend(artists)
            if row == 0:
                for handle in _legend_handles(artists):
                    legend_entries.setdefault(handle.get_label(), handle)

    fig.legend(
        handles=list(legend_entries.values()),
        loc="outside right upper",
        frameon=False,
    )
    fig.suptitle(f"{projection_method} - Comparison Across Pathologies", fontsize=14)
    fig.hover_cursor = enable_hover(all_artists)

    if save:
        out_dir = os.path.dirname(output_file)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        fig.savefig(output_file, dpi=dpi, bbox_inches="tight")
    if show:
        plt.show()
    return fig