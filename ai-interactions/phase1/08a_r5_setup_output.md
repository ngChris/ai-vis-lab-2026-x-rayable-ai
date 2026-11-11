Yes. For your current setup, I would make this a focused Phase I investigation of model confidence and false positives, rather than trying to reproduce every plot in the screenshot.

Your task/model setup is already well aligned with the assignment: Phase I treats the model as a black box and asks what drives its errors, while your chosen model is the CheXpert-trained TorchXRayVision DenseNet-121.    Task-and-Model
1. The experiment you want to answer
Your screenshot suggests this question:
Does the model know when it is wrong?

More precisely:
When the model makes a false-positive prediction, is its confidence usually just above the decision threshold (0.7), or does it sometimes make highly confident mistakes?

That is a much better Phase I question than simply reporting accuracy, because the assignment explicitly says that aggregate performance metrics aren't enough; you should investigate a systematic behavioral pattern in depth.    lab-assignment
2. Start from your existing notebook
You already have most of the infrastructure.

Your notebook currently:
- loads densenet121-res224-chex
- loads CheX_Dataset
- restricts the labels to those covered by the model
- obtains model scores
- uses 0.7 as the classification threshold
- stores age, sex and view metadata
- already distinguishes TP/TN/FP/FN
- already has interactive projection visualizations.
So don't rebuild the pipeline.

The important variables you already have are:
XRAY_DATASETXRAY_LABELS_LISTMODEL_SCORE_PREDICTIONS_CONVERTEDDATASET_PATHOLOGIESDATASET_AGESDATASET_GENDER_LISTXRAY_VIEW_LIST


and the prediction rule is already:
y_pred = (y_scores >= 0.7).astype(int)


3. First experiment: confidence distribution of errors
For each pathology, calculate the four prediction categories:
                    Ground truth

                 negative       positive

prediction
negative            TN             FN

positive            FP             TP

Then look at the model score distributions for those four groups.

For example, suppose we investigate Pneumonia.
import numpy as npimport pandas as pdimport matplotlib.pyplot as pltpathology = "Pneumonia"label_idx = DATASET_LABEL_INDICES_MAP[pathology]y_true = XRAY_LABELS_LIST[:, label_idx]y_score = MODEL_SCORE_PREDICTIONS_CONVERTED[:, label_idx]threshold = 0.7y_pred = (y_score >= threshold).astype(int)tp = (y_true == 1) & (y_pred == 1)tn = (y_true == 0) & (y_pred == 0)fp = (y_true == 0) & (y_pred == 1)fn = (y_true == 1) & (y_pred == 0)print("TP:", tp.sum())print("TN:", tn.sum())print("FP:", fp.sum())print("FN:", fn.sum())


Then:
plt.figure(figsize=(10, 6))plt.hist(y_score[tp], bins=30, alpha=0.5, label="True Positive")plt.hist(y_score[tn], bins=30, alpha=0.5, label="True Negative")plt.hist(y_score[fp], bins=30, alpha=0.7, label="False Positive")plt.hist(y_score[fn], bins=30, alpha=0.7, label="False Negative")plt.axvline(    threshold,    linestyle="--",    label="Threshold = 0.7")plt.xlabel("Model confidence / score")plt.ylabel("Number of images")plt.title(f"{pathology}: Prediction confidence by outcome")plt.legend()plt.show()


This is the first key visualization.
4. Then answer the actual question quantitatively
The histogram is useful, but you want a number behind the observation.

For false positives, calculate:
fp_scores = y_score[fp]print("Number of false positives:", len(fp_scores))print("Minimum FP score:", fp_scores.min())print("Median FP score:", np.median(fp_scores))print("Mean FP score:", fp_scores.mean())print("Maximum FP score:", fp_scores.max())


Then divide the false positives into meaningful confidence ranges:
bins = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]fp_hist, _ = np.histogram(fp_scores, bins=bins)fp_table = pd.DataFrame({    "confidence_range": [        "0.70–0.75",        "0.75–0.80",        "0.80–0.85",        "0.85–0.90",        "0.90–0.95",        "0.95–1.00"    ],    "false_positives": fp_hist})fp_table["percentage"] = (    fp_table["false_positives"] / len(fp_scores) * 100)fp_table


Now you can make a statement such as:
"X% of false positives have scores between 0.70 and 0.80, while Y% have scores above 0.90."

That is much stronger than saying "there seem to be some high-confidence false positives."
5. The particularly interesting measurement
I'd add this:
high_confidence_fp = fp_scores >= 0.9print(    "High-confidence FP:",    high_confidence_fp.sum())print(    "Percentage of FP with score >= 0.9:",    100 * high_confidence_fp.mean())


And perhaps:
very_high_confidence_fp = fp_scores >= 0.95print(    "Very-high-confidence FP:",    very_high_confidence_fp.sum())print(    "Percentage of FP with score >= 0.95:",    100 * very_high_confidence_fp.mean())


This gives you a very clean behavioral question:
How often is the model confidently wrong?

6. Don't investigate only one pathology
This is important for the assignment.

You don't want to discover:
"Pneumonia has some high-confidence false positives."

and stop.

Instead, run the same analysis across all model-supported pathologies.

Something like:
results = []for pathology in DATASET_PATHOLOGIES:    label_idx = DATASET_LABEL_INDICES_MAP[pathology]    y_true = XRAY_LABELS_LIST[:, label_idx]    y_score = MODEL_SCORE_PREDICTIONS_CONVERTED[:, label_idx]    y_pred = (y_score >= 0.7).astype(int)    fp = (y_true == 0) & (y_pred == 1)    fp_scores = y_score[fp]    if len(fp_scores) == 0:        continue    results.append({        "pathology": pathology,        "n_false_positives": len(fp_scores),        "mean_fp_score": fp_scores.mean(),        "median_fp_score": np.median(fp_scores),        "max_fp_score": fp_scores.max(),        "fp_ge_0.9": np.mean(fp_scores >= 0.9),        "fp_ge_0.95": np.mean(fp_scores >= 0.95)    })fp_results = pd.DataFrame(results)fp_results.sort_values(    "fp_ge_0.9",    ascending=False)


Now you can see whether the phenomenon is:
- specific to one pathology,
- common across pathologies,
- or particularly severe for certain findings.
That is much more interesting scientifically.
7. Then comes the really good part: Where are the false positives?
This is where your existing notebook becomes useful.

Your lecture explicitly presents dimensionality reduction as a way to reveal hidden structure in high-dimensional data, while warning that projections can also produce misleading patterns.     2026 AI  VIS Lecture 03 Explain…

You already have:
downprojector = Downprojector(    XRAY_IMAGE_FEATURES.reshape(-1, 224 * 224))


and your notebook already has a visualization separating:
- TP
- TN
- FP
- FN.
So for your chosen pathology, run:
create_viewer(    downprojector,    visualize_classification_outcome)


Select:
Projection: UMAP
Pathology: [your pathology]
Threshold: 0.7

I'd actually compare PCA, UMAP and t-SNE, because your lecture specifically covers these three techniques and emphasizes that their strengths and weaknesses differ.     2026 AI  VIS Lecture 03 Explain…     2026 AI  VIS Lecture 03 Explain…     2026 AI  VIS Lecture 03 Explain…
8. The hypothesis becomes much more interesting
You can now formulate:
H1
False positives are concentrated near the decision boundary.

versus
H2
False positives form distinct regions of the input space and some receive very high confidence.

If H2 happens, that is a strong Phase I finding.

You could then ask:
What distinguishes those false-positive regions from the correctly classified negative cases?

This is exactly the kind of follow-up the assignment asks for: don't stop at identifying a cluster of errors; investigate what distinguishes it and whether there are subgroups with different behavior.    lab-assignment
9. Add age, sex and view
This is where your existing metadata becomes valuable.

For every FP you already have:
age
sex
AP/PA
model score

Your notebook already puts these into the Plotly hover information.

I'd create an FP dataframe:
fp_df = pd.DataFrame({    "score": y_score[fp],    "age": np.asarray(XRAY_AGE_LIST)[fp],    "sex": np.asarray(XRAY_GENDER_LIST)[fp],    "view": np.asarray(XRAY_VIEW_LIST)[fp]})fp_df.head()


Then ask:
Does confidence differ by view?
fp_df.groupby("view")["score"].agg(    ["count", "mean", "median", "max"])


Does it differ by sex?
fp_df.groupby("sex")["score"].agg(    ["count", "mean", "median", "max"])


Does it differ by age?
For example:
fp_df["age_group"] = pd.cut(    fp_df["age"],    bins=[0, 30, 50, 70, 90, 120],    labels=["<30", "30–50", "50–70", "70–90", "90+"])fp_df.groupby("age_group", observed=True)["score"].agg(    ["count", "mean", "median", "max"])


This gives you a much richer question:
Are high-confidence false positives associated with particular patient/image characteristics?

And your original task explicitly says that Phase I should relate errors/confidence to attributes such as age, sex and view.    Task-and-Model
10. One visualization I'd make for the final presentation
I'd make a figure like this:
                MODEL CONFIDENCE OF FALSE POSITIVES

Number
  │
  │       █
  │       █
  │   █   █
  │   █   █       █
  │   █   █   █   █
  │ █ █   █   █   █       █
  └──────────────────────────────────
    .70 .75 .80 .85 .90 .95 1.00
                         ↑
                  high-confidence FP

But make it interactive and allow:
- pathology selection
- threshold selection
- age/sex/view filtering
- hover over individual points.
That would fit very well with the course's emphasis on interactive visualizations as investigative tools, rather than just static charts.    90 AI and Visualization - Zoom …
11. Then investigate the high-confidence FPs
Suppose you discover:
Pneumonia
-------------------------
FPs                    412
median FP score       0.76
FP >= 0.90             87
FP >= 0.95             31

Don't immediately conclude that the model is bad.

Instead, investigate those 87 images.

For example:
high_fp_indices = np.where(    fp & (y_score >= 0.90))[0]print(high_fp_indices[:20])


Then inspect those images.

You can create a contact sheet of, say, the top 25 highest-confidence false positives.

That lets you ask:
Are these genuinely strange images?

Are there particular acquisition characteristics?

Are they concentrated in AP images?

Do they look visually similar?

Are there multiple subgroups?

That is where the experiment turns from "we plotted some errors" into "we discovered a model behavior."
12. An even stronger experiment: confidence vs. correctness
I'd also make this visualization:
correct = (    ((y_true == 1) & (y_pred == 1)) |    ((y_true == 0) & (y_pred == 0)))incorrect = ~correctplt.figure(figsize=(10, 6))plt.hist(    y_score[correct],    bins=30,    alpha=0.5,    label="Correct")plt.hist(    y_score[incorrect],    bins=30,    alpha=0.7,    label="Incorrect")plt.axvline(    0.7,    linestyle="--",    label="Threshold")plt.xlabel("Model score")plt.ylabel("Number of images")plt.title(f"{pathology}: Does confidence predict correctness?")plt.legend()plt.show()


But there's one important conceptual issue:

For binary classification, a score of 0.95 for a negative case means the model is extremely confident in the positive class.

So for measuring confidence in the predicted class, you should actually calculate:
prediction_confidence = np.where(    y_pred == 1,    y_score,    1 - y_score)


Then:
incorrect_confidence = prediction_confidence[~correct]print(    "Median confidence on incorrect predictions:",    np.median(incorrect_confidence))print(    "Incorrect predictions with confidence >= 0.9:",    np.mean(incorrect_confidence >= 0.9))


This is the cleaner definition for your "Does the model know when it is wrong?" question.
13. I would structure your Phase I investigation like this
Question 1 — Does confidence correspond to correctness?
Visualization: confidence distributions for correct vs incorrect predictions.

↓
Question 2 — Are false positives merely borderline?
Visualization: FP confidence distribution with bins:

0.70–0.75 ... 0.95–1.00

↓
Question 3 — Are high-confidence FPs systematic?
Visualization: percentage of high-confidence FPs by pathology.

↓
Question 4 — Where do these errors occur?
Visualization: PCA / UMAP / t-SNE colored by:
TP / TN / FP / FN

↓
Question 5 — What characterizes the problematic regions?
Visualization: FP confidence vs:
age
sex
AP/PA

↓
Question 6 — Can we identify a specific subgroup?
For example:
"High-confidence FPs are disproportionately AP images."

or:
"The high-confidence FP cluster consists mainly of older patients."

or:
"High-confidence FPs occupy a distinct region of the image projection."

That final question is where your actual finding should emerge.
One important correction to your current experiment
Your notebook currently limits the dataset to:
MAX_NUMBER_OF_DATA = 10000


and then takes:
idxs=np.arange(0, n)


So you're taking the first 10,000 images, not a random sample.

For an investigation where you're going to claim that a behavior is systematic, I'd change that to a reproducible random sample:
rng = np.random.default_rng(42)n = min(MAX_NUMBER_OF_DATA, len(XRAY_DATASET))selected_indices = rng.choice(    len(XRAY_DATASET),    size=n,    replace=False)XRAY_DATASET = xrv.datasets.SubsetDataset(    XRAY_DATASET,    idxs=selected_indices)


Or, if the full dataset is computationally manageable, use the full dataset.

This matters because the assignment explicitly says the dataset should be large enough for patterns to be systematic rather than cherry-picked.    lab-assignment
What I would do next
Given your current notebook, I would not start coding everything from scratch.

The next practical step is:

1. Pick one pathology → 2. run the confidence/error analysis → 3. identify whether high-confidence FPs exist → 4. investigate those FPs with UMAP + age/sex/view → 5. only then expand to the other pathologies.

That gives you a hypothesis-driven investigation rather than a collection of unrelated plots.

Also, because you're the AI-aided pair, your process itself needs to be recorded: the assignment asks you to keep important prompts, how AI suggestions affected decisions, and which suggestions were accepted/modified/rejected.    lab-assignment Your lab notes also make clear that AI should be used collaboratively for exploration rather than simply generating the entire visualization in one shot.    90 AI and Visualization - Zoom …

If you want, I can take your existing xraymodel.ipynb and lay out the exact cells to add for this experiment, including the final 3–4 publication-quality plots and the tables you'll need for the Phase I midpoint.