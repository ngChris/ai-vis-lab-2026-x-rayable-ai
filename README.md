# ai-vis-lab-2026-x-rayable-ai

# Task
Multi-label detection of findings on chest X-rays. We study what drives the model's false positives and false negatives.

Phase I: we treat the model as a black box. We relate its errors and confidence to patient and image attributes such as age, sex, view (AP/PA) and how the image was taken. We also test how the predictions shift under image augmentations and perturbations.
Phase II: we open the model to check whether the error patterns found in Phase I come from different image regions or learned features.

# Model
TorchXRayVision DenseNet-121 (densenet121-res224-chex), a pretrained chest X-ray classifier. We deliberately use the version trained only on CheXpert (Stanford Hospital). It has never seen an NIH image, so our whole dataset is an external test set. The library's default version (densenet121-res224-all) was trained on NIH data that includes most of our test images.

# Dataset

NIH ChestX-ray14, the subset relabelled by Google radiologists (Majkowska et al., Radiology 2020): 4,376 images from 1,695 patients, with reference labels from panels of radiologists. We use the findings that both the dataset and the model cover. The metadata includes age, sex and view. The original NIH text-mined labels are also available, so we can compare them with the expert labels.

Additional dataset (optional): If we cannot obtain access to the full CheXpert dataset from Stanford, we may use the publicly available CheXpert-v1.0-small version on Kaggle, which provides an alternative source of chest X-ray images and metadata.

# Links

1. Paper (TorchXRayVision): https://arxiv.org/abs/2111.00595
2. Model / code: https://github.com/mlmed/torchxrayvision
3. Documentation: https://mlmed.org/torchxrayvision/
4. Training data of the model (CheXpert): https://arxiv.org/abs/1901.07031
5. Dataset labels (Google relabels): https://pubs.rsna.org/doi/10.1148/radiol.2019191293
6. Dataset images (NIH ChestX-ray14): https://www.kaggle.com/datasets/nih-chest-xrays/data
7. Kaggle (CheXpert-v1.0-small): https://www.kaggle.com/datasets/ashery/chexpert
