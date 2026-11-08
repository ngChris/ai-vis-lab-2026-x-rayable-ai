# AI Interaction 002 — Find patterns and any other interresting things 

**Context**

# 1. Prompt

[Added image for the analysis](./02_plot_subgroups_0.7.png)

In the following are plots for each pathology, showing how the model scored, the actually classification outcomes and age vs confidence.  Threshold was 0.7.

Analyse and interpret the diagrams. Find any patterns that might be worth to investigate.

# 2. AI Response

## Summary of the important text parts

**A. The model appears to distinguish some pathologies much better than others**

**Atelectasis**

Two relatively distinct clusters are visible. The smaller left cluster contains predominantly false negatives and true positives, while the larger right cluster contains false positives and true negatives.

This is interesting because the embedding seems to separate images with different reference-label status, even though classification errors remain within both groups.

**Cardiomegaly**

There is a similarly strong separation between two major clusters. The classification outcomes suggest that false positives are concentrated in the larger cluster, while false negatives are visible in the smaller cluster.

Worth investigating: whether the false positives share particular image characteristics or whether the model systematically mistakes certain anatomical configurations for cardiomegaly.

**Edema**

Again, two distinct clusters are visible. The error distribution appears similar to cardiomegaly and atelectasis.

This raises the question of whether the model has learned meaningful visual characteristics of these findings or whether the clusters reflect other shared image properties.

**Effusion**

The two-cluster structure is particularly apparent. The smaller cluster contains predominantly false negatives and true positives, while the larger cluster contains predominantly false positives and true negatives.

This is a promising candidate for investigating why certain positive cases are systematically missed.

**B. Pathologies with more diffuse embedding structures**

Other pathologies exhibit a different pattern.

| Pathology                 | Visual observation                                 | Potential interpretation                                                           |
| ------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Consolidation             | One dominant cluster with scattered smaller groups | Less obvious separation between positive and negative cases.                       |
| Enlarged Cardiomedistinum | One dominant cluster with some peripheral points   | Potentially heterogeneous visual characteristics.                                  |
| Fracture                  | Dense central cluster and several outliers         | Possible variation in how fractures appear in the images.                          |
| Lung Lesion               | Broad, elongated cluster                           | Images may share general characteristics without forming clearly separated groups. |
| Pneumonia                 | Broad, dense, relatively continuous cluster        | Positive and negative examples may be difficult to distinguish visually.           |
| Pneumothorax              | Large cluster with peripheral groups               | Potential subgroups or atypical image characteristics.                             |
| Lung Opacity              | Two distinct clusters                              | Potential separation of different image or label groups.                           |


...


1. UMAP does not preserve every relationship in the original data.

The lecture explicitly warns that distances between clusters, cluster sizes and apparent shapes can be misleading. UMAP is useful for revealing possible structures, but the projection itself is not proof of underlying relationships. 2026 AI  VIS Lecture 03 Explaining Through Projections.pdf
 2026 AI  VIS Lecture 03 Explaining Through Projections.pdf


2. The age plots are heavily overplotted.

Thousands of points make it difficult to see differences in density. Consider using hexbin plots, density contours or age-binned confidence distributions.


...


10. One visualization I would particularly recommend building


[Complete AI Response](./02_first_analysis_output.md)

## 3. What we did

### Any Patterns Visible in the Embeddings?

The AI identified a potentially interesting pattern in the embeddings. For some pathologies where the model appeared to perform relatively well, the 2D UMAP projections showed two visually distinct clusters. These pathologies were **Atelectasis, Cardiomegaly, Edema, and Effusion**.

For the other pathologies, the embeddings appeared more diffuse, with no similarly clear separation between clusters.

At first, this seemed like an interesting direction for further investigation. However, we decided not to investigate the embedding clusters further for now. UMAP is a dimensionality-reduction technique that projects high-dimensional feature representations into a lower-dimensional space. Therefore, apparent distances, cluster sizes, and separations in the 2D projection cannot automatically be interpreted as meaningful relationships in the original feature space.

### Overplotting

The scatter plot showing age against model confidence suffered from substantial overplotting, making it difficult to identify meaningful patterns or differences between observations.

Following the AI's recommendation, we replaced the scatter plot with hexbin plots (2D histograms). 

### Interactive Error Exploration Dashboard

The AI also recommended developing a dedicated interactive dashboard for exploring the model's errors in more detail.

Based on this suggestion, we created an interactive visualization that combines three complementary views of model performance:

1. **Confusion matrix** – to examine the distribution of correct and incorrect predictions.
2. **ROC curve** – to investigate the model's discrimination performance across different classification thresholds.
3. **Precision–Recall curve** – to examine the trade-off between precision and recall, which is particularly useful for evaluating performance on individual pathologies.

### First research question

To get even further down how different meta data of the images are related to the false positive rate and false negative reate, we formulated the questions

**Are false positives disproportionately associated with particular patient or image characteristics, especially AP/PA view, age and sex?**
