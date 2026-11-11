# Phase I, AI-aided pair

The code and the visualization results are stored in the notebooks of this directory. These are the two base notebooks and 6 notebooks about research questions we investigated.

They are structured in the following way:

## Files
| File | Content |
|---|---|
| [Basetools and Dashboard](r0_dataset_overiew_dashboard.ipynb) | This is the base notebook containing the loading of the model and dataset as well as the interactive plots|
| [Tools for neighbor analysis and augmentation ](neighbor_analysis.ipynb) | Contains the functions used for research question 4 and 6. |
| [R1 - Downprojection ](r1_downprojection.ipynb) | Visualizations for **Can downprojection reveal systematic patterns in the model’s false-positive and false-negative predictions?** |
| [R2 - Model prediction similarity ](r2_path_correlation.ipynb) | Visualizations for **Which pathologies does the model treat similarly?** |
| [R3 - Image characteristics/metadata ](r3_false_positive_subgroup_investigation.ipynb) | Visualizations for **Are false positives/negatives disproportionately associated with particular patient or image characteristics, especially AP/PA view, age, sex, and image acquisition?** |
| [R4 - Augmentation ](r4_data_augmentation.ipynb) | Visualizations for **How sensitive does the model respond to certain data augmentations?** |
| [R5 - Confidence in Prediction ](r5_does_the_model_know_when_it_is_wrong.ipynb.ipynb) | Visualizations for **Does the model know when it is wrong?** |
| [R6 - NN Analysis ](r6_kNN_analysis.ipynb) | Visualizations for **Are the model's predictions locally consistent among visually similar X-ray images, and does this consistency differ between correctly and incorrectly classified samples?** |

In addition, we added the notebooks as HTML files in the folder html_notebooks in case the notebooks are not working.