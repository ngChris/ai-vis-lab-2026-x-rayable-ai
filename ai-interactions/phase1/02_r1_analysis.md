# AI Interaction 002 — First Research Question Analysis

**Can downprojection reveal systematic patterns in the model’s false-positive and false-negative predictions?**

# 1. Prompt

[Added image for the analysis](./02_r1_plot_subgroups_0.7_v4.png)

Can downprojection reveal systematic patterns in the model’s false-positive and false-negative predictions?

Pls analyse and interpret the result.

We used a threshold of 0.7. For downprojection we used S-UMAP.

# 2. AI Response

1. S-UMAP only claims where FP/FN occur withing the pathology-specific image manifold.
2. AI suggests that Downprojection reveals systematic spatial organization of model errors, and the organization differs substantially across pathologies.
3. AI revealed that gender does not visually explain the errors.
4. AI created the research question: Are FP and FN regions actually low-margin regions, or are they confidently wrong?
5. AI suggests as next step to quantify the **local** FP/FN rates.

[Complete AI Response](./02_r1_analysis_output.md)

# 3. What we did

## Any Patterns Visible in the Embeddings?

The AI identified a potentially interesting pattern in the embeddings. For some pathologies where the model appeared to perform relatively well, the 2D UMAP projections showed two visually distinct clusters. These pathologies were Atelectasis, Cardiomegaly, Edema, Lung Opacity, and Effusion.

For the other pathologies, the embeddings appeared more diffuse, with no similarly clear separation between clusters.

The AI repeatly warned about S-UMAP limited interpretability (which is of course correct) but somehow still guided us in using more UMAP techhniques for visualization. We continued with the AI to create plots to visualize the local FP/FN rates by using an k-nearest neighbors algorithm. 

We could htne observe: The model's false-positive behavior is pathology-dependent and, for several findings, spatially heterogeneous. This suggests that particular subpopulations of images may be associated with an increased likelihood of false-positive predictions.

The AI then suggested to compare Age/View/Gender characteristics, this is hower already done in research question 3.


