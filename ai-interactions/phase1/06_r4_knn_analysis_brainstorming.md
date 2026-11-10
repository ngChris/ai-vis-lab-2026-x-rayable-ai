# AI Interaction — Ideas for NN

**Are the model's predictions locally consistent among visually similar X-ray images, and does this consistency differ between correctly and incorrectly classified samples?**

# 1. Prompt
I would like to focus on this recommendation: 

Fourth recommendation: Find the nearest-neighbor images in embedding space
This is another approach I would strongly recommend.

Instead of plotting every embedding as a point, select a particular X-ray and retrieve the images whose feature vectors are most similar to it.

You can use cosine similarity or Euclidean distance, depending on the representation and normalization.

For each query image, display:
The original image.
Its ground-truth labels.
Its predicted scores.
The nearest neighboring images.
The labels and scores of those neighbors.
Example
Suppose you select a pneumothorax-positive image.

The visualization retrieves the ten nearest images in the model's embedding space.

You can then ask:
How many neighbors are also pneumothorax-positive?
Do the images have similar visible characteristics?
Are the negative examples genuinely similar to the positive image?
Do the neighbors receive similar model scores?
Are the same patterns observed for false positives and false negatives?
If positive and negative examples frequently appear among one another's nearest neighbors, this would support the observation that the local representation does not cleanly separate the classes.

If the nearest neighbors share meaningful visual characteristics, you could investigate which characteristics are common to them.

However, similarity in the embedding does not necessarily mean similarity in disease status. The representation might emphasize anatomy, acquisition conditions, or other shared features. < In order to do so, I would look at an image that was missclassified and analyse its nearest neighbors. Is it advisable to use downprojections or can i use the full img?

# 2. AI Response
Yes, analyzing the nearest neighbors of misclassified chest X-rays is an excellent approach for understanding what your model has learned.

My recommendation is to use the full-dimensional embeddings from your model rather than dimensionality-reduced projections to identify the nearest neighbors.

There is an important distinction between three possible representations:
Representation	Recommended?	Reason
Original X-ray pixels	Generally no	Pixel similarity is strongly influenced by positioning, brightness, anatomy, etc.
Full-dimensional model embeddings	Yes — preferred	Preserves the feature representation learned by your model
2D/3D UMAP, t-SNE or PCA projections	For visualization	Dimensionality reduction can distort local distances and neighborhood relationships

**1. Why use full-dimensional embeddings?**
Suppose your model produces an embedding vector with 1,024 dimensions for each X-ray.

You can calculate the similarity between a misclassified image and every other image directly in this 1,024-dimensional space.

For cosine similarity:

$$
\operatorname{sim}(x_i, x_j)
= \frac{z_i^\top z_j}{\|z_i\| \|z_j\|}
$$

where $z_i$ and $z_j$ are the embeddings extracted from your model.

This avoids the information loss introduced by dimensionality reduction.

Important: An embedding from the layer immediately before the classification head is a good starting point, because it represents the features directly available to the classifier. You can later compare earlier layers to investigate whether the similarities change.

**2. How I would investigate a misclassification**
Imagine you have a pneumothorax classifier that produces the following prediction:
Ground truth

Pneumothorax: Positive

Model prediction
0.18
Example score (threshold = 0.50)

Question: Why did the model assign such a low score to a positive example?

Retrieve its 10 nearest neighbors and examine their ground-truth labels and predicted probabilities.

For example, if 8 of the 10 nearest neighbors are negative and receive similarly low scores, that could suggest the query's representation lies in a predominantly negative region of embedding space.

However, this alone does not establish why the model made the error.

**3. What I would measure**
For each misclassified image, I would examine:
- Neighbor label agreement: How many of the k nearest neighbors share the query's ground-truth label?
- Prediction agreement: How many neighbors receive the same predicted classification?
- Score distribution: Are predicted probabilities similar among neighboring images?
- Visual characteristics: Do the images share anatomical characteristics, acquisition properties, or visible pathologies?
- Distance: How close are the neighbors relative to other images?
You could also compare the nearest-neighbor characteristics of four groups:
Query type	What to investigate
True positive (TP)	Are neighboring images predominantly positive?
True negative (TN)	Are neighboring images predominantly negative?
False positive (FP)	Does the model place negative images near positive examples?
False negative (FN)	Does the model place positive images near negative examples?

This comparison is especially valuable because it allows you to investigate whether misclassifications are associated with mixed-label neighborhoods.

**4. A simple Python implementation**
Assuming you have extracted your embeddings into a NumPy array:

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# embeddings: (N, D)
# N images, D embedding dimensions

query_idx = 42

similarities = cosine_similarity(
    embeddings[query_idx:query_idx+1],
    embeddings
)[0]

# Exclude query image
similarities[query_idx] = -np.inf

k = 10
neighbor_indices = np.argsort(similarities)[-k:][::-1]
```
You can now retrieve the original X-ray images, labels, and prediction scores using neighbor_indices.

Make sure to use a suitable retrieval set, avoid retrieving duplicate images or different views of the same patient as independent evidence, and keep the query separate from the candidate pool where appropriate.

**5. Where dimensionality reduction is still useful**
I would use PCA or UMAP as a complementary visualization, not as the basis for neighbor retrieval.

For example:
1. Retrieve the 10 nearest neighbors using the original model embeddings.
2. Project the embeddings into 2D with UMAP.
3. Highlight the misclassified query and its actual nearest neighbors on the projection.
4. Display the original X-ray images beside the projection.
Be careful: a 2D projection does not guarantee that the actual nearest neighbors will appear visually closest to the query.

One additional consideration: Since your investigation concerns chest X-rays, I would also stratify the analysis by AP/PA projection where that metadata is available. Otherwise, you might find that the model's nearest neighbors primarily share acquisition characteristics rather than pneumothorax status.

My preferred experimental setup: Use full-dimensional penultimate-layer embeddings with cosine similarity, retrieve 10–20 neighbors per misclassified X-ray, and compare the results systematically against correctly classified images. This gives you both qualitative examples and quantitative evidence about the learned representation.

The key research question is not simply whether a misclassified X-ray has negative or positive neighbors, but whether incorrect predictions are associated with local embedding neighborhoods dominated by the opposite ground-truth class.

# 3. What we did
We used the suggestion to investigate missclassified images through nearest neighbor analysis.
We did not use the model's internal embeddings, as we thought this was not in the scope of Phase I but rather of Phase II.