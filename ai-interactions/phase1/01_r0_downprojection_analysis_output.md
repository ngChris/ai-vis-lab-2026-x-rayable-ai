Yes. There are several patterns in these plots that are potentially very good Phase-I findings. The most interesting one is not simply that the model makes errors, but that the errors appear to be structured in the embedding space and that the model seems to produce a large number of positive predictions at the 0.5 threshold.

This fits the assignment particularly well: Phase I asks you to go beyond performance metrics and investigate systematic behavioral patterns and then ask what distinguishes the problematic groups.    lab-assignment
1. The strongest pattern: large false-positive regions
The middle column ("Classification outcomes") is probably the most interesting part of the figure.

Across many pathologies, there is a very large orange region, while the other outcome categories occupy much smaller regions.

From your legend, orange corresponds to False Positive.

This is particularly striking for:
- Atelectasis
- Cardiomegaly
- Edema
- Enlarged Cardiomediastinum
- Fracture
- Lung Opacity
- Lung Opacity / Pneumonia-related groups
- Pneumothorax
The effect is less visually overwhelming for some of the other findings, but the same general pattern occurs.
Interpretation
At threshold 0.5, the model appears to assign positive predictions to many images that are labelled negative.

That suggests:
The model may be systematically over-predicting pathology rather than making errors randomly.

This is much more interesting than saying "the model has many false positives."

The visualization suggests that these false positives are not uniformly distributed across the embedding space.

For example, in the Cardiomegaly plot, the large right-hand embedding region corresponds overwhelmingly to the same classification outcome, while a separate left-hand region has a very different mixture of outcomes.

That immediately gives you a stronger research question:
What distinguishes the embedding regions in which the model produces false positives from the regions in which it behaves correctly?

That is almost exactly the kind of follow-up the assignment asks for: a cluster with many errors is only the beginning; you should investigate what distinguishes it and whether it contains subgroups with different behavior.    lab-assignment
2. False positives seem to occupy coherent embedding regions
This is, in my opinion, your best potential finding.

Look at the first and second columns together.

For several pathologies, the UMAP contains clearly separated or elongated regions. The classification-outcome plot then shows that particular regions are dominated by a particular outcome.

For example:
Cardiomegaly
You have roughly:
- a smaller cluster around x ≈ 4–7
- a very large cluster around x ≈ 14–19
The classification plot shows that the large cluster is dominated by one outcome, while the smaller cluster has a much more heterogeneous mixture.
Edema
Again there are two very distinct regions:
- a small cluster on the left
- a large cluster on the right
And the right-hand cluster is visually dominated by the same classification outcome.
Lung Opacity
There is again a strong separation between two regions, with the classification outcomes differing substantially between them.
Atelectasis
The separation is also very apparent: a smaller lower-left group and a much larger upper-right group, with different score/outcome compositions.
Why this matters
This suggests that the model's errors may be related to image characteristics represented in the embedding, rather than being random.

In other words:
Some types of X-rays appear to be systematically difficult for the model.

That is a very strong Phase-I direction.

But there is an important caveat.

The lecture explicitly warns that dimensionality-reduction plots can create misleading apparent structure: cluster sizes and distances in t-SNE/UMAP should not automatically be interpreted as meaningful, and hyperparameters can substantially change the visualization.     2026 AI  VIS Lecture 03 Explain…     2026 AI  VIS Lecture 03 Explain…

So don't claim:
"There are two natural image classes."

Instead say something like:
"The projection reveals regions with markedly different error compositions. We therefore investigate whether these regions correspond to systematic differences in patient or acquisition characteristics."

That's much stronger scientifically.
3. Model confidence is strongly associated with embedding position
The left column is also interesting.

The colour represents model score, and you can see that the score is not uniformly distributed across the projection.

For several pathologies, particular embedding regions contain systematically higher or lower scores.

For example:
- Atelectasis: the lower-left cluster contains relatively high-score points, whereas much of the large upper-right cluster is lower/mid confidence.
- Cardiomegaly: the small left cluster tends toward higher scores, while the large right cluster contains more moderate/lower scores.
- Edema: similarly, the left cluster appears higher-scoring than much of the large right cluster.
- Lung Opacity: the left cluster is relatively high-scoring, while the other region has a different score distribution.
- Effusion and Pneumothorax also show substantial score variation across their embedding structures.
This is potentially important because it means:
The model's confidence is not independent of the type of image represented by the embedding.

You could investigate whether the embedding is capturing things such as:
- image view
- acquisition characteristics
- positioning
- presence/absence of other pathologies
- image quality
- age
- sex
- portable vs non-portable acquisition
- AP vs PA
- anatomical composition
The task definition explicitly gives you these patient/image attributes as possible explanatory variables.    Task-and-Model
4. Age seems to have a weak positive relationship with confidence
The right column is surprisingly interesting.

Across most pathologies, there appears to be a slight upward trend in model confidence with increasing age.

It is not a dramatic relationship. There is enormous vertical scatter at essentially every age.

But the upper envelope and density seem to shift somewhat upward as age increases.

I would therefore not write:
"The model becomes more confident with age."

That's too strong.

I'd write:
"There appears to be a weak positive association between patient age and model confidence across several findings, although the relationship is noisy."

This is worth testing quantitatively.
Especially interesting candidates
The apparent effect seems worth checking for:
- Cardiomegaly
- Edema
- Enlarged Cardiomediastinum
- Fracture
- Lung Lesion
- Lung Opacity
- Effusion
- Pneumonia
The effect may differ by pathology.
5. But age × confidence is not yet enough
This is an important limitation of the current visualization.

You're showing:

Age → model confidence

But your actual research question is about:

Age → model errors

Those aren't the same thing.

A model could become more confident with age while actually becoming more accurate, less accurate, or simply more likely to predict positive.

So the next visualization should be:
Age vs model score, split by outcome
For each pathology:
- True Positive
- True Negative
- False Positive
- False Negative
Then you could ask:
Does age affect confidence differently for correct and incorrect predictions?

That would be much more compelling.

For example, you might discover:
"Confidence increases with age primarily among false positives."

That would turn your current weak visual observation into a very strong finding.
6. The threshold of 0.5 itself deserves investigation
This is another major point.

You are currently looking at:
prediction ≥ 0.5 → positive

But the visualization appears to suggest that 0.5 may be producing a very large number of positive predictions.

That raises a very important question:
Is 0.5 an appropriate threshold for these pathologies?
For a multi-label medical model, the optimal operating point can differ substantially between findings.

Therefore, don't necessarily interpret the orange dominance as an intrinsic property of the model yet.

It could partly be:
model calibration + threshold choice

rather than simply poor feature learning.

I'd definitely investigate the same plots at something like:

0.2 / 0.3 / 0.4 / 0.5 / 0.6 / 0.7 / 0.8

and see whether the false-positive regions persist.

You don't necessarily need to show all seven in the final presentation. The investigation can determine whether 0.5 is driving the phenomenon.
7. Different pathologies have very different embedding structures
This is another pattern worth highlighting.

The shape of the embedding differs dramatically between findings.

For example:
Pathology	Visual structure
Atelectasis	Two major separated regions
Cardiomegaly	Two strongly separated regions
Consolidation	Dense elongated cluster + scattered points
Edema	Two very distinct groups
Enlarged Cardiomediastinum	Mainly one elongated cluster
Fracture	One dominant cluster with scattered outliers
Lung Lesion	Very elongated structure
Lung Opacity	Two clearly separated regions
Effusion	Two separated regions
Pneumonia	Large elongated central cluster
Pneumothorax	Large compact cluster + scattered outliers


This suggests that the representation of the images differs substantially depending on which pathology you're investigating.

However, be careful: these are separate UMAPs, so you cannot compare the numerical positions of clusters between pathologies. UMAP coordinates themselves don't have a shared semantic interpretation.

The useful comparison is the internal structure of each pathology, not "cluster x=15 in cardiomegaly is similar to x=15 in edema."
8. Outliers could be extremely interesting
There are many isolated points around the main clusters.

These are particularly visible for:
- Consolidation
- Enlarged Cardiomediastinum
- Fracture
- Lung Lesion
- Pneumonia
- Pneumothorax
Some of these isolated points appear to have very different classification outcomes from the surrounding dense region.

That's potentially a gold mine.

For example:
Why are some images embedded far away from the main population, and does the model behave differently on these outliers?

You could investigate whether they correspond to:
- unusual views
- unusual acquisition
- extreme ages
- poor image quality
- uncommon pathology combinations
- AP rather than PA
- images with multiple findings
- mislabeled cases
This would be much more interesting than simply reporting the outliers themselves.
9. A particularly promising hypothesis: acquisition/view effects
Given what you're already planning to investigate, I would put AP vs PA very high on the list.

The embedding structure could be capturing acquisition/view information rather than pathology itself.

For example, suppose the large false-positive cluster turns out to contain predominantly AP images.

Then you have a much stronger story:
The model's false positives are concentrated in a particular image-acquisition subgroup.

That is a genuine model-behaviour finding.

And it would fit the task specification very well because your Phase-I task explicitly proposes investigating age, sex, view (AP/PA), and image acquisition characteristics.    Task-and-Model
10. I would investigate these hypotheses in this order
If this were my project, I would not add many more random visualizations. I would follow the strongest patterns already visible.
Hypothesis 1 — False positives are concentrated in specific image subgroups
Question:
What differentiates the regions dominated by false positives?

Test against:
- AP vs PA
- age
- sex
- acquisition information
- image quality if available
This is probably your strongest direction.
Hypothesis 2 — The 0.5 threshold is responsible for much of the FP behaviour
Plot:

score distributions by outcome

for every pathology.

Something like:
                 Model score
       0        0.25       0.5       0.75       1
FP     ████████████████████████
TN     ███████████
TP                  █████████████████
FN          █████████

The actual distributions will tell you whether 0.5 is a sensible boundary.
Hypothesis 3 — Age affects errors, not merely confidence
For every pathology:

Age × score, coloured by:
- TP
- TN
- FP
- FN
Then ask:
Does the FP rate increase with age?

Does confidence increase with age primarily for false positives?

That could produce a very compelling result.
Hypothesis 4 — AP/PA explains embedding clusters
Colour the UMAP by:

AP vs PA

instead of model score.

If one of your existing clusters suddenly becomes almost entirely AP images, you've found a very strong explanation for the structure.

This would be one of the first things I would try.
Hypothesis 5 — Sex explains part of the error structure
Similarly:

UMAP coloured by sex + classification outcome

Then investigate:
Are FP/FN regions disproportionately male or female?

Don't stop at a difference in counts, because class prevalence may differ. Compare rates within groups.
11. One visualization I would strongly recommend
Instead of another 30-panel figure, make an interactive investigative view.

For one pathology at a time:

UMAP

with:
- colour = TP/TN/FP/FN
- tooltip = age, sex, AP/PA, score
- filters = age / sex / view
- optionally image thumbnail on hover/click
Then you can select the false-positive region and ask:
What are the characteristics of the images in this region?

This directly follows the course's idea of using visualization as an investigative tool rather than merely producing static charts. The assignment explicitly says the goal is to understand an observed error pattern in depth rather than merely identify it.    lab-assignment
12. My current interpretation
If I had to formulate the findings from this figure for your midpoint presentation, I would currently say:
At a threshold of 0.5, the model exhibits substantial false-positive behaviour across several pathologies. These errors are not uniformly distributed in the embedding space: distinct regions of the projection show markedly different classification-outcome compositions and confidence levels. This suggests that model errors may be associated with systematic characteristics of the input images rather than occurring randomly.

The age-confidence plots also suggest a weak positive association between age and model confidence for several pathologies, although the relationship is highly variable. This motivates investigating whether age is associated with errors specifically, rather than confidence alone.

The next investigation therefore focuses on explaining the error-dominated embedding regions using metadata such as age, sex and AP/PA view, as well as testing whether the observed false-positive behaviour is sensitive to the 0.5 decision threshold.

That is a much stronger Phase-I story than "the model has bad accuracy."
One important methodological warning
Because these are UMAP projections, don't make causal or strong geometric claims from the plots alone. Your lecture explicitly emphasizes that dimensionality reduction can hide information and that apparent cluster size/distance can be misleading.     2026 AI  VIS Lecture 03 Explain… The lecture also specifically warns that UMAP/t-SNE hyperparameters can influence the resulting structure.     2026 AI  VIS Lecture 03 Explain…

So the UMAP should generate hypotheses, and then your metadata/error-rate analyses should test them.

That's actually ideal for this assignment.
My ranking of the findings worth pursuing
★★★★★ False positives concentrated in particular embedding regions
★★★★★ Determine whether AP/PA explains those regions
★★★★☆ Determine whether 0.5 is producing the apparent FP dominance
★★★★☆ Age × error outcome rather than merely age × confidence
★★★☆☆ Sex differences in FP/FN rates
★★★☆☆ Investigate isolated/outlier images
★★☆☆☆ General differences in UMAP shapes between pathologies

The first two together could potentially become the central Phase-I finding of the project.

And importantly, your assignment specifically requires the pattern to be systematic rather than cherry-picked, and asks you to investigate what distinguishes an error-dominated cluster.    lab-assignment Your current figure is actually a good starting point for exactly that. 















pls create plots to run the experiment to answere the question












Worked for 2m 26s





Analysis paused



I would build this as a False-Positive Subgroup Investigation directly on top of your existing xraymodel.ipynb.

The experiment should answer:
Are false positives disproportionately associated with particular patient or image characteristics, especially AP/PA view, age, sex, and image acquisition?

Rather than just plotting the number of false positives, we'll measure the false-positive rate within each subgroup. This is important because, for example, a group with more AP images might naturally have more false positives simply because it contains more images.
The plots I recommend
Plot	What it investigates
1. FP rate by AP/PA view	Whether AP images have more false positives than PA images
2. FP rate by sex	Whether error rates differ between male and female patients
3. FP rate by age group	Whether older patients are more susceptible to false positives
4. AP/PA × sex heatmap	Whether combinations of patient and acquisition characteristics matter
5. UMAP coloured by subgroup	Whether false-positive embedding regions correspond to AP/PA, age or sex
6. Confidence distributions	Whether false positives have different confidence distributions across subgroups
7. Subgroup comparison across pathologies	Whether the same effects occur consistently across findings

I'll use your existing model predictions, labels and dataset metadata. You won't need to run model inference again.

Created
 Your experiment code is ready.
Extended Jupyter Notebook

Original notebook + new experiment section

Recommended

Download xraymodel_with_subgroup_experiment.ipynb

Standalone Python code

Experiment section only


Download false_positive_subgroup_experiment.py

How to run it
1. Open the extended notebook.
2. Run your existing cells in order, including model loading, dataset loading and prediction.
3. Run the new section at the bottom: Phase I experiment: false-positive subgroup investigation.
4. The plots will be generated interactively.
What to investigate first
I'd start with these three:
1
False-positive rate: AP vs PA

Does the model make systematically more false-positive predictions on AP images?2
False-positive rate: male vs female

Are there differences between patient subgroups?3
UMAP coloured by AP/PA

Do the false-positive regions correspond to particular image views?
Important methodological detail
I've included two safeguards:
- False-positive rate is calculated as FP / (FP + TN), rather than comparing raw false-positive counts.
- Uncertain labels (-1) and missing labels are excluded from binary error calculations.
The experiment uses your requested threshold of 0.5, independently of the thresholds used in some earlier notebook cells.

One limitation: I have prepared and syntax-checked the experiment code, but haven't run it against your actual CheX dataset because the chest_data directory isn't among the uploaded files. The actual plots will appear when you execute it in your existing dataset environment.

My recommendation: Start with the AP/PA comparison. If it reveals a substantial difference, we can investigate whether AP images explain the false-positive clusters in your original UMAP plots. That could become a very strong Phase-I finding.