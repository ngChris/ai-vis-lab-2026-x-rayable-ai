# AI Interaction 000 — Support creating basic visualizations

**Context** Help to build a simple visualizations tool for the data in Python.

## 1. Prompt

I want to create plots for a interactive dashboard to better understand how the model behaves. Which downprojection methods can i use to understand the dataset and how the model behaves?


## 2. AI Response

1. The AI suggested to apply downprojection methods like PCA, UMAP or t-SNE on the image space. 
2. The AI suggested to apply downprojeciton methods on the embedding space of the model.
3. Warns that UMAP and t-SNE only preserve local neighborhood and not global distances. 
4. For a complex analysis it suggested ROC-AUC and precision-recall metrics.

[Setup AI Response](./00_r0_create_basic_dashboard_output.md)

## 3. What we did

**Decision:** Partly applied

We applied the suggestion for PCA, UMAP and t-SNE but **rejected** the idea of downprojecting on the models embeddings space as this is a more suitable task for phase 2. We developed plots for the downprojections methods based on the visualization functions the AI provided.

We also prepared plots for the confusion matrix in multiple iterations also with the help of AI. The confusion matrix plots revealed that only on one of the pathologies (Lung Opacity) the model was performing well, and since there are only 3 pathologies we could use with the Google NHI dataset we decided to focus only on the CheX dataset. We repeated the experiment with the CheX dataset.

