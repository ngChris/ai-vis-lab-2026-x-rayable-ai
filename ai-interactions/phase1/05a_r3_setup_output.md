For your Phase I experiment, I recommend building a false-positive/false-negative subgroup analysis dashboard that investigates whether the TorchXRayVision DenseNet-121 makes systematically different errors depending on:
1. Image view: AP vs. PA
2. Patient age: younger vs. older patients, and continuous age
3. Patient sex: female vs. male
4. Interactions: for example, whether the age-related error pattern differs between AP and PA images.
The key is not simply to show which subgroup has the most errors. You want to determine whether the model is disproportionately likely to make an error for a particular subgroup, while accounting for differences in subgroup sizes and disease prevalence.

I would prioritize the following six visualizations.
1. False-positive and false-negative rates by subgroup
Highest priority








nature.com


Plot: Grouped bar chart.
- X-axis: AP vs. PA, or Female vs. Male.
- Y-axis: Error rate (%).
- Bars: False-positive rate (FPR) and false-negative rate (FNR).
- Separate panels: View, sex and age groups.
Calculate:
\[
FPR = \frac{FP}{FP+TN}
\]

\[
FNR = \frac{FN}{FN+TP}
\]

Why this is useful:
- Shows whether AP images have a higher FPR than PA images.
- Reveals whether the model misses more positive cases in one sex.
- Makes subgroup differences immediately visible.
Important: Do not plot raw FP and FN counts alone. A subgroup with more images will naturally tend to have more errors.
2. Age vs. error probability
Highest priority








hbiostat.org


Plot: Scatter plot with a smoothed trend line, or preferably a binned rate plot.
- X-axis: Patient age.
- Y-axis: FPR or FNR.
- Separate lines: AP and PA.
- Optional facets: Female and male.
I recommend calculating FPR and FNR in age bins, for example:
- 0–20
- 21–40
- 41–60
- 61–80
- 81+
This helps answer:
- Does the model produce more false negatives in older patients?
- Are false positives more frequent among younger patients?
- Does the relationship between age and model errors differ for AP and PA?
Keep age continuous for a complementary statistical analysis, rather than relying exclusively on arbitrary age groups.
3. Error-rate heatmap: Age × View × Sex
Highly recommended








techcommunity.microsoft.com


Plot: Heatmap.

Create two heatmaps:
- One for FPR.
- One for FNR.
Structure:
- X-axis: Age groups.
- Y-axis: AP/PA and sex combinations.
- Cell color: Error rate.
- Cell annotation: Error rate and number of images.
Example:
Group	0–20	21–40	41–60	61–80	81+
Female AP					
Female PA					
Male AP					
Male PA					

This is particularly useful for discovering interactions.

For example, perhaps AP images have more false negatives overall, but the difference is especially pronounced among older female patients.

That is a much more interesting finding than simply saying AP images have a higher error rate.
4. AP/PA × Sex interaction heatmap
Plot: Two-dimensional heatmap.

Your existing investigation notebook already includes a version of this visualization.

For each pathology:
- X-axis: Female / Male.
- Y-axis: AP / PA.
- Color: False-positive rate.
- Cell annotation: FP count / actual-negative count.
This lets you investigate whether the model behaves differently for, say, female AP images compared with male AP images.

I would create an equivalent heatmap for FNR as well.

One useful extension is to add age as a filter, so you can inspect the interaction for younger and older patients separately.
5. UMAP projection highlighting false positives and false negatives
Best exploratory visualization








link.springer.com


Plot: Interactive UMAP scatter plot.

You are already experimenting with PCA, t-SNE and UMAP in your main notebook, so this connects naturally to your existing work.

Each point represents one chest X-ray.
- X/Y: UMAP coordinates calculated from image features.
- Color: Classification outcome.
- Shape: AP vs. PA.
- Point size or another visual encoding: Patient age.
- Hover: Sex, age, view, pathology, prediction score and ground-truth label.
Use four outcome categories:
Outcome	Suggested color
True positive	Green
True negative	Blue
False positive	Red
False negative	Purple

Questions this visualization can answer:
- Are false positives concentrated in particular image regions?
- Do AP images dominate certain error clusters?
- Are older patients concentrated in error-prone regions?
- Are there subgroups of false positives with similar visual characteristics?
An important distinction: UMAP can reveal clusters and local patterns, but it cannot establish that AP, age or sex causes errors. The projection should be used to discover interesting subgroups, which you then investigate with the statistical plots.

Also, avoid interpreting distances between distant UMAP clusters too literally. The lecture explicitly warns about this limitation (Lecture 3, pages 20–26).
6. Prediction-score distributions for false-positive investigation
Plot: Overlaid histograms or violin plots.








lipidsig.bioinfomics.org


This is particularly interesting because it investigates not just whether an error happened, but how confident the model was when making that error.

For example, select one pathology and examine only images where the reference label is negative.
- X-axis: AP vs. PA, or Female vs. Male.
- Y-axis: Model prediction score.
- Show the threshold as a horizontal reference line.
- Separate distributions by subgroup.
For false-positive investigation, look for:
- A subgroup with many scores just above the threshold.
- A subgroup with consistently high false-positive confidence.
- Differences in the score distributions between AP and PA images.
You can repeat this for actual-positive images to investigate false negatives.

This is useful because two groups might have similar FPRs but very different confidence distributions.

7. My recommended additional analysis: Error-rate comparison with confidence intervals
This is less visually flashy, but essential if you want to make defensible conclusions.

Plot: Forest plot.








note.com


For each subgroup, calculate the difference in error rates relative to a reference group.

For example:
\[
\Delta FPR = FPR_{AP}-FPR_{PA}
\]

\[
\Delta FNR = FNR_{AP}-FNR_{PA}
\]

Display:
- One row per subgroup comparison.
- X-axis: Difference in error rate (percentage points).
- Horizontal lines: 95% confidence intervals.
- Vertical reference line at zero.
This makes it easy to identify which subgroup differences are substantial and which could simply be sampling variation.

Because your dataset contains multiple images per patient, I would ideally calculate confidence intervals using a patient-level bootstrap rather than treating every image as independent.

How I would organize the experiment
You already have much of the necessary infrastructure in your xraymodel.ipynb and r1_false_positive_subgroup_investigation.ipynb.

I would organize the experiment as follows:
Experiment workflow
1. Data preparation
   
   Join predictions, reference labels and metadata. Normalize age, sex and AP/PA view. Exclude missing and uncertain labels from binary error calculations.
2. Calculate classification outcomes
   
   For each pathology, classify every image as TP, TN, FP or FN using the selected threshold.
3. Subgroup analysis
   
   Calculate FPR and FNR by view, age and sex, including combinations of these attributes.
4. Visual investigation
   
   Create the subgroup charts, heatmaps, score distributions and UMAP projections.
5. Validate findings
   
   Investigate confidence intervals, sample sizes, patient-level dependence and differences between pathologies.

Important details specific to your implementation
I noticed several things in your existing notebooks worth addressing:
1. Your current subgroup investigation uses a prediction threshold of 0.7. Keep this consistent across comparisons, and document that the findings depend on this threshold.
2. Your existing code correctly excludes uncertain (-1) and missing labels from binary FP/FN calculations. Keep this behavior.
3. Your current subgroup plots focus mainly on FPR. Extend them to FNR as well.
4. You currently use a minimum subgroup size of 20. This is a reasonable initial display filter, but it does not guarantee statistically reliable results. Show the denominators and confidence intervals.
5. Since you have multiple pathologies, investigate them separately before making general claims about the model.
Also, distinguish image-level from patient-level analysis: a patient can contribute multiple X-rays, so repeated images should not be treated as fully independent observations.
My final prioritization
If I were doing this experiment, I would prioritize these five visualizations for the project presentation:
Priority	Visualization	Main purpose
1	FPR/FNR grouped bar charts	Identify problematic subgroups
2	Age vs. error-rate plot	Identify age-related patterns
3	Age × View × Sex heatmap	Discover subgroup interactions
4	UMAP error projection	Discover hidden error clusters
5	Prediction-score distributions	Understand model confidence in errors

The forest plot would be my additional statistical validation view.

One particularly interesting hypothesis to investigate: AP images might produce more false positives than PA images, but this difference might be concentrated in older patients rather than being consistent across all age groups.

That would give you a much richer finding than simply reporting that AP images have a higher error rate.

Finally, remember that the assignment explicitly asks you to investigate systematic model behavior rather than just report aggregate performance metrics (lab assignment, Phase I). These visualizations are designed to help you do exactly that. lab-assignment.txt


I would start by extending your existing subgroup investigation notebook to calculate and visualize both FPR and FNR, then use the UMAP projection to investigate whichever subgroup difference looks most interesting.