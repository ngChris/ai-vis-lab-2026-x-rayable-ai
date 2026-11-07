Yes. For your Phase I chest-X-ray project, I’d make the projection itself a reusable function and put a small control panel around it:
- Projection: PCA / UMAP / t-SNE
- Color by: prediction error, pathology, age, sex, AP/PA view
- Parameters: perplexity for t-SNE; n_neighbors and min_dist for UMAP
- Run/update button
- Hover/click: show the corresponding X-ray and metadata
This fits the lecture particularly well: PCA, UMAP and t-SNE are explicitly covered as dimensionality-reduction methods, and the lecture emphasizes that their strengths/weaknesses and hyperparameters can substantially change the resulting projection.     2026 AI  VIS Lecture 03 Explain…     2026 AI  VIS Lecture 03 Explain…

For your assignment, the important part is that the widget shouldn't just be a pretty projection. Your Phase I goal is to investigate systematic false positives/false negatives and their relationship to patient/image attributes, rather than report aggregate performance.    Task-and-Model    lab-assignment
A good Python/Jupyter design
Since you're already working in a notebook with TorchXRayVision, I'd start with ipywidgets + Matplotlib:
import numpy as npimport matplotlib.pyplot as pltimport ipywidgets as widgetsfrom IPython.display import display, clear_outputfrom sklearn.decomposition import PCAfrom sklearn.manifold import TSNEimport umap.umap_ as umapdef compute_projection(X, method="PCA",                       n_neighbors=15,                       min_dist=0.1,                       perplexity=30):    if method == "PCA":        reducer = PCA(n_components=2, random_state=42)    elif method == "UMAP":        reducer = umap.UMAP(            n_components=2,            n_neighbors=n_neighbors,            min_dist=min_dist,            random_state=42        )    elif method == "t-SNE":        reducer = TSNE(            n_components=2,            perplexity=perplexity,            random_state=42,            init="pca"        )    else:        raise ValueError(f"Unknown method: {method}")    return reducer.fit_transform(X)


Then create the controls:
method_dropdown = widgets.Dropdown(    options=["PCA", "UMAP", "t-SNE"],    value="PCA",    description="Projection:")color_dropdown = widgets.Dropdown(    options=[        "Error type",        "Pathology",        "Age",        "Sex",        "View"    ],    value="Error type",    description="Color by:")neighbors_slider = widgets.IntSlider(    value=15,    min=5,    max=100,    step=5,    description="Neighbors:")min_dist_slider = widgets.FloatSlider(    value=0.1,    min=0.0,    max=0.99,    step=0.05,    description="min_dist:")perplexity_slider = widgets.IntSlider(    value=30,


The useful part is then a single plotting function:
def update_plot(_=None):    with output:        clear_output(wait=True)        method = method_dropdown.value        Z = compute_projection(            X,            method=method,            n_neighbors=neighbors_slider.value,            min_dist=min_dist_slider.value,            perplexity=perplexity_slider.value        )        fig, ax = plt.subplots(figsize=(9, 7))        # Replace this with your actual labels        colors = error_labels        scatter = ax.scatter(            Z[:, 0],            Z[:, 1],            c=colors,            s=18,            alpha=0.7        )        ax.set_title(f"{method} projection")        ax.set_xlabel("Dimension 1")        ax.set_ylabel("Dimension 2")        plt.show()


Connect it:
run_button.on_click(update_plot)controls = widgets.VBox([    method_dropdown,    color_dropdown,    neighbors_slider,    min_dist_slider,    perplexity_slider,    run_button])display(widgets.HBox([    controls,    output]))


But I'd make one important improvement
For your particular project, I wouldn't make "Pathology" the main coloring option.

I'd make the central visualization:

Projection of the model's image representations → colored by model behavior

For example:
Color	Meaning
🟢	True positive
🔴	False positive
🔵	True negative
🟠	False negative


Then add controls for:
Projection
[ PCA ▼ ]

Color by
[ Error type ▼ ]

Finding
[ Pneumonia ▼ ]

Age
[ All ▼ ]

Sex
[ All ▼ ]

View
[ All / AP / PA ▼ ]

UMAP parameters
n_neighbors [====●====] 15
min_dist    [==●======] 0.10

t-SNE parameters
perplexity  [====●====] 30

[ Update projection ]

That would let you investigate questions like:
Do false positives form a distinct region of representation space?

Then change:

Color by → Age

and ask:
Are the false-positive regions associated with older patients?

Then:

Color by → View
Is the structure actually driven by AP vs PA acquisition?

Then:

Color by → confidence
Are the errors concentrated in low-confidence regions, or are there high-confidence mistakes?

That is much closer to the assignment's requirement to go beyond simply finding a cluster and ask what distinguishes it, whether there are sub-clusters, and why the model behaves differently there.    lab-assignment
One more thing I'd add: projection comparison
A particularly strong version of the widget would have a toggle:
Projection:  [ PCA | UMAP | t-SNE ]

☐ Compare all projections

When enabled:
┌──────────────┬──────────────┬──────────────┐
│ PCA          │ UMAP         │ t-SNE        │
│              │              │              │
│   • • •      │   •••        │    •••       │
│ • • • •      │ •••••        │  •••••       │
│    • •       │   •••        │    •••       │
└──────────────┴──────────────┴──────────────┘

This is especially useful because the lecture explicitly warns that t-SNE hyperparameters matter, and that apparent cluster sizes/distances can be misleading.     2026 AI  VIS Lecture 03 Explain…

And UMAP similarly has parameters controlling local/global structure.     2026 AI  VIS Lecture 03 Explain…

For your AI-aided pair, this also gives us a meaningful interactive design to iterate on rather than simply asking AI to generate a complete visualization in one shot. The lab instructor specifically describes visualization design as exploratory, progressive and iterative, and recommends using GenAI as a collaborator to explore alternatives and refine them.    90 AI and Visualization - Zoom …

If you want, I can next adapt this directly to your existing xraymodel.ipynb code, including the actual TorchXRayVision embeddings, FP/FN labels, UMAP/PCA/t-SNE switch, and clicking a point to display the corresponding X-ray.