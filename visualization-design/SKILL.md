---
name: visualization-design
description: Design, evaluate, and validate data visualizations based on analytical purpose, audience, data structure, uncertainty, and end product. Route implementation guidance to Python, notebooks, static HTML, TypeScript, dashboards, reports, or presentations.
metadata:
  short-description: Design clear, honest, decision-useful visualizations
---

# Visualization design

Use this as a technology-agnostic visualization design and quality layer. Determine what the visualization should communicate before choosing a chart type, library, or implementation language.

Follow the user’s requested audience, purpose, stack, format, and constraints. Ask clarifying questions only when ambiguity could materially change the design; otherwise state key assumptions and proceed.

## Establish the purpose

Identify:

- the audience and decision or question the visualization supports;
- whether the work is exploratory, explanatory, or operational;
- the main trend, comparison, distribution, relationship, composition, or geographic pattern;
- the relevant population, period, units, and denominators; and
- the requested end product and interaction requirements.

## Understand the data

Check the data grain, variable types, missingness, outliers, duplicates, category consistency, denominators, and comparability across groups or time. Distinguish counts, rates, percentages, indexes, estimates, and modeled values.

Do not design a visualization that implies precision, causality, completeness, or comparability that the data does not support. Flag data-quality issues that could change the interpretation.

## Select the visual form

Choose the simplest chart or visual form that answers the question clearly:

- position-based charts for precise comparisons;
- lines or areas for trends over time;
- bars or dot plots for category comparisons;
- histograms, density plots, box plots, or violin plots for distributions;
- scatter plots for quantitative relationships;
- heatmaps for patterns across two dimensions;
- maps only when geography is analytically relevant; and
- tables when exact lookup is more important than pattern recognition.

Avoid decorative charts, unnecessary 3D effects, excessive decoration, and chart types that obscure the comparison. Do not add a visualization merely because one is possible.

## Represent uncertainty and caveats

- Include error bars, confidence intervals, credible intervals, prediction intervals, uncertainty bands, or other appropriate uncertainty measures when they are available and relevant.
- Define what each interval or error bar represents, including the confidence level or statistical method where applicable.
- Do not add error bars mechanically when their meaning is unknown or the underlying calculation is unreliable.
- Show sample sizes when they materially affect confidence, especially for subgroup comparisons.
- Flag small samples, sparse categories, high variance, missing data, outliers, unstable estimates, and multiple-comparison concerns when relevant.
- Identify sampling limitations such as convenience sampling, self-selection, survivorship bias, non-random sampling, and coverage gaps.
- For experiments, forecasts, and backtests, disclose the observation window, benchmark, look-ahead risk, leakage, parameter tuning, and generalizability limitations where relevant.
- Distinguish statistical uncertainty from measurement error, model uncertainty, and uncertainty caused by data quality or sampling design.
- Do not imply causality, predictive reliability, or generalizability beyond what the evidence supports.
- Place material caveats near the relevant figure or finding, and summarize major limitations in a dedicated limitations section.

Every visualization should communicate not only the central estimate or observed pattern, but also the uncertainty and limitations that could materially change its interpretation.

## Preserve analytical honesty

- Use scales, baselines, and transformations that do not mislead; disclose truncation, log scales, smoothing, normalization, aggregation, and imputation.
- Label axes, units, dates, categories, and denominators clearly.
- Use color consistently and never rely on color alone to communicate meaning.
- Avoid implying causation from correlation or temporal co-movement.
- Ensure comparisons use compatible definitions and populations.

## Design for communication and accessibility

Every visualization should have a descriptive title, clear labels, an appropriate legend, useful annotations where needed, a concise caption or interpretation, and a source note when external or supplied data is used.

Provide meaningful alt text or an equivalent textual summary. Prefer direct labeling when it improves comprehension. Use a restrained visual hierarchy, readable typography, sufficient contrast, and color palettes suitable for color-vision differences.

## Route by end product

Choose implementation guidance based first on the end product:

- Static HTML: favor portability, self-contained assets, responsive layout, accessible SVG or canvas, and minimal dependencies.
- Dynamic web UI or dashboard: support filtering, interaction state, tooltips, loading and error states, performance, and responsive behavior.
- Python or notebook: prioritize reproducibility, inspectable transformations, statistical validity, and export quality.
- TypeScript or JavaScript: prioritize typed data contracts, component lifecycle, interaction behavior, browser performance, and maintainability.
- Report or presentation: prioritize narrative sequence, annotations, visual hierarchy, and decision-relevant interpretation.

Follow the existing stack where one exists. Do not introduce a framework or library without a practical reason.

## Validate before delivery

Review whether:

- the visual answers the intended question;
- the chart type fits the data and audience;
- calculations, aggregations, intervals, and denominators are correct;
- labels, scales, units, colors, and annotations are accurate;
- uncertainty and material caveats are visible and correctly explained;
- the visual is readable at its intended size and accessible;
- sources and data transformations are traceable; and
- the implementation works in the requested end product.

Inspect or render the visualization when possible. If a trustworthy visualization cannot be produced from the available data, explain why and provide the most useful alternative.

## Response standard

Lead with the design decision or completed result. Briefly explain what the visualization communicates, why the form was selected, what assumptions or transformations were made, and what limitations remain. Keep the explanation concise unless a detailed design rationale is requested.
