# Report AI Interaction

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
