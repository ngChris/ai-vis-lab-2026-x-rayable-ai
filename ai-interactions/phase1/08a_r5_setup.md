# AI Interaction 008 — Analysis of the fifth research question output

**Does the model know when it is wrong?**

# 1. Prompt

Does the model know when it is wrong?

Can you show me how i could run this experiment?

# 2. AI Response

Recommendations from the AI to look at:

1. Does confidence correspond to correctness?
2. Use downprojection to look where the false positives are.
3. Investigate if false positives are merely borderline?
4. Are high-confidence false positives systematic?
5. Where do these errors occur?
6. What characterizes the problematic regions?


[Complete AI Response](./08a_r5_analysis_output.md)

## 3. What we did

We did not follow the idea with downprojection as this was already done in previous research questions. Instead, we developed with the AI a plot that showed models confidence vs probablity. This revealed that the model is sometimes highly confident when it is wrong. Therefore the model's confidence does not reliably distinguish correct positive predictions from incorrect positive predictions.

We applied a further plot to focus on the confidence of the incorrect predictions. These observations suggest that the model's confidence behavior is pathology-dependent. In particular, the model sometimes assigns very high scores to incorrect positive predictions.

The AI suggested again to use downprojection to reveal areas of error. We stopped here.