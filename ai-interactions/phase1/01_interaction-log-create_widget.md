# AI Interaction 001 — Create a widget in IPython Notebook to switch projections

## 1. Prompt 

```
How could i build a widget in python with controls to allow the user switch projection methods ( PCA, UMAP, t-SNE)?
```

## 2. AI Response

Yes. For your project, I’d make the projection itself a reusable function and put a small control panel around it:
- Projection: PCA / UMAP / t-SNE
- Color by: prediction error, pathology, age, sex, AP/PA view
- Parameters: perplexity for t-SNE; n_neighbors and min_dist for UMAP
- Run/update button
- Hover/click: show the corresponding X-ray and metadata

Example: 

run_button.on_click(update_plot)

controls = widgets.VBox([
    method_dropdown,
    color_dropdown,
    neighbors_slider,
    min_dist_slider,
    perplexity_slider,
    run_button
])

display(widgets.HBox([
    controls,
    output
]))

[Complete AI Response](./01_interaction-log-create_widget_output.md)

## 3. What we did

**Decision:** Modified

We used the overall structure of the code but modified it in a way to make it more resusable for other visualizations and simplified it on several places to make it more human readable.