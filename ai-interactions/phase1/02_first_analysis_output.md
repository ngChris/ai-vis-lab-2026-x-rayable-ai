# Analysis and interpretation of the pathology plots (threshold = 0.7)

The plots reveal several interesting patterns that are worth investigating in Phase I. In particular, I would focus on pathology-specific classification behaviour, differences between positive and negative cases, confidence calibration, and potential age-related effects.

The most interesting aspect is that the model does not appear to behave uniformly across pathologies. Some pathologies form clearly separated clusters in the embedding, while others show more diffuse distributions. This suggests that the model may find certain findings easier to distinguish than others.

There are also some promising research directions involving the relationship between model confidence and classification errors.

One important qualification: these are exploratory visual observations, not yet statistically confirmed findings. The embedding is a 2D projection, so distances and cluster sizes should not automatically be interpreted as meaningful distances in the original feature space.

## 1. Overall patterns across the pathologies

The visualization has three complementary views:

| Column                          | What it tells us                                                                  |
| ------------------------------- | --------------------------------------------------------------------------------- |
| Left: Model Confidence          | Where images are positioned in the UMAP embedding and how confident the model is. |
| Middle: Classification Outcomes | Where true positives, true negatives, false positives and false negatives occur.  |
| Right: Age vs. Model Confidence | Whether confidence changes with patient age.                                      |

The middle column is particularly important because it allows us to connect the model's errors to regions of the embedding.

### A. The model appears to distinguish some pathologies much better than others

[Atelectasis | Treatment & Management | Point of Care - StatPearls](https://images.openai.com/static-rsc-4/3VmQyu1o2_11wbAIwnlfWRmV1Vp65dBjYhDU83pn7jnAWV9WxMcUXq8gEBrLK924KuAKqMj6E6ZYnlX1fjjkQ_zqAhCNuVPRLQABwRwFG8TnOG3RYo67f4ZTaU9W2cS9kxr9IIxO_c9ue9MYebKNe8VR_WVxKZMg8p3zcxThDvo?purpose=inline)

Atelectasis

Two relatively distinct clusters are visible. The smaller left cluster contains predominantly false negatives and true positives, while the larger right cluster contains false positives and true negatives.

This is interesting because the embedding seems to separate images with different reference-label status, even though classification errors remain within both groups.

[Kardiomegalie | pacs](https://images.openai.com/static-rsc-4/4XmSPRKNFLEH81GugHfN6e0m-4AZBiTUyLELfEsRyO6dgQ2B1OX0erMcVIn3NJOtd0Qm28jIOLiMkAZ4Ku33l7Bni8j1jAsoM7Bb4Q7vu46lJSzBh-OTl7YRNMLKbY18vUxUuRtwV_9ZyseW5E0DOrjPLK9Sh2x1D10i88DG-tc?purpose=inline)

Cardiomegaly

There is a similarly strong separation between two major clusters. The classification outcomes suggest that false positives are concentrated in the larger cluster, while false negatives are visible in the smaller cluster.

Worth investigating: whether the false positives share particular image characteristics or whether the model systematically mistakes certain anatomical configurations for cardiomegaly.

[File:AP portable CXR of a patient in acute pulmonary oedema.jpg - Wikimedia Commons](https://images.openai.com/static-rsc-4/GLqfx0ptl0DdJQeHnPNObhHR9PYXtYES__yLxQChypw_9TxhxfqOSNObtQxCpQrRVfzWJILGu2X4MWQJRSb_SJ0ee7zx599BLcErOdiqspaFmJXi_GP66JhLEJwj3SIn3JJ3o5WaYYqHuFpD95_fhaAai50ST49R0IMEpqD3LnE?purpose=inline)

Edema

Again, two distinct clusters are visible. The error distribution appears similar to cardiomegaly and atelectasis.

This raises the question of whether the model has learned meaningful visual characteristics of these findings or whether the clusters reflect other shared image properties.

[Respiratory-Pleural effusion Flashcards | Quizlet](https://images.openai.com/static-rsc-4/BZuaeZCYBIbzOw4bckdyqmi3h7FBoQkfjjQCvUpdZwD6uNasnewK5IkQT1YIONl9Q_VupvTMq5qtn4E_E4VMRf4KOAb7YpUuEwOV4kyJCmnU1wxBwDEIQSewokHr8e7RxJVOKaL6LmU1DSeBeiJliND8rb5DjiRPtWxKmEtDdb4?purpose=inline)

Effusion

The two-cluster structure is particularly apparent. The smaller cluster contains predominantly false negatives and true positives, while the larger cluster contains predominantly false positives and true negatives.

This is a promising candidate for investigating why certain positive cases are systematically missed.

An important observation: These four pathologies exhibit a recurring pattern. The clusters appear to contain different ground-truth label groups, but the model still makes errors within them.

This suggests a potentially interesting distinction between:

- Images that are visually distinguishable in the embedding.
- Images that the classifier can correctly classify.

The two are not necessarily the same thing.

### B. Pathologies with more diffuse embedding structures

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

These differences are interesting because they suggest that a single classification task can exhibit very different embedding structures depending on the pathology.

However, a diffuse UMAP does not necessarily mean that a pathology is harder to classify. Likewise, clearly separated clusters do not prove that the model has learned the pathology itself.

The next step should be to investigate what actually distinguishes these clusters.

## 2. False positives and false negatives: the most interesting finding

The middle column is arguably the most valuable part of the visualization.

The legend distinguishes:

- Green: True positive
- Blue: True negative
- Orange: False positive
- Pink: False negative

At a threshold of 0.7, these outcomes let us investigate two fundamentally different error types.

False positives: The model predicts a finding when the reference label says it is absent.

False negatives: The model fails to predict a finding when the reference label says it is present.

### A recurring spatial pattern

For several pathologies, the false positives and false negatives appear to occupy different major embedding regions.

For example:

- False negatives are particularly visible in smaller clusters for atelectasis, cardiomegaly, edema and effusion.
- False positives are particularly visible in the larger clusters for these same pathologies.
- Some pathologies, such as pneumonia and lung lesion, exhibit more mixed and continuous distributions.

This raises an important research question:

Are false positives and false negatives caused by different underlying image characteristics?

For example, false positives might be associated with:

- Particular anatomical structures.
- Image acquisition differences.
- Other pathological findings that resemble the target finding.
- Certain image quality characteristics.

False negatives might be associated with:

- Subtle or less pronounced findings.
- Small affected regions.
- Different presentations of the same pathology.
- Low image contrast.

These are hypotheses, not conclusions from the current plots.

### A particularly interesting direction: error subgroups

I would not investigate all false positives or all false negatives as homogeneous groups.

Instead, I would look for subgroups within each error category.

For example, false negatives for cardiomegaly might consist of:

1. Images where the heart appears only slightly enlarged.
2. Images with unusual projection or positioning.
3. Images with poor image quality.
4. Images where another finding dominates the image.

If these subgroups exist, they could explain why the model fails on some examples but succeeds on others.

This would be a much stronger Phase I finding than simply reporting a false-negative rate.

## 3. Age versus model confidence

The right column contains a scatterplot for each pathology.

- X-axis: Patient age.
- Y-axis: Model confidence.
- Each point represents an individual image.

There are some interesting initial observations.

### A. No obvious strong age dependency

Across most pathologies, confidence is distributed over a relatively broad range across the entire age spectrum.

There is no immediately obvious pattern where confidence consistently increases or decreases with age.

This is worth investigating because age could influence image characteristics and the prevalence or appearance of particular findings.

However, the plots do not establish that age has no effect.

### B. Possible increase in confidence with age

Some plots appear to show a slight increase in the upper and central confidence distribution with increasing age.

This is particularly worth checking for:

- Cardiomegaly
- Edema
- Enlarged cardiomediastinum
- Fracture

One possible explanation is that the model is more confident on certain image characteristics that occur more frequently in older patients.

But another explanation is simply that the prevalence of the finding changes with age.

These two explanations need to be distinguished.

### C. Confidence is not necessarily correctness

This is especially important at the 0.7 threshold.

A model can be highly confident and still be wrong.

For example:

- A false positive with confidence 0.95 is a highly confident error.
- A false negative with confidence 0.65 is a relatively uncertain missed finding.
- A false negative with confidence 0.05 is a highly confident incorrect prediction.

The current age plots do not distinguish these cases.

I would therefore add a horizontal reference line at 0.7 and encode the classification outcome with colour.

That would immediately reveal whether certain age groups contain more high-confidence errors.

## 4. Gender and potential demographic effects

The left column includes markers for:

- Finding present – male
- Finding present – female
- Finding absent – male
- Finding absent – female

This is useful because it allows us to investigate whether male and female patients occupy different regions of the embedding.

From the overview, I cannot confidently identify a consistent gender-specific separation across the pathologies.

However, this is a worthwhile investigation.

I would specifically investigate:

1. Are false-positive rates different between male and female patients?
2. Are false-negative rates different between male and female patients?
3. Does model confidence differ between genders when controlling for the actual finding?
4. Are demographic differences concentrated in particular embedding clusters?

One important consideration: a difference in error rates does not automatically imply model bias. Differences in disease prevalence, age distributions, image acquisition and sample sizes could also contribute.

## 5. Patterns worth investigating further

I would prioritize the following research questions.

1\. Error clusters and their characteristics

Highest priority

Research question: Why does the model systematically misclassify certain regions of the embedding?

Investigate whether false positives and false negatives form identifiable subgroups.

Suggested analysis:

- Select the largest false-positive and false-negative clusters.
- Compare their age, sex and view distributions.
- Inspect representative X-ray images.
- Compare their confidence distributions.

Potential finding: Certain image subgroups systematically trigger specific classification errors.

2\. Age-related classification errors

High priority

Research question: Does the model become more or less reliable for particular age groups?

Instead of only examining confidence, calculate:

- False-positive rate by age group.
- False-negative rate by age group.
- Sensitivity and specificity by age group.
- Mean confidence for correct and incorrect predictions.

Possible age groups: 20–39, 40–59, 60–79 and 80+.

Potential finding: The model might have systematically different error rates for younger and older patients.

3\. High-confidence mistakes

Research question: Does the model make some mistakes with very high confidence?

Divide errors into confidence intervals:

| Confidence | Interpretation            |
| ---------- | ------------------------- |
| 0–0.3      | Low-confidence prediction |
| 0.3–0.5    | Moderate-low              |
| 0.5–0.7    | Near threshold            |
| 0.7–0.9    | Confident positive        |
| 0.9–1.0    | Very confident positive   |

For false negatives, also investigate the lower confidence intervals.

Potential finding: Certain pathologies may produce highly confident false positives, suggesting systematic confusion rather than random uncertainty.

4\. Pathology-specific differences

Research question: Why does the model produce different embedding structures for different pathologies?

Compare:

- Cluster composition.
- False-positive and false-negative proportions.
- Confidence distributions.
- Density and distribution of outliers.

Potential finding: Some pathologies may have more heterogeneous visual presentations, making them harder to classify consistently.

5\. Gender and image acquisition effects

Research question: Are classification errors associated with patient sex or imaging characteristics?

Investigate:

- Error rates by sex.
- Error rates by AP versus PA view.
- Confidence by image acquisition type.
- Interactions between age, sex and view.

Potential finding: Some apparent demographic differences may actually be explained by differences in imaging conditions.

## 6. An important additional investigation: threshold sensitivity

You have currently fixed the classification threshold at 0.7.

This is a useful starting point, but it introduces an important limitation: the classification outcomes depend on the chosen threshold.

Consider an image with a model score of 0.68:

- At a threshold of 0.7, it is classified as negative.
- At a threshold of 0.5, it is classified as positive.

This means that an image can switch from a false negative to a true positive simply by changing the threshold.

I would therefore repeat the classification analysis using:

Suggested threshold comparison

# 0.70

0.10

0.95

Current threshold

This control illustrates the threshold choice; it does not recalculate your underlying classification results.

I would compare 0.5, 0.6, 0.7, 0.8 and 0.9.

This could reveal whether the observed error clusters are stable or whether they change substantially depending on the decision threshold.

For example, if a particular subgroup contains many false negatives at 0.7 but becomes correctly classified at 0.5, the issue may be one of decision threshold or calibration rather than an inability to recognize the finding.

## 7. Important limitations of the current visualization

There are several things I would be careful about before drawing conclusions.

1\. UMAP does not preserve every relationship in the original data.

The lecture explicitly warns that distances between clusters, cluster sizes and apparent shapes can be misleading. UMAP is useful for revealing possible structures, but the projection itself is not proof of underlying relationships.&#x20;

2026 AI  VIS Lecture 03 Explaining Through Projections.pdf

2026 AI  VIS Lecture 03 Explaining Through Projections.pdf



2\. The age plots are heavily overplotted.

Thousands of points make it difficult to see differences in density. Consider using hexbin plots, density contours or age-binned confidence distributions.

3\. The current plots do not show error rates directly.

A cluster with many orange points might simply contain more observations overall. You need the proportion of false positives and false negatives within each group, not just their absolute numbers.

4\. Images from the same patient may not be independent.

If patients contribute multiple images, use patient-level grouping when splitting, sampling and estimating uncertainty.

5\. Confidence is not necessarily calibration.

A score of 0.9 should not automatically be interpreted as a 90% probability that the finding is present. Calibration needs to be evaluated separately.

These precautions are especially important because the assignment expects systematic behavioural findings, rather than conclusions based on a handful of examples.&#x20;

lab-assignment.txt



## 8. What I would do next: a concrete investigation plan

I would avoid immediately creating more plots for every possible attribute. Instead, I would use the existing visualizations to narrow down the investigation.

My recommended sequence:

1. Start with cardiomegaly, atelectasis and effusion.

   They show particularly interesting cluster structures and error distributions. Select one or two for deeper investigation.
2. Identify the false-positive and false-negative subgroups.

   Extract the corresponding image IDs and compare their metadata. Look for common characteristics.
3. Investigate age and sex.

   Calculate error rates separately for demographic groups, rather than relying on confidence scatterplots alone.
4. Investigate image acquisition.

   Compare AP and PA images, if that metadata is available. This is especially interesting because differences in projection can affect the appearance of anatomical structures.
5. Inspect representative images.

   Select examples from each error subgroup and compare them visually. Look for recurring image characteristics that could explain the errors.
6. Test threshold sensitivity.

   Repeat the analysis at several thresholds to determine whether the observed behaviour is robust.

## 9. My suggested main research narrative

I think there is a particularly promising story emerging from your current results:

## Does the model fail systematically on particular subgroups of chest X-rays?

The initial UMAP projections reveal different embedding structures across pathologies. For several findings, false positives and false negatives appear concentrated in different regions.

We want to understand whether these errors are associated with patient characteristics, image acquisition conditions or particular visual subgroups.

Central hypothesis:

The model's classification errors are not randomly distributed, but are associated with identifiable subgroups of images and patients.

I would formulate three main research questions:

1. Where does the model fail? Are there identifiable subgroups in the embedding that contain disproportionately many classification errors?
2. Who does the model fail on? Are errors associated with age, sex or other patient characteristics?
3. Under which imaging conditions does the model fail? Are errors associated with image view, acquisition conditions or visual characteristics?

This gives you a coherent investigative story rather than a collection of unrelated visualizations.

## 10. One visualization I would particularly recommend building

[Sleep and temperature data from wearable devices support noninvasive detection of diabetes mellitus in a large-scale, retrospective analysis | Communications Medicine](https://images.openai.com/static-rsc-4/SSrTfut-_8XJ3Eqr9bbQP765-o7ijj_B8hDpCGYzmx99Rlh5x_FcMUfGH1_lA7lWwieJ1B4Og8WSD1zrPHZeKF3MErTr4s1dMp17qHZ5gnegAy2LQW4425kWQ8daaQwh_gpv97jpBfrqMyUUdE8sJL2tQohlhgNMPOeniD3MtXQ?purpose=inline)

[nature.com](https://www.nature.com/articles/s43856-026-01501-0?utm_source=chatgpt.com)

I would create an interactive error exploration dashboard.

The central view would be your existing UMAP, but with additional functionality:

- Filter by pathology.
- Filter by classification outcome.
- Filter by age range.
- Filter by sex.
- Filter by AP/PA view.
- Adjust the classification threshold.
- Select individual points to inspect the corresponding X-ray and metadata.

Alongside it, include:

- A confusion matrix that updates with the filters.
- Confidence distributions for each error category.
- Age distributions for false positives and false negatives.
- Error rates for different image acquisition groups.

The most valuable interaction would be selecting a cluster of false negatives and immediately seeing the corresponding X-ray images and their metadata.

That would let you move from observing a pattern to understanding what characterizes the pattern.

## Final assessment

Promising Phase I results

I think your existing plots already provide a good starting point. The strongest opportunity is the recurring spatial separation of false positives and false negatives in several pathologies.

However, I would not yet claim that the model performs worse for older patients, that certain pathologies are inherently harder, or that demographic bias exists. Those require additional quantitative evidence.

My recommendation: Make the next investigation about the characteristics of false-positive and false-negative subgroups, starting with cardiomegaly and atelectasis. Then investigate whether age, sex and image view explain some of the observed differences.

This is a particularly good direction for your assignment because it directly addresses the requirement to go beyond identifying clusters and investigate what distinguishes them and why the model behaves differently within them.