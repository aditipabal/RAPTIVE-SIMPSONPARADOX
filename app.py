import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Simpson's Paradox Revenue Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

def generate_simpson_data(sample_size=1500, random_seed=42):
    """
    Generates synthetic revenue data demonstrating Simpson's Paradox.

    Predictor: time_on_page (continuous)
    Outcome: revenue (continuous)
    Confounder: browser (categorical: Chrome, Safari, Firefox)
    """
    np.random.seed(random_seed)
    n_per_group = sample_size // 3

    firefox_x = np.random.normal(loc=2.0, scale=0.6, size=n_per_group)
    firefox_y = 4.0 * (firefox_x - 2.0) + 80.0 + np.random.normal(scale=3.0, size=n_per_group)

    safari_x = np.random.normal(loc=5.0, scale=0.6, size=n_per_group)
    safari_y = 4.0 * (safari_x - 5.0) + 50.0 + np.random.normal(scale=3.0, size=n_per_group)

    chrome_x = np.random.normal(loc=8.0, scale=0.6, size=n_per_group)
    chrome_y = 4.0 * (chrome_x - 8.0) + 20.0 + np.random.normal(scale=3.0, size=n_per_group)

    df = pd.DataFrame({
        "time_on_page": np.concatenate([firefox_x, safari_x, chrome_x]),
        "revenue": np.concatenate([firefox_y, safari_y, chrome_y]),
        "browser": ["Firefox"] * n_per_group + ["Safari"] * n_per_group + ["Chrome"] * n_per_group
    })

    df["time_on_page"] = df["time_on_page"].clip(lower=0.1)
    df["revenue"] = df["revenue"].clip(lower=0.1)

    return df

# Sidebar controls
st.sidebar.header("🛠️ Controls & Parameters")

view_mode = st.sidebar.selectbox(
    "Select View Mode",
    options=["Aggregated view", "Browser-level view"],
    help="Choose whether to view the combined revenue data or split by browser type."
)

sample_size = st.sidebar.slider(
    "Sample Size",
    min_value=500,
    max_value=5000,
    value=1500,
    step=100,
    help="Total number of data points to generate across all browser groups."
)

show_regression_lines = st.sidebar.checkbox(
    "Show regression lines",
    value=True,
    help="Toggle rendering of regression fit lines on the scatter plot."
)

# Load Data
df = generate_simpson_data(sample_size=sample_size)

# Calculate regressions
def get_regressions(df):
    results = {}
    # Overall
    agg_slope, agg_intercept = np.polyfit(df['time_on_page'], df['revenue'], 1)
    results['Aggregated'] = {'slope': agg_slope, 'intercept': agg_intercept}

    # Browsers
    for b in sorted(df['browser'].unique()):
        sub = df[df['browser'] == b]
        slope, intercept = np.polyfit(sub['time_on_page'], sub['revenue'], 1)
        results[b] = {'slope': slope, 'intercept': intercept}

    return results

reg_results = get_regressions(df)

# Plotting Function
def create_plot(df, reg_results, view_mode, show_lines):
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    x_min, x_max = df['time_on_page'].min() - 0.5, df['time_on_page'].max() + 0.5
    y_min, y_max = df['revenue'].min() - 5, df['revenue'].max() + 5

    browser_colors = {
        "Chrome": "#4285F4",    # Google blue
        "Safari": "#34A853",    # Clean green
        "Firefox": "#EA4335"    # Clean red
    }

    if view_mode == "Aggregated view":
        # Draw all points with same neutral color
        ax.scatter(df['time_on_page'], df['revenue'], color="grey", alpha=0.4, edgecolors="none", s=30, label="All Visitors")

        if show_lines:
            slope = reg_results['Aggregated']['slope']
            intercept = reg_results['Aggregated']['intercept']
            x_vals = np.linspace(x_min, x_max, 200)
            y_vals = slope * x_vals + intercept
            ax.plot(x_vals, y_vals, color="#E91E63", linewidth=4, label=f"Aggregated Trend (slope = {slope:.3f})")
    else:
        # Draw points colored by browser
        for b in sorted(df['browser'].unique()):
            sub = df[df['browser'] == b]
            color = browser_colors[b]
            ax.scatter(sub['time_on_page'], sub['revenue'], color=color, alpha=0.5, edgecolors="none", s=30, label=f"{b} Visits")

            if show_lines:
                slope = reg_results[b]['slope']
                intercept = reg_results[b]['intercept']
                bx_min, bx_max = sub['time_on_page'].min() - 0.2, sub['time_on_page'].max() + 0.2
                x_vals = np.linspace(bx_min, bx_max, 100)
                y_vals = slope * x_vals + intercept
                ax.plot(x_vals, y_vals, color=color, linewidth=3, linestyle="--", label=f"{b} Trend (slope = {slope:.3f})")

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Time on Page (minutes)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Revenue ($)", fontsize=12, fontweight="bold")
    ax.set_title(f"Revenue vs. Time on Page: {view_mode}", fontsize=14, fontweight="bold", pad=15)
    ax.legend(loc="best", frameon=True, facecolor="white", edgecolor="none")

    plt.tight_layout()
    return fig

# Show Title
st.title("Simpson’s Paradox Revenue Explorer")
st.markdown("An interactive web app demonstrating the danger of aggregated revenue analytics in product and business operations.")

fig = create_plot(df, reg_results, view_mode, show_regression_lines)
st.pyplot(fig)

# Slope Table Display
st.markdown("### 📈 Slope Summary Table")

agg_slope = reg_results['Aggregated']['slope']
group_slopes = [reg_results[b]['slope'] for b in sorted(df['browser'].unique())]
paradox_present = (agg_slope < 0) and all(gs > 0 for gs in group_slopes)

summary_data = [
    {
        "Segment": "Aggregated (Overall)",
        "Slope": round(agg_slope, 3),
        "Trend Direction": "Negative (-)" if agg_slope < 0 else "Positive (+)",
        "Paradox Present": paradox_present
    }
]

for b in sorted(df['browser'].unique()):
    b_slope = reg_results[b]['slope']
    summary_data.append({
        "Segment": f"Browser: {b}",
        "Slope": round(b_slope, 3),
        "Trend Direction": "Positive (+)" if b_slope > 0 else "Negative (-)",
        "Paradox Present": paradox_present
    })

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, width="stretch", hide_index=True)

if paradox_present:
    st.success(f"🎉 **Simpson's Paradox is ACTIVE!** Aggregated Slope is **{agg_slope:.3f}** (Negative), while all individual browser slopes are strictly Positive (ranging between ~3.8 and ~4.3)!")
else:
    st.warning("⚠️ **Simpson's Paradox is not active.** Verify that group slopes are positive and the combined slope is negative.")

# Explanations and Context Panels
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🧠 What is Simpson’s Paradox?")
    st.write(
        "Simpson's Paradox is a statistical phenomenon where a trend or relationship appearing "
        "in separate groups of data **reverses** or disappears when the groups are aggregated "
        "together. This occurs because of a **confounding variable**—a variable that influences "
        "both the predictor and the outcome."
    )

    st.markdown("#### Why do the trends differ in this dataset?")
    st.write(
        "In this dataset, each individual browser has a clear, positive relationship: as users spend more time on "
        "the page, revenue increases. However, the browser groups also have vastly different baselines (means):"
    )
    st.write(
        "- **Firefox** users spend very little time on average (~2 minutes) but produce extremely high baseline revenue (~$80).\n"
        "- **Safari** users have moderate time on page (~5 minutes) and moderate baseline revenue (~$50).\n"
        "- **Chrome** users have very high time on page (~8 minutes) but generate extremely low baseline revenue (~$20)."
    )
    st.write(
        "When the browser label is omitted (Aggregated view), the high-revenue Firefox points on the left and the "
        "low-revenue Chrome points on the right drag the overall regression line downwards, creating a false "
        "conclusion that spending more time on the page leads to *lower* revenue."
    )

with col_right:
    st.markdown("### 💼 Why This Matters for RevOps")
    st.write(
        "In Revenue Operations (RevOps) and product analytics, relying solely on **aggregated metrics** (like "
        "overall site-wide Revenue Per Mille [RPM] or conversion rates) can result in expensive strategic blunders."
    )
    st.write(
        "For instance, an executive analyzing the aggregated data might conclude that 'increased page engagement is hurting "
        "revenue' and decide to reduce content length or page sizes. In reality, increasing page engagement *always* "
        "boosts revenue for every single browser. The negative aggregate slope is entirely an artifact of user distribution."
    )
    st.markdown("#### Confounding Variables & Revenue Diagnostics:")
    st.write(
        "1. **How Aggregated Trends Hide Browser/Platform Effects:** When metrics are combined, the distinct baseline differences "
        "between groups can skew the aggregated trend, hiding the true platform-level performance.\n"
        "2. **Safari Mobile vs. Chrome Desktop:** Safari mobile users often exhibit shorter session times (low time_on_page) but "
        "high baseline conversion/purchasing intent (high revenue). Conversely, Chrome desktop users spend longer browsing (high time_on_page) "
        "but may have lower average transaction sizes (low revenue) or higher bounce rates.\n"
        "3. **Revenue Diagnostics:** RevOps teams must segment metrics by platform, browser, device, or acquisition channel "
        "before making crucial product optimization, ad spent, or budget allocation decisions."
    )
