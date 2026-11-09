# AI Interaction 002 — First Research Question Analysis

**Can downprojection reveal systematic patterns in the model’s false-positive and false-negative predictions?**

# 1. Prompt

[Added image for the analysis](./02_r1_plot_subgroups_0.7_v4.png)

Can downprojection reveal systematic patterns in the model’s false-positive and false-negative predictions?

Pls analyse and interpret the result.

We used a threshold of 0.7. For downprojection we used S-UMAP.

# 2. AI Response

## Summary of the important text parts

A. Strongly separated error regions — especially Edema, Effusion, Pneumonia
These are the most interesting results.

For Edema and Effusion, S-UMAP produces two very distinct image regions. The classification plot then shows something striking:
- one region is dominated by false negatives (pink),
- the other region is dominated by false positives (orange),
- while relatively few correct predictions are visible compared with the two error types.
The same broad pattern appears for Pneumonia.

This suggests that the model is not simply making random mistakes. Rather, different regions of the image space correspond to different failure modes.

A good interpretation is:
The model appears to behave differently for different subpopulations of images within the same pathology. Some image regions are associated predominantly with missed positives, whereas other regions are associated predominantly with spurious positive predictions.


...


2. Atelectasis and Cardiomegaly show a similar pattern
For Atelectasis and Cardiomegaly, the ground-truth plots again show a relatively clear separation between the finding-present and finding-absent populations.

But the classification plots reveal that the large regions contain substantial mixtures of:
- false positives,
- false negatives,
- and some correct predictions.
So here the model failure is less cleanly localized.


...



3. Consolidation, Lung Lesion, Lung Opacity and Pneumothorax look more heterogeneous
For Consolidation, Lung Lesion, Lung Opacity, and Pneumothorax, FP and FN points are much more intermingled with each other.

This means that the projection does not give you a simple story such as:
"This region = false negatives; that region = false positives."

Instead, the model seems to encounter a continuous/heterogeneous range of cases, with errors distributed throughout the main manifold and around its boundaries.

That gives you another potentially useful hypothesis:
Some pathologies exhibit localized failure modes, whereas others exhibit diffuse errors throughout the image manifold.

[Complete AI Response](./02_r1_analysis_output.md)

# 3. What we did

## Any Patterns Visible in the Embeddings?

The AI identified a potentially interesting pattern in the embeddings. For some pathologies where the model appeared to perform relatively well, the 2D UMAP projections showed two visually distinct clusters. These pathologies were Atelectasis, Cardiomegaly, Edema, Lung Opacity, and Effusion.

For the other pathologies, the embeddings appeared more diffuse, with no similarly clear separation between clusters.

At first, this seemed like an interesting direction for further investigation as the AI suggested. However, we decided not to investigate the embedding clusters further for now. UMAP is a dimensionality-reduction technique that projects high-dimensional feature representations into a lower-dimensional space. Therefore, apparent distances, cluster sizes, and separations in the 2D projection cannot automatically be interpreted as meaningful relationships in the original feature space.

### Formulate new research questions

To get even further down how different meta data of the images are related to the false positive rate and false negative reate, we formulated the questions

**Are false positives disproportionately associated with particular patient or image characteristics, especially AP/PA view, age and sex?**
