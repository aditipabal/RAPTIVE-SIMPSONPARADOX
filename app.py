import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Simpson's Paradox Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

def generate_simpson_data(n_per_group=50, num_groups=3, group_slope=1.5, noise=0.5, random_seed=42):
    """
    Generates synthetic data demonstrating Simpson's Paradox.

    Each group has a positive slope (group_slope) between x and y,
    but the overall (aggregated) slope is negative because group means for x
    increase while group means for y decrease.
    """
    np.random.seed(random_seed)

    if num_groups == 3:
        x_means = [2.0, 5.0, 8.0]
        y_means = [12.0, 8.0, 4.0]
        group_names = ["Group A", "Group B", "Group C"]
    elif num_groups == 4:
        x_means = [2.0, 5.0, 8.0, 11.0]
        y_means = [15.0, 11.0, 7.0, 3.0]
        group_names = ["Group A", "Group B", "Group C", "Group D"]
    else:
        # Fallback/dynamic generation
        x_means = [2.0 + 3.0 * i for i in range(num_groups)]
        y_means = [5.0 + 4.0 * (num_groups - 1 - i) for i in range(num_groups)]
        group_names = [f"Group {chr(65 + i)}" for i in range(num_groups)]

    data = []
    for i in range(num_groups):
        mu_x = x_means[i]
        mu_y = y_means[i]
        name = group_names[i]

        # Generate x values
        x = np.random.normal(loc=mu_x, scale=0.8, size=n_per_group)
        # Generate y values based on group_slope and normal noise
        y = group_slope * (x - mu_x) + mu_y + np.random.normal(loc=0.0, scale=noise, size=n_per_group)

        for val_x, val_y in zip(x, y):
            data.append({
                "x": val_x,
                "y": val_y,
                "group": name
            })

    return pd.DataFrame(data)

def calculate_regressions(df):
    """
    Computes slope, intercept, and sign for aggregated and group-level regressions.

    Returns a dictionary of regression results and a pandas DataFrame for tabular display.
    """
    results = {}

    # 1. Aggregated regression
    agg_slope, agg_intercept = np.polyfit(df['x'], df['y'], 1)
    results['Aggregated'] = {
        'slope': agg_slope,
        'intercept': agg_intercept,
        'label': 'Aggregated (All data)'
    }

    # 2. Group-level regressions
    for g in sorted(df['group'].unique()):
        group_df = df[df['group'] == g]
        slope, intercept = np.polyfit(group_df['x'], group_df['y'], 1)
        results[g] = {
            'slope': slope,
            'intercept': intercept,
            'label': f'Group-level ({g})'
        }

    # Check if paradox is present
    # Paradox is present if aggregated slope sign differs from ALL group slope signs.
    agg_sign = np.sign(agg_slope)
    paradox_present = True
    for g in sorted(df['group'].unique()):
        g_slope = results[g]['slope']
        if np.sign(g_slope) == agg_sign or np.sign(g_slope) == 0 or agg_sign == 0:
            paradox_present = False
            break

    # Build summary DataFrame for display
    summary_data = []
    for key, val in results.items():
        is_agg = (key == 'Aggregated')

        # Determine paradox status/highlight
        if is_agg:
            status = "Overall Trend"
        else:
            g_slope = val['slope']
            if np.sign(g_slope) != agg_sign:
                status = "🚨 REVERSED (Paradox)"
            else:
                status = "Consistent"

        summary_data.append({
            "Analysis Level": val['label'],
            "Slope": round(val['slope'], 3),
            "Intercept": round(val['intercept'], 3),
            "Trend Direction": "Positive (+)" if val['slope'] > 0 else "Negative (-)",
            "Relation to Overall": status
        })

    summary_df = pd.DataFrame(summary_data)
    return results, summary_df, paradox_present

def create_plot(df, regression_results, view_mode):
    """
    Generates the scatter plot with regression lines based on selected view mode.
    """
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(10, 6))

    x_min, x_max = df['x'].min() - 1, df['x'].max() + 1
    y_min, y_max = df['y'].min() - 2, df['y'].max() + 2

    # Distinct group colors
    palette = sns.color_palette("Set1", n_colors=len(df['group'].unique()))
    group_colors = {g: palette[i] for i, g in enumerate(sorted(df['group'].unique()))}

    if view_mode == "Aggregated":
        # Draw all points with same neutral color
        ax.scatter(df['x'], df['y'], color="grey", alpha=0.5, edgecolors="none", s=50, label="All Data Points")

        # Aggregated regression line
        agg_slope = regression_results['Aggregated']['slope']
        agg_intercept = regression_results['Aggregated']['intercept']
        x_vals = np.linspace(x_min, x_max, 200)
        y_vals = agg_slope * x_vals + agg_intercept
        ax.plot(x_vals, y_vals, color="crimson", linewidth=4, label=f"Overall Regression (slope = {agg_slope:.3f})")

    else: # "By Group"
        # Draw points colored by group
        for g in sorted(df['group'].unique()):
            group_df = df[df['group'] == g]
            color = group_colors[g]
            ax.scatter(group_df['x'], group_df['y'], color=color, alpha=0.7, edgecolors="none", s=60, label=f"{g} Points")

            # Group regression line
            slope = regression_results[g]['slope']
            intercept = regression_results[g]['intercept']

            # Draw line within group's range
            gx_min, gx_max = group_df['x'].min() - 0.5, group_df['x'].max() + 0.5
            x_vals = np.linspace(gx_min, gx_max, 100)
            y_vals = slope * x_vals + intercept
            ax.plot(x_vals, y_vals, color=color, linewidth=3, linestyle="--", label=f"{g} Fit (slope = {slope:.3f})")

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Predictor (x)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Outcome (y)", fontsize=12, fontweight="bold")
    ax.set_title(f"Scatter Plot: {view_mode} View", fontsize=14, fontweight="bold", pad=15)
    ax.legend(loc="best", frameon=True, facecolor="white", edgecolor="none")

    plt.tight_layout()
    return fig

# Streamlit App Logic
st.title("Simpson's Paradox Explorer")

st.markdown("""
Simpson's Paradox is a striking statistical phenomenon where a trend appears in several groups of data but **reverses** when the groups are combined.

This interactive explorer lets you generate synthetic data to visualize how a **confounding variable** (the group membership) can completely flip the direction of a linear relationship between $x$ and $y$.
""")

# Sidebar controls
st.sidebar.header("🛠️ Controls & Parameters")

view_mode = st.sidebar.selectbox(
    "Select View Mode",
    options=["Aggregated", "By Group"],
    help="Choose whether to view the combined data or split by sub-groups."
)

sample_size = st.sidebar.slider(
    "Sample Size (per group)",
    min_value=10,
    max_value=200,
    value=50,
    step=10,
    help="Number of data points generated for each sub-group."
)

num_groups = st.sidebar.slider(
    "Number of Groups",
    min_value=3,
    max_value=4,
    value=3,
    step=1,
    help="Number of categorical sub-groups."
)

group_slope = st.sidebar.slider(
    "Group-level Slope (True)",
    min_value=-2.0,
    max_value=4.0,
    value=1.5,
    step=0.1,
    help="The slope of the relationship between x and y within each group."
)

noise_level = st.sidebar.slider(
    "Noise Level",
    min_value=0.1,
    max_value=3.0,
    value=0.5,
    step=0.1,
    help="Standard deviation of the random noise added to y."
)

random_seed = st.sidebar.number_input(
    "Random Seed",
    min_value=1,
    max_value=1000,
    value=42,
    step=1,
    help="Change the seed to generate different random datasets."
)

# Generate Data
df = generate_simpson_data(
    n_per_group=sample_size,
    num_groups=num_groups,
    group_slope=group_slope,
    noise=noise_level,
    random_seed=random_seed
)

# Calculate Regressions
regression_results, summary_df, paradox_present = calculate_regressions(df)

# Plotting area
fig = create_plot(df, regression_results, view_mode)
st.pyplot(fig)

# Table and Paradox Alert
st.markdown("### 📈 Regression Slopes Summary")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("This table shows the fitted slope and intercept for the overall dataset and for each subgroup:")
    # Display table without index to keep it clean
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

with col2:
    if paradox_present:
        st.success("### 🎉 Simpson's Paradox is PRESENT!")
        st.markdown(
            f"The **overall trend is negative** (slope = **{regression_results['Aggregated']['slope']:.3f}**), "
            "but **every sub-group trend is positive**! This is a perfect example of a statistical reversal."
        )
    else:
        st.warning("### ⚠️ Simpson's Paradox is NOT present.")
        st.markdown(
            "The signs of the aggregated slope and the group-level slopes do not fully contradict. "
            "Try increasing the **Group-level Slope** or adjusting other settings in the sidebar to produce a reversal!"
        )

# Scientific/Mathematical Explanation
st.markdown("---")
st.markdown("### 🧠 How It Works: The Mathematics of the Paradox")

st.markdown(f"""
In this dataset:
1. **Within-Group Relationship:** For each group $i$, $y$ is generated directly as:
   $$y = \\beta \\cdot (x - \\mu_{{x, i}}) + \\mu_{{y, i}} + \\epsilon$$
   where the true slope $\\beta$ is set to **{group_slope:.1f}** (which is positive). As a result, the fitted slopes for all groups are close to this value.

2. **Aggregated Relationship:** The group means are chosen such that as the mean of $x$ increases, the mean of $y$ decreases:
   - Group A: $\\mu_{{x}}$ is low, $\\mu_{{y}}$ is high.
   - Group B: $\\mu_{{x}}$ is medium, $\\mu_{{y}}$ is medium.
   - Group C: $\\mu_{{x}}$ is high, $\\mu_{{y}}$ is low.

   When we combine (aggregate) all the groups together and ignore the group labels, the overall regression line trends downward from the Group A cluster to the Group C cluster, resulting in an aggregated slope of **{regression_results['Aggregated']['slope']:.3f}**.

3. **The Confounder:** Here, `group` acts as a **confounder** because it influences both $x$ (group assignment determines where points lie on the horizontal axis) and $y$ (group assignment determines where points lie on the vertical axis). Omitting `group` from the analysis leads to a severely biased and misleading conclusion.
""")
