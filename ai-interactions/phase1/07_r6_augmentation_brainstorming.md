# AI Interaction — Ideas for image changes

**How sensitive does the model respond to certain data augmentations?**

# 1. Prompt
Since I lack the medical background, what would make sense for data augmentation for our torchray x model? I could, of course, alter brightness, add distortion, etc. But is there something specific with regards to x-rays that could drastically change interpretation from a medical point of view?

# 2. AI Response
Yes. And for your X-rayable AI project, I think this could be a particularly interesting experiment: rather than applying arbitrary image augmentations, investigate which medically meaningful image characteristics influence the model's predictions.

Since you're currently investigating pneumothorax detection, there are several transformations worth exploring. Some simulate realistic variations in X-ray acquisition, while others can actually obscure the evidence needed to diagnose pneumothorax.

The important distinction is:
- Label-preserving augmentation: Changes the image without changing the underlying medical condition.
- Diagnostic information degradation: Makes the condition more difficult or impossible to recognize, even though the patient still has it.
- Anatomically misleading transformation: Changes important structures or creates unrealistic radiological appearances.

### 1. What actually matters for pneumothorax?
Pneumothorax means air has accumulated between the lung and the chest wall.

On an upright chest X-ray, the important features include:
- A thin pleural line marking the edge of the collapsed lung.
- A darker region beyond that line, without normal lung vascular markings.
- Sometimes a relatively small abnormal area near the lung apex.
These findings can be subtle. In supine patients, the air can appear in different anatomical locations, so the signs depend on the patient's positioning. 
European Respiratory Society+2


This is exactly why some augmentations are more interesting than others.

### 2. Which augmentations would I investigate?
Here is how I'd prioritize them for your project.
Augmentation	Medical relevance	My recommendation
Brightness / exposure	Can change visibility of subtle lung findings	High priority
Contrast / gamma	Can obscure or emphasize pleural boundaries	High priority
Gaussian blur	Can remove fine pleural-line detail	High priority
Image resolution / downsampling	Can make small abnormalities difficult to detect	High priority
Small rotations	Simulate positioning variations	Useful
Translation / mild cropping	Can remove peripheral lung information	Useful, but risky
Horizontal flipping	Preserves many findings but changes laterality	Secondary experiment
Elastic distortion	Can create unrealistic anatomy	Avoid initially
Vertical flipping / large rotations	Anatomically implausible	Avoid

These choices are consistent with chest X-ray augmentation research, which has used exposure, blur, flip and affine transformations, while medical-imaging guidance emphasizes maintaining biologically plausible appearances. 
Frontiers+1

### 3. The three experiments I'd find most interesting

####  A. Contrast and gamma manipulation

Pneumothorax can be identified by the difference between the lung and the air outside it. Changing contrast or gamma may influence how clearly the pleural boundary is visible.

Research question: Does the model rely heavily on intensity differences rather than anatomical structures?

#### B. Blur and resolution reduction

Small pneumothoraces may be recognizable through very fine lines. Blurring or downsampling can suppress those features.

Research question: Does the model's confidence change significantly when fine details disappear?

#### C. Positioning and framing

Patient positioning matters considerably. A pneumothorax in a supine patient can have different radiographic signs from one in an upright patient. 
European Respiratory Society+1

However, you cannot realistically simulate a change from PA to AP or upright to supine simply by rotating an image. Such changes involve different projection geometry and sometimes actual redistribution of air.

One additional experiment could be particularly revealing: cropping near the lung apex or lateral chest wall. These are locations where important signs can appear. A small crop may remove the evidence entirely without changing the label assigned to the image. That's useful as a sensitivity test, but not necessarily a valid label-preserving augmentation.

### 4. How I'd integrate this into your existing analysis
You already have the original images, model predictions and TP/FP/FN/TN classifications. I'd build directly on those.

For example, suppose an originally correctly classified pneumothorax image receives these hypothetical scores:

Here the score drops below your 0.5 threshold after blurring. That observation would be worth investigating: it might indicate reliance on fine image details, although it would not prove that the model specifically uses the pleural line.

I'd measure:

$$
\Delta p = p_{\text{augmented}}-p_{\text{original}}
$$

Since your project is investigating model behavior rather than improving training performance, I would treat augmentation as a controlled perturbation experiment, not as a way to generate more training samples.

I'd begin with a small group of images from each classification category (TP, FP, FN and TN) and systematically vary one augmentation at a time.

You can then investigate two different effects:

1. Prediction stability: How much does the model's pneumothorax score change when the image is altered?
2. Neighborhood stability: Do the nearest neighbors of an augmented image change in raw-pixel, PCA or UMAP feature space?
For the second question, keep the original feature space and fitted PCA/UMAP transformations fixed, and project the augmented query into them. Otherwise you could be measuring changes to the representation itself rather than the effect of augmentation on the query.

I would prioritize contrast, gamma, blur and resolution, because they are directly relevant to the visibility of subtle pneumothorax findings, and they're straightforward to implement and compare.

One final caveat: your current 224 × 224 images have already lost detail compared with the original radiographs. That makes resolution sensitivity especially interesting, but also means the findings may not generalize to full-resolution diagnostic images.

A potentially strong research question for your project would be:

How robust are pneumothorax predictions to clinically plausible image perturbations, and are incorrectly classified images more sensitive to these perturbations than correctly classified images?

That would nicely complement your nearest-neighbor analysis, without requiring medical expertise to make claims about what the model actually sees.

# 3. What we did
We used contrast, gamma, blur, and resolution reduction to see how they affect model predictions.
First, we implemented an interactive widget to test different augmentations and strengths on individual images.
Since single images are not representative, we extended the analysis to the whole dataset subset using a fixed strength of 0.6.
We then compared predictions before and after augmentation across different pathologies, focusing on model sensitivity rather than training improvements.