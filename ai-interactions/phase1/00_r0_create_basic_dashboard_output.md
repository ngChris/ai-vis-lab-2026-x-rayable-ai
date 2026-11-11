For your torchxrayvision DenseNet model, I recommend PCA followed by UMAP or t-SNE to visualize the learned representations of the 810 chest X-rays in 2D.

The key is to visualize the model's feature embeddings, rather than the raw images or the four binary labels. This helps you investigate whether X-rays with similar learned features cluster together and whether the clusters correspond to your four pathologies:
- Lung Opacity
- Fracture
- Nodule/Mass
- Pneumothorax
Because these are multi-label data, a single X-ray can belong to multiple classes. The most meaningful visualization is therefore four separate scatter plots, one per pathology, with positive and negative examples colored differently. That avoids forcing every image into just one class.

Complete implementation
This code extracts the 1,024-dimensional feature vector immediately before the DenseNet classifier, reduces it to 2D using PCA + t-SNE, and plots the four pathologies separately.
import numpy as npimport torchimport matplotlib.pyplot as pltimport torchvisionimport torchxrayvision as xrvfrom sklearn.decomposition import PCAfrom sklearn.manifold import TSNEfrom matplotlib.lines import Line2D# --------------------------------------------------# 1. Load model and dataset# --------------------------------------------------device = torch.device("cuda" if torch.cuda.is_available() else "cpu")model = load_model().to(device)dataset = load_dataset()model.eval()# --------------------------------------------------# 2. Extract DenseNet feature embeddings# --------------------------------------------------features_list = []labels_list = []# Capture the input to the final classifier layer.# These vectors represent the learned image features.def capture_features(module, inputs):    features_list.append(inputs[0].detach().cpu().numpy())hook = model.classifier.register_forward_pre_hook(capture_features)with torch.no_grad():    for i in range(len(dataset)):        sample = dataset[i]        image = torch.as_tensor(sample["img"], dtype=torch.float32)        image = image.unsqueeze(0).to(device)        # Forward pass triggers the feature hook        _ = model(image)        labels_list.append(np.asarray(sample["lab"]).reshape(-1))hook.remove()features = np.concatenate(features_list, axis=0)labels = np.stack(labels_list, axis=0)print("Feature matrix:", features.shape)print("Label matrix:", labels.shape)



Expected feature shape: (810, 1024), assuming the dataset contains 810 images and the model's classifier uses 1,024 input features.
# --------------------------------------------------# 3. Downproject to 2D: PCA -> t-SNE# --------------------------------------------------# PCA first reduces noise and makes t-SNE more efficient.pca = PCA(n_components=min(50, features.shape[0], features.shape[1]))features_pca = pca.fit_transform(features)tsne = TSNE(    n_components=2,    perplexity=30,    init="pca",    learning_rate="auto",    random_state=42)embeddings_2d = tsne.fit_transform(features_pca)print("2D embedding:", embeddings_2d.shape)print(    f"PCA variance retained: "    f"{pca.explained_variance_ratio_.sum():.1%}")



# --------------------------------------------------# 4. Plot each pathology separately# --------------------------------------------------pathologies = [    "Lung Opacity",    "Fracture",    "Nodule/Mass",    "Pneumothorax"]# Align label columns to the requested pathology names.# This avoids silently assuming the dataset's label order.dataset_pathologies = list(dataset.pathologies)label_indices = [    dataset_pathologies.index(name) for name in pathologies]fig, axes = plt.subplots(    2, 2, figsize=(15, 12), constrained_layout=True)axes = axes.ravel()for j, pathology in enumerate(pathologies):    ax = axes[j]    col = label_indices[j]    y = labels[:, col]    # TorchXRayVision labels can use NaN for unknown labels.    known = np.isfinite(y)    positive = known & (y == 1)    negative = known & (y == 0)    unknown = ~known



How to interpret the plots
- Clear separation: Positive and negative examples occupy different regions, suggesting the learned features distinguish that pathology.
- Mixed colors: The model's features may not separate the classes cleanly, or the labels and images may be noisy.
- Small isolated clusters: These may represent unusual cases, image artifacts, or a meaningful subgroup worth investigating.
- Overlapping pathology plots: This is expected because the task is multi-label and different diseases can share visual characteristics.
Important: t-SNE preserves local neighborhood structure, not global distances. A visible cluster does not prove that the model classifies those cases correctly. For a more complete analysis, compare these plots with the model's predicted probabilities and evaluate each pathology using ROC-AUC and precision-recall metrics.

One further detail: your model's classifier has its own output pathology order. The code above visualizes the feature space using your dataset's four labels, rather than assuming those labels correspond directly to the model's output columns.