# AI Reflection Phase I

## AI-aided pair
Christoph Schmid, k01155128
Lisa Rastegar, k12509982

## Observed failure patterns
* **Time-consuming rabbit holes:** AI suggestions sometimes led to unnecessary investigations and attempts to tie up loose ends, consuming more time than expected.

* **Prompting bias (yes-man behavior):** The AI would largely agree with our suggestions without sufficiently questioning assumptions or challenging our approach.

* **Hallucinations and incomplete answers:** Even when explicitly instructed to be critical, the AI would sometimes provide partially incorrect, speculative, or half baked answers.

* **Deviating from project requirements:** The AI tended to suggest analyzing the model's learned representations (Phase II), for example by using the model's feature embedding space instead of following the specific requirements of Phase I. It often suggested conventional ML analysis approaches instead of considering the course constraints.

* **Overcomplicated solutions:** The AI was quick to suggest advanced techniques and fancy visualizations, such as dimensionality reduction, without first evaluating whether simpler approaches would be sufficient.

## Emerging best practices
* **Use AI for brainstorming, but critically evaluate its suggestions:** AI can provide useful ideas and alternative approaches, but these should not be accepted without questioning their relevance and validity.

* **Provide clear and specific instructions:** Having a concrete idea of what should be achieved helps guide the AI toward useful solutions and reduces unnecessary complexity.

* **Delegate specific subtasks:** Rather than relying on AI for the entire process of planning, implementation, analysis, and reporting, use it for clearly defined tasks. This reduces the risk of an AI driven feedback loop in which AI generated assumptions or interpretations are repeatedly reinforced without human verification.

* **Provide sufficient project context:** Clearly communicate the project requirements and constraints, particularly the distinction between Phase I and Phase II, to prevent suggestions that fall outside the intended scope.

## Used models
* GPT-6 (assessment, brainstorming, analysis)
* GPT-6.1 Sol (coding, implementation)
* 

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
