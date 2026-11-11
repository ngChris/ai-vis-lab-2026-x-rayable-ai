# AI Interaction 001 — Let the AI analyse plots from the downprojection methods

## 1. Prompt 

[Added image for the analysis](./01_r0_plot_subgroups.png)

In the following are plots for each pathology, showing how the model scored, the actually classification outcomes and age vs confidence.  Threshold was 0.5.

Analyse and interpret the diagrams. find any patterns that might be worth to investigate.

## 2. AI Response

1. AI described the visualize appearence of the plots, for example that there is a very large orange region, while the other outcome categories occupy much smaller regions.
2. AI suggested that the model may be systematically over-predicting pathology rather than making errors randomly.
3. AI formulated the research question: What distinguishes the embedding regions in which the model produces false positives from the regions in which it behaves correctly?
4. AI found that for several pathologies, the UMAP contains clearly seperated or elongated regions. 
5. AI suggests that model's errors may be related to image characteristics.
6. The AI suggests to visualize Age vs model score, split by outcome
7. The AI detects a weak relationship between patien age and model confidence.
8. The AI proposes investigating age, sex, view (AP/PA), and image acquisition characteristics.
9. The AI suggests to not add more random visualizations. 
10. The AI proposed an interactive investigation view.


[Complete AI Response](./01_r0_downprojection_analysis_output.md)

## 3. What we did

The AI was correct in describe the plots, but i didn't provide as any insights or cues. The same goes for 2. We iteratively improved the viewer/plots with the help of the AI (e.g. add hover text) and replaced matplotlib with plotly for more complex visualization. However, we were still not able to detect meaningful patterns or insights about the model. Instead the AI lead us to more complex viszalization often ending in regression analysis.

To get a more structured approach and not let the AI walk us in endless loops, we tried to formulate research questions based on the one the formulated in the Analysis response.

We ended up with the follwing research questions:

1. Can downprojection reveal systematic patterns in the model’s false-positive and false-negative predictions?

2. Which pathologies does the model treat similarly?

3. Are false positives disproportionately associated with particular patient or image characteristics, especially AP/PA view, age and sex?

4. Are the model's predictions locally consistent among visually similar X-ray images, and does this consistency differ between correctly and incorrectly classified samples?

5. Does the model know when it is wrong?

6. Are the model's predictions locally consistent among visually similar X-ray images, and does this consistency differ between correctly and incorrectly classified samples?