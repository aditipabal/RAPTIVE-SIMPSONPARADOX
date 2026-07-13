# RAPTIVE-SIMPSONPARADOX
Simpson’s Paradox Revenue Explorer
An interactive Streamlit dashboard demonstrating how aggregated metrics can reverse underlying trends due to confounding variables — a phenomenon known as Simpson’s Paradox. This is especially relevant in Revenue Operations (RevOps), where browser, platform, or audience segmentation can dramatically change the interpretation of performance data.

📌 Overview
This app generates synthetic revenue data and shows how:

Each browser segment (Chrome, Safari, Firefox) has a positive relationship between time on page and revenue.

But when all browsers are combined, the overall trend becomes negative.

This reversal illustrates Simpson’s Paradox, a critical concept in analytics and decision‑making.

The dashboard allows users to explore the paradox interactively through scatterplots, regression lines, slope tables, and business explanations.

🎯 Why This Matters (RevOps Context)
In RevOps, relying solely on aggregated KPIs can lead to incorrect strategic decisions. For example:

Safari mobile users may have shorter sessions but higher baseline revenue.

Chrome desktop users may have longer sessions but lower baseline revenue.

When these segments are combined, the aggregated regression can misleadingly suggest that more time on page reduces revenue, even though every individual segment shows the opposite.

This dashboard demonstrates why segmentation is essential before making revenue, product, or optimization decisions.

🧠 Key Features
Synthetic data generation with realistic browser‑level baselines

Aggregated vs browser‑level views

Interactive controls (sample size, regression lines, view mode)

Slope comparison table

Automatic paradox detection

Clear statistical + business explanation panels

Streamlit‑based UI for easy deployment and sharing

📊 Example Output
Aggregated slope: Negative

Browser slopes: Positive

Paradox status: ACTIVE

This reversal is the hallmark of Simpson’s Paradox.


The app is deployed on Streamlit Cloud:

👉 https://raptive-simpsonparadox-7bjvom4bwrjenhn5qf5qku.streamlit.app/
