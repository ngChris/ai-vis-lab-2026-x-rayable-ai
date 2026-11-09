Yes. The plots already give you a **strong Phase-I story**, but I would frame them as **hypotheses about what drives false positives**, not yet as causal explanations.

Your Phase-I question is exactly about relating model errors to patient/image attributes, and the assignment explicitly expects you to go beyond identifying a pattern and investigate what distinguishes the error groups. Task-and-Model lab-assignment

## 1. Main finding: AP/PA view is the strongest signal

The **view plot is probably your most interesting result**.

For many findings, the false-positive rate is much higher for **AP than PA**:

| Finding | AP | PA | Approx. difference |
|---|---:|---:|---:|
| Atelectasis | ~53% | ~26% | **+27 pp** |
| Cardiomegaly | ~34% | ~14% | **+20 pp** |
| Consolidation | ~24% | ~12% | **+12 pp** |
| Edema | ~37% | ~11% | **+26 pp** |
| Effusion | ~34% | ~12% | **+22 pp** |
| Enlarged cardiomediastinum | ~20% | ~11% | **+9 pp** |
| Lung opacity | ~41% | ~22% | **+19 pp** |
| Fracture | ~10% | ~10% | ~0 pp |
| Lung lesion | ~9% | ~15% | **PA higher** |
| Pneumonia | ~12% | ~13% | ~0 pp |

So this isn't simply "AP has a slightly higher FPR." **There is a systematic AP-associated increase for several findings**, particularly atelectasis, edema, effusion, cardiomegaly and lung opacity.

### Interpretation

This suggests that **image acquisition/view may be an important source of model error**.

However, you should **not yet conclude that AP itself causes the false positives**.

AP images can be associated with other characteristics of the acquisition/patient context. For example, AP images may differ from PA images in positioning, patient mobility, image quality, magnification, or other acquisition characteristics. Those factors could be the actual source of the model's difficulty.

So a stronger statement for your presentation would be:

> **False positives are strongly associated with AP view for several findings. This suggests that the model's errors may be sensitive to image acquisition and/or characteristics correlated with AP imaging. However, AP view may be acting as a proxy for other acquisition or patient factors, which requires further investigation.**

That is a much more defensible conclusion than "the model is biased against AP images."

---

# 2. Age is also a very strong pattern

The age plot shows an even more visually striking **age gradient**.

For many findings, FPR increases approximately monotonically with age:

**≤40 → 41–50 → 51–60 → 61–70 → 71–80 → >80**

For example:

### Atelectasis
Approximately:

- ≤40: **13%**
- 41–50: **24%**
- 51–60: **32%**
- 61–70: **41%**
- 71–80: **55%**
- >80: **69%**

That is a huge increase.

The same general pattern appears for:

- cardiomegaly
- consolidation
- edema
- effusion
- enlarged cardiomediastinum
- fracture
- lung lesion
- lung opacity
- pneumonia

The particularly strong ones appear to be **atelectasis and lung opacity**, with older groups reaching roughly 60–70%.

### Interpretation

This suggests that the model's false positives are **not uniformly distributed across age**.

But again, age itself may not be the causal factor.

Older patients may have different:

- image acquisition characteristics,
- prevalence of chronic anatomical changes,
- image quality,
- positioning,
- devices/tubes,
- comorbidities,
- combinations of findings.

So an important question becomes:

> **Is age independently associated with false positives, or is age acting as a proxy for the types of images that older patients tend to receive?**

This is actually a very good next research question.

---

# 3. Sex appears comparatively unimportant

The sex plot is almost the opposite story.

Female and male FPRs are generally very close.

For example:

- Atelectasis: ~39% vs ~36%
- Cardiomegaly: ~22% vs ~23%
- Consolidation: ~18% vs ~17%
- Edema: ~24% vs ~19%
- Effusion: ~22% vs ~21%
- Enlarged cardiomediastinum: ~14% vs ~15%
- Fracture: ~10% vs ~9%
- Lung lesion: ~12% vs ~13%
- Lung opacity: ~30% vs ~30%
- Pneumonia: ~13% vs ~12%

There are some differences, but they are substantially smaller than the age and AP/PA differences.

### Interpretation

At least from these plots:

> **Sex does not appear to be a major driver of false-positive behavior at the chosen threshold.**

That's still a valuable finding. You don't need every investigated attribute to reveal a strong effect.

You could actually emphasize the contrast:

> **The model's false positives appear much more strongly structured by age and image view than by sex.**

That makes your story more interesting.

---

# 4. There is an important finding-specific pattern

Another thing I would emphasize is that **the model does not behave the same way for every finding**.

For example:

- AP has a very large effect for **atelectasis**
- AP has a very large effect for **edema**
- AP has a very large effect for **effusion**
- AP has a very large effect for **cardiomegaly**
- But AP/PA makes almost no difference for **fracture**
- And for **lung lesion**, PA actually has a higher FPR than AP.

Similarly, age affects some findings much more strongly than others.

This suggests that you shouldn't search only for:

> "Is AP associated with errors?"

Instead ask:

> **"Which findings are particularly sensitive to AP, age, or their combination, and why?"**

That is a much richer model-behavior question and aligns well with the assignment's requirement to investigate patterns in depth rather than merely identify them. lab-assignment

---

# 5. The really interesting question: age × view

I think this should be your **next major investigation**.

Right now you have:

**Age → FPR**

and

**View → FPR**

But those variables may interact.

For example, perhaps:

> Older + AP → extremely high FPR

while

> Older + PA → only moderately high FPR.

Or perhaps AP increases FPR equally at every age.

Those are very different explanations.

### Make a heatmap

For each finding, create something like:

| | PA | AP |
|---|---:|---:|
| ≤40 | FPR | FPR |
| 41–50 | FPR | FPR |
| 51–60 | FPR | FPR |
| 61–70 | FPR | FPR |
| 71–80 | FPR | FPR |
| >80 | FPR | FPR |

This could immediately reveal whether the effects are:

- **additive** → age and view independently affect FPR
- **interactive** → AP particularly hurts certain age groups
- **confounded** → the apparent age effect largely disappears after separating AP and PA

I would consider this one of the highest-value next visualizations.

---


# 6. The biggest statistical issue: these are descriptive results

The plots show very convincing differences, but you should add a statistical analysis.

For each finding, you could model:

> **False positive ~ age + sex + view + interactions**

More formally, restrict the analysis to images that are actually negative for that finding and model whether the model incorrectly predicts it.

This lets you ask:

> Does AP remain associated with false positives **after accounting for age and sex?**

and:

> Does age remain associated with false positives **after accounting for view?**

This is much stronger than simply comparing bar heights.

### Especially important: patient-level dependence

Your dataset is **4,376 images from 1,695 patients**. Task-and-Model

Therefore, some patients contribute multiple images.

That means the individual images aren't necessarily independent observations.

You should therefore consider:

- patient-level bootstrap
- cluster-robust standard errors
- or another patient-level statistical treatment.

Otherwise, you may make the apparent sample size look larger than the number of independent patients really is.

---

# 7. Investigate the confidence scores, not only the thresholded errors

You currently use:

> **threshold = 0.7**

That is useful, but it hides information.

Imagine two groups:

- Group A: predictions mostly around **0.68**
- Group B: predictions mostly around **0.99**

Both can produce a false positive at threshold 0.7, but the model behavior is very different.

So I strongly recommend looking at the **prediction-score distributions** for:

- AP vs PA
- young vs old
- male vs female

especially for actual negatives.

For example:

**Distribution of model scores for actual negatives**

```text
             AP
        █████████████
      ███████████████
    █████████████████
---------------------- 0.7
              ████

             PA
       █████████
     ███████████
   █████████████
---------------------- 0.7
         ██
```

This could reveal whether AP images are:

1. shifted toward higher confidence,
2. producing more borderline cases,
3. producing a second high-confidence false-positive population.

That is much more informative about **model behavior** than FPR alone.

---

# 8. Vary the threshold

Another excellent question:

> **Does the demographic/view disparity persist across thresholds?**

Currently, everything is at 0.7.

Try:

**0.3, 0.5, 0.7, 0.9**

and plot FPR for AP/PA and age groups.

You might discover that:

- the disparity exists only around 0.7,
- the disparity becomes even larger at high confidence,
- or the disparity disappears at another threshold.

If AP has a consistently higher FPR across thresholds, that's considerably stronger evidence of a systematic difference.

---

# 9. Look at false-positive examples themselves

This is probably the most important qualitative follow-up.

Once you identify a group such as:

> **AP + false positive for cardiomegaly**

look at representative images.

Don't just choose a few visually interesting examples. Sample systematically.

Ask:

### What do the false positives have in common?

For example:

- Is there obvious heart enlargement?
- Is the heart magnified because of AP projection?
- Is there rotation?
- Is lung volume low?
- Are there tubes/lines?
- Is there an unusual positioning?
- Are there other abnormalities?
- Is the model detecting a visually plausible but incorrect finding?

You could compare:

**AP false positives vs AP true negatives**

and

**PA false positives vs PA true negatives**

This begins to explain *why* the model behaves differently.

---

# 10. A particularly interesting analysis: "false positive clusters"

Your lecture explicitly emphasizes using visualization to uncover hidden structure and then investigating what distinguishes error groups. 2026 AI  VIS Lecture 03 Explain…

You could therefore create an embedding/projection of the X-ray images and color points by:

- correct negative
- false positive

Then additionally encode:

- age
- AP/PA
- sex
- finding

The interesting question isn't simply:

> "Do false positives form a cluster?"

It is:

> **"Are the false-positive clusters primarily composed of AP images, older patients, or particular combinations of these?"**

And then:

> **"Are there sub-clusters with different false-positive behavior?"**

That would fit the course's Phase-I philosophy very well: finding a cluster is only the beginning; you should investigate what distinguishes it and whether it contains meaningful subgroups. lab-assignment

One caution: if you use t-SNE/UMAP, don't overinterpret cluster distances or apparent cluster sizes. The lecture specifically warns about the interpretability limitations of dimensionality reduction and the sensitivity of t-SNE/UMAP to parameters. 2026 AI  VIS Lecture 03 Explain… 2026 AI  VIS Lecture 03 Explain…

---

# 11. An important dataset/model question

There's one issue I would resolve before making strong conclusions.

Your task says the model is:

> **TorchXRayVision DenseNet-121, pretrained on CheXpert**

and that the NIH/Google dataset is intended as an external test set. Task-and-Model

You mentioned that you moved away from the NIH/Google dataset because performance was too poor.

That's reasonable for exploratory analysis, **but you need to be very explicit about what dataset you are now using**.

If you are evaluating the CheXpert-trained model on CheXpert data, make sure the images are from a genuinely held-out patient-level test set and that there is no train/test leakage.

Otherwise, the age/view patterns might describe the model **on a dataset very similar to its training distribution**, rather than general model behavior.

This is not necessarily bad—the question can still be interesting—but it changes the claim you can make.

---

# 12. I would formulate your current findings like this

For your presentation, I would currently summarize the results as:

> **False positives are not uniformly distributed across patient and image characteristics. The strongest differences are associated with image view and age, whereas sex shows comparatively little effect. AP images exhibit substantially higher false-positive rates than PA images for several findings, particularly atelectasis, edema, effusion, cardiomegaly and lung opacity. False-positive rates also generally increase with patient age, with particularly high rates among patients over 80.**
>
> **However, these associations do not establish that age or AP view independently causes the errors. AP view may be correlated with other acquisition and patient characteristics. The next step is therefore to investigate interactions between age and view, control for confounding factors, examine prediction-confidence distributions, and inspect representative false-positive images to determine what visual or acquisition characteristics distinguish them.**

That is a **strong Phase-I finding** because you're not stopping at "AP is higher."

---

# 13. My recommended next investigations, prioritized

If you have limited time, I would do them in this order:

### 🔴 Priority 1 — Age × AP/PA interaction
**Question:**  
> Is the age effect still present separately within AP and PA?

This is probably the single most informative next analysis.

### 🔴 Priority 2 — Statistical model
For each finding:

> **FPR ~ age + sex + view + age×view**

Determine which associations remain after controlling for the others.

### 🔴 Priority 3 — Prediction-score distributions
Instead of only FPR at 0.7:

> **How are the raw model confidence scores distributed among actual negatives?**

Do this for AP vs PA and young vs old.

### 🟠 Priority 4 — Acquisition/image-quality factors
Find out whether you have additional metadata describing how the image was acquired.

### 🟠 Priority 5 — Representative false positives
Inspect systematically sampled examples from the strongest groups:

- AP + false positive
- PA + false positive
- >80 + false positive
- ≤40 + false positive

Try to identify recurring visual characteristics.

### 🟡 Priority 6 — Threshold sensitivity
Repeat the analysis at several thresholds.

### 🟡 Priority 7 — Embedding/projection
Use the X-ray representations to ask whether false-positive cases occupy particular regions/subgroups.

---

## The deeper story I think you are uncovering

Your original question was:

> **Are false positives disproportionately associated with particular patient or image characteristics?**

Your plots suggest the answer is:

**Yes — particularly age and view.**

But the more interesting Phase-I question now becomes:

> **Why are AP images and older-patient images associated with higher false-positive rates, and are these effects independent or driven by correlated acquisition and image characteristics?**

That is a much stronger investigative question than the original one. It gives you a clear progression:

**Observation → association → control for confounding → identify subgroups → inspect images → formulate explanation.**

And that progression fits the assignment especially well: the instructors explicitly say that simply identifying a pattern isn't sufficient; you should investigate what distinguishes the error group and whether there are meaningful subgroups. lab-assignment

Finally, because you're the **GenAI-aided pair**, this is also a good place to document how AI influenced the investigation: e.g. whether the age×view hypothesis, confidence-distribution analysis, or acquisition investigation emerged from the collaboration, and which suggestions you accepted/rejected. The assignment specifically asks the AI pair to record how AI suggestions affected subsequent analytical decisions. lab-assignment