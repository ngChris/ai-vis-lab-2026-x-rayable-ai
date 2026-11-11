# Reflection on GenAI usage report
Terminology: AIA pair = GenAI-aided pair, HO pair = human-only pair

## Were there insights found by the human-only pair that the AI-aided pair overlooked, or vice versa?

The AIA pair focused strongly on broad analysis of the distribution of all outputs, which the HO pair did not explore. The AIA pair found that in general, there were no clear clusters over all outputs. Specifically for the different disease labels, certain diseases clearly clustered into positive and negative, and this clear clustering seemed to be associated with the model’s classification confidence
On the other hand, the HO pair focused more on performance metrics than general behavior of the score distribution, and observed a correlation between diagnoses – i.e., if a patient had a positive diagnosis, it was likely that they would have multiple diagnoses, allowing the hypothesis that the model is better at generally detecting diseased vs healthy lungs than specific pathologies.

## How did their visualization choices differ?

The AIA pair produced interactive visualisations and visualisations with large scopes – e.g. unsupervised clusters of all torchxrayvision outputs, bar plots of performance differences over all diagnoses, visualisations of perturbation performance for many different perturbation types at specific perturbation levels – and they used less visualisations to guide the steps in their work.
The HO pair focused initially on performance graphics and entered into concrete hypothesis-exploration loops by using very specific visualisations (heatmaps, line plots, bivariate scatter plots) to explore a hypothesis, rejecting or pursuing the hypothesis, generating a further specific visualisation, and so on. They also relied more on several perturbation steps to assess the effect of a specific type of perturbation on the results.

## Did AI assistance change the breadth or depth of the investigation?

The AIA pair had a broader initial search, while the human-only pair proceeded to the in-depth analysis more quickly. Neither group ended up with a broader array of answers given the amount of data analysed.

## Did it help the AI-aided pair move more quickly, or did verifying and correcting AI suggestions introduce additional work?

Verifying and correcting introduced additional work and the AI-derived suggestions led to a large amount of time being invested in preliminary explorations (“rabbit holes”) rather than exploring hypothesis.

## How did the two pairs differ in their confidence in their conclusions, and what evidence justified that confidence?

The HO pair is somewhat more confident in their conclusions, though it is hard to distinguish what is due to the different usage of GenAI (as described above with the hypothesis-visualisation feedback loops) and what is due to personal medical-domain-specific expertise of the HO pair.
