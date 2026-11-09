# AI Interaction 002 — First Research Question Analysis

# 1. Prompt

[Added image for the analysis](./02_r1_plot_subgroups_0.7_v4.png)

We asked the questions: Can downprojection reveal systematic patterns in the model’s false-positive and false-negative predictions?

Pls analyse and interpret the result.

We used a threshold of 0.7. For downprojection we used S-UMAP.

# 2. AI Response

## Summary of the important text parts


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

### Second research question

To get even further down how different meta data of the images are related to the false positive rate and false negative reate, we formulated the questions

**Are false positives disproportionately associated with particular patient or image characteristics, especially AP/PA view, age and sex?**
