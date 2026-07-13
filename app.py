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

# 12. Code quality: helper functions for clean architecture
@st.cache_data
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

    
    df["time_on_page"] = df["time_on_page"].clip(lower=0.1)
    df["revenue"] = df["revenue"].clip(lower=0.1)
    
    return df

def get_regressions(df):
    """
    Calculates overall and browser-level regression lines.
    """
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

# 9. Sidebar improvements: short description and organized headers
st.sidebar.markdown("### ℹ️ About")
st.sidebar.markdown(
    "Generate simulated revenue data to explore how Simpson's Paradox can "
    "reverse conclusions when data are aggregated."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Simulation Controls")

view_mode = st.sidebar.selectbox(
    "View Mode",
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

# Load Data and calculate regressions
df = generate_simpson_data(sample_size=sample_size)
reg_results = get_regressions(df)

# Header
st.title("Simpson’s Paradox Revenue Explorer")
st.markdown("An interactive dashboard demonstrating the visual and statistical danger of aggregated metrics in product and business analytics.")

# KPI metrics section at the top
agg_slope = reg_results['Aggregated']['slope']
browser_slopes = [reg_results[b]['slope'] for b in sorted(df['browser'].unique())]
avg_browser_slope = np.mean(browser_slopes)
paradox_present = (agg_slope < 0) and all(gs > 0 for gs in browser_slopes)

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric(
        label="Overall Slope",
        value=f"{agg_slope:.2f}",
        delta="Negative",
        delta_color="inverse"
    )

with kpi_col2:
    st.metric(
        label="Average Browser Slope",
        value=f"{avg_browser_slope:.2f}",
        delta="Positive",
        delta_color="normal"
    )

with kpi_col3:
    paradox_status = "ACTIVE" if paradox_present else "NOT DETECTED"
    st.metric(
        label="Simpson's Paradox",
        value=paradox_status,
        delta="Reversal Active" if paradox_present else "No Reversal",
        delta_color="normal" if paradox_present else "inverse"
    )
st.markdown("---")

# 8. Improve chart presentation
def create_plot(df, reg_results, view_mode, show_lines):
    # Professional Matplotlib/Seaborn config
    sns.set_theme(style="whitegrid")

    
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 13,
        'axes.titlesize': 15,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 11
    })

    fig, ax = plt.subplots(figsize=(11, 6))

    x_min, x_max = df['time_on_page'].min() - 0.5, df['time_on_page'].max() + 0.5
    y_min, y_max = df['revenue'].min() - 5, df['revenue'].max() + 5

    
    fig, ax = plt.subplots(figsize=(11, 6))
    
    x_min, x_max = df['time_on_page'].min() - 0.5, df['time_on_page'].max() + 0.5
    y_min, y_max = df['revenue'].min() - 5, df['revenue'].max() + 5
    
    browser_colors = {
        "Chrome": "#4285F4",    # Professional Blue
        "Safari": "#34A853",    # Professional Green
        "Firefox": "#EA4335"    # Professional Red
    }

    if view_mode == "Aggregated view":
        ax.scatter(
            df['time_on_page'],
            df['revenue'],
            color="#9E9E9E",
            alpha=0.35,
            edgecolors="none",
            s=25,
            label="All Visitors"
        )

        if show_lines:
            slope = reg_results['Aggregated']['slope']
            intercept = reg_results['Aggregated']['intercept']
            x_vals = np.linspace(x_min, x_max, 200)
            y_vals = slope * x_vals + intercept
            ax.plot(
                x_vals,
                y_vals,
                color="#E91E63",
                linewidth=5,
                label=f"Aggregated Trend (slope = {slope:.2f})"
            )
    else:
        for b in sorted(df['browser'].unique()):
            sub = df[df['browser'] == b]
            color = browser_colors[b]
            ax.scatter(
                sub['time_on_page'],
                sub['revenue'],
                color=color,
                alpha=0.45,
                edgecolors="none",
                s=25,
                label=f"{b} Visits"
            )

            if show_lines:
                slope = reg_results[b]['slope']
                intercept = reg_results[b]['intercept']
                bx_min, bx_max = sub['time_on_page'].min() - 0.2, sub['time_on_page'].max() + 0.2
                x_vals = np.linspace(bx_min, bx_max, 100)
                y_vals = slope * x_vals + intercept
                ax.plot(
                    x_vals,
                    y_vals,
                    color=color,
                    linewidth=4,
                    linestyle="--",
                    label=f"{b} Trend (slope = {slope:.2f})"
                )

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Time on Page (minutes)", fontweight="bold", labelpad=10)
    ax.set_ylabel("Revenue ($)", fontweight="bold", labelpad=10)
    ax.set_title(f"Revenue Analytics by Session Duration ({view_mode})", fontweight="bold", pad=15)

    ax.legend(
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor="#E0E0E0",
        framealpha=0.9
    )

    plt.tight_layout()
    return fig

# Render plot
fig = create_plot(df, reg_results, view_mode, show_regression_lines)
st.pyplot(fig)

# 2. Rename Section & 7. Improve regression summary table
st.markdown("### 📈 Regression Summary")

    
    if view_mode == "Aggregated view":
        ax.scatter(
            df['time_on_page'], 
            df['revenue'], 
            color="#9E9E9E", 
            alpha=0.35, 
            edgecolors="none", 
            s=25, 
            label="All Visitors"
        )
        
        if show_lines:
            slope = reg_results['Aggregated']['slope']
            intercept = reg_results['Aggregated']['intercept']
            x_vals = np.linspace(x_min, x_max, 200)
            y_vals = slope * x_vals + intercept
            ax.plot(
                x_vals, 
                y_vals, 
                color="#E91E63", 
                linewidth=5, 
                label=f"Aggregated Trend (slope = {slope:.2f})"
            )
    else:
        for b in sorted(df['browser'].unique()):
            sub = df[df['browser'] == b]
            color = browser_colors[b]
            ax.scatter(
                sub['time_on_page'], 
                sub['revenue'], 
                color=color, 
                alpha=0.45, 
                edgecolors="none", 
                s=25, 
                label=f"{b} Visits"
            )
            
            if show_lines:
                slope = reg_results[b]['slope']
                intercept = reg_results[b]['intercept']
                bx_min, bx_max = sub['time_on_page'].min() - 0.2, sub['time_on_page'].max() + 0.2
                x_vals = np.linspace(bx_min, bx_max, 100)
                y_vals = slope * x_vals + intercept
                ax.plot(
                    x_vals, 
                    y_vals, 
                    color=color, 
                    linewidth=4, 
                    linestyle="--", 
                    label=f"{b} Trend (slope = {slope:.2f})"
                )
                
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Time on Page (minutes)", fontweight="bold", labelpad=10)
    ax.set_ylabel("Revenue ($)", fontweight="bold", labelpad=10)
    ax.set_title(f"Revenue Analytics by Session Duration ({view_mode})", fontweight="bold", pad=15)
    
    ax.legend(
        loc="upper right", 
        frameon=True, 
        facecolor="white", 
        edgecolor="#E0E0E0", 
        framealpha=0.9
    )
    
    plt.tight_layout()
    return fig

# Render plot
fig = create_plot(df, reg_results, view_mode, show_regression_lines)
st.pyplot(fig)

# 2. Rename Section & 7. Improve regression summary table
st.markdown("### 📈 Regression Summary")

summary_data = [
    {
        "Segment": "Aggregated (Overall)",
        "Regression Slope": round(agg_slope, 3),
        "Direction": "Negative (-)" if agg_slope < 0 else "Positive (+)",
        "Interpretation": "Negative relationship" if agg_slope < 0 else "Positive relationship"
    }
]

for b in sorted(df['browser'].unique()):
    b_slope = reg_results[b]['slope']
    summary_data.append({
        "Segment": f"Browser: {b}",
        "Regression Slope": round(b_slope, 3),
        "Direction": "Positive (+)" if b_slope > 0 else "Negative (-)",
        "Interpretation": "Positive relationship" if b_slope > 0 else "Negative relationship"
    })

summary_df = pd.DataFrame(summary_data)

# Highlight aggregated row if it differs from subgroups
def highlight_row(row):
    is_agg = row['Segment'] == "Aggregated (Overall)"
    if is_agg and paradox_present:
        return ['background-color: #FEE8EB; font-weight: bold; color: #D32F2F'] * len(row)
    return [''] * len(row)

styled_df = summary_df.style.apply(highlight_row, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# 3. Improve the success/warning message
if paradox_present:
    st.success(
        "✅ **Simpson's Paradox detected.** "
        "Overall regression is negative while every browser-specific regression remains positive."
    )
else:
    st.warning(
        "⚠️ **Simpson's Paradox not active.** "
        "The overall and subgroup regression slopes do not show opposing signs."
    )

st.markdown("---")

# 4. Improve the text layout & 5. Improve browser explanation & 2. Rename Confounding -> Business Takeaways
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🧠 What is Simpson's Paradox?")
    st.write(
        "Simpson's Paradox is a classical statistical phenomenon where a trend or correlation "
        "reverses when data is aggregated. A trend observed within distinct, meaningful subgroups "
        "can completely disappear or change direction when those subgroups are combined."
    )
    st.write(
        "This occurs because a hidden **confounding variable** relates to both the predictor "
        "and the outcome, altering the overall baseline. Ignoring the confounder leads "
        "to a biased and fundamentally incorrect overall conclusion."
    )

    
    st.markdown("### ❓ Why does it happen?")
    st.write(
        "In this dataset, each individual browser has a clear, positive relationship: as users spend "
        "more time on the page, revenue increases. However, the browser groups have vastly different "
        "baseline averages (means) for both session duration and spending:"
    )

    
    # 5. Replace long bullet points with a compact dynamically generated summary table
    browser_stats = df.groupby('browser').agg(
        avg_time=('time_on_page', 'mean'),
        avg_revenue=('revenue', 'mean')
    ).reset_index()

    browser_stats = browser_stats.sort_values(by='avg_time')
    time_labels = ["Low", "Medium", "High"]
    rev_labels = ["High", "Medium", "Low"]

    browser_stats['Avg Time'] = time_labels
    browser_stats['Avg Revenue'] = rev_labels

    
    browser_stats = browser_stats.sort_values(by='avg_time')
    time_labels = ["Low", "Medium", "High"]
    rev_labels = ["High", "Medium", "Low"]
    
    browser_stats['Avg Time'] = time_labels
    browser_stats['Avg Revenue'] = rev_labels
    
    compact_summary = pd.DataFrame({
        "Browser": browser_stats['browser'],
        "Avg Time": browser_stats['Avg Time'],
        "Avg Revenue": browser_stats['Avg Revenue']
    })

    st.markdown("**Subgroup Baseline Summary (Dynamic):**")
    st.dataframe(compact_summary, use_container_width=True, hide_index=True)

    
    st.markdown("**Subgroup Baseline Summary (Dynamic):**")
    st.dataframe(compact_summary, use_container_width=True, hide_index=True)
    
    st.write(
        "When the browser label is omitted (Aggregated view), the high-revenue, low-engagement Firefox subgroup "
        "and the low-revenue, high-engagement Chrome subgroup drag the combined regression line downwards, "
        "yielding a false negative overall trend."
    )

with col_right:
    st.markdown("### 💼 Business Takeaways")
    st.write(
        "Relying solely on aggregated high-level KPIs can result in expensive strategic blunders. "
        "In RevOps, this paradox highlights why segmentation is crucial before optimizing products or allocating budgets."
    )
    st.write(
        "An executive analyzing the overall combined line might conclude that 'increased page engagement is hurting "
        "revenue' and decide to reduce session length or truncate page content. In reality, increasing page engagement *always* "
        "boosts revenue within every single browser."
    )

    
    st.markdown("#### Why does it matter?")
    st.write(
        "1. **Confounding Variables & Revenue Diagnostics:** Combining user segments with distinct baselines "
        "skews the aggregated trend, masking true performance and leading to attribution errors.\n\n"
        "2. **Safari Mobile vs. Chrome Desktop:** Safari mobile users frequently exhibit shorter session times (low time_on_page) but "
        "extremely high baseline conversion and purchasing intent (high revenue). In contrast, Chrome desktop users spend longer "
        "browsing and researching (high time_on_page) but generate lower transaction value (low revenue) or higher dropoffs."
    )

st.markdown("---")

# 6. Add a "Key Takeaway" box
st.info(
    "💡 **Key Takeaway**\n\n"
    "Simpson's Paradox demonstrates that trends observed in aggregated data can reverse after accounting for meaningful subgroups. "
    "Before making business decisions based on observational data, always investigate potential confounding variables."
)

# 10. Add footer with small divider
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 13px; margin-top: 15px;'>"
    "Built with 🐍 <b>Python</b> | 🎈 <b>Streamlit</b> | 🔢 <b>NumPy</b> | 🐼 <b>Pandas</b> | 🔬 <b>Scikit-learn</b>"
    "</div>",
    unsafe_allow_html=True
)
