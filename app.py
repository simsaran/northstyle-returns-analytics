import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

st.set_page_config(page_title="NorthStyle Returns Analytics",page_icon="🛍️",layout="wide",initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .block-container{padding:1.5rem 2rem}
    .kpi{background:white;border-radius:12px;padding:16px 20px;border:1px solid #E8E8E8;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:8px}
    .kpi-label{font-size:11px;color:#888;margin-bottom:4px;font-weight:500;text-transform:uppercase;letter-spacing:.04em}
    .kpi-value{font-size:26px;font-weight:700;color:#111;line-height:1.1}
    .kpi-note{font-size:11px;color:#888;margin-top:3px}
    .kpi-red .kpi-value{color:#C0392B}
    .kpi-green .kpi-value{color:#0A7540}
    .kpi-amber .kpi-value{color:#B7791F}
    .kpi-blue .kpi-value{color:#0C447C}
    .finding{background:#F0FBF6;border-left:3px solid #27AE60;border-radius:0 8px 8px 0;padding:11px 15px;font-size:13px;color:#1A5C35;margin:10px 0;line-height:1.6}
    .alert{background:#FDF2F2;border-left:3px solid #C0392B;border-radius:0 8px 8px 0;padding:11px 15px;font-size:13px;color:#7B1818;margin:10px 0;line-height:1.6}
    .warning{background:#FEF9EC;border-left:3px solid #F39C12;border-radius:0 8px 8px 0;padding:11px 15px;font-size:13px;color:#7D5A00;margin:10px 0;line-height:1.6}
    .section-title{font-size:15px;font-weight:600;color:#111;margin:18px 0 10px 0;padding-bottom:6px;border-bottom:1.5px solid #EBEBEB}
    footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    base = Path(__file__).parent
    orders   = pd.read_csv(base / "order-data.csv")
    customers= pd.read_csv(base / "customer-data.csv")
    segments = pd.read_csv(base / "segment-summary.csv")
    categories = pd.read_csv(base / "category-analysis.csv")
    scenarios= pd.read_csv(base / "scenario-model.csv")
    with open(base / "key-findings.json") as f:
        findings = json.load(f)
    return orders, customers, segments, categories, scenarios, findings

orders, customers, segments, categories, scenarios, findings = load()

SEG_COLORS = {
    "Loyal Buyer":         "#0A7540",
    "Occasional Returner": "#4285F4",
    "Serial Returner":     "#F59E0B",
    "Bracket Buyer":       "#C0392B",
}

st.markdown("## NorthStyle Co. — Returns and Profitability Analytics")
st.markdown("**January 2024 to December 2024** &nbsp;|&nbsp; 1,800 customers &nbsp;|&nbsp; 10,592 orders &nbsp;|&nbsp; 4 customer segments &nbsp;|&nbsp; 5 product categories")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "  Customer Segments  ",
    "  True Profitability  ",
    "  Return Patterns  ",
    "  Policy Scenarios  ",
])

# ── TAB 1: SEGMENTS ───────────────────────────────────────────────────────────
with tab1:
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="kpi kpi-blue">
            <div class="kpi-label">Total customers</div>
            <div class="kpi-value">1,800</div>
            <div class="kpi-note">Across 4 return behaviour segments</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi kpi-amber">
            <div class="kpi-label">Overall return rate</div>
            <div class="kpi-value">{findings['overall_return_rate']}%</div>
            <div class="kpi-note">By return value as % of gross revenue</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi kpi-red">
            <div class="kpi-label">Unprofitable customers</div>
            <div class="kpi-value">{findings['pct_customers_unprofitable']}%</div>
            <div class="kpi-note">Negative net profit after return costs</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi kpi-green">
            <div class="kpi-label">Most profitable segment</div>
            <div class="kpi-value" style="font-size:18px">Loyal Buyer</div>
            <div class="kpi-note">$375.96 avg net profit per customer</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="alert"><strong>The core finding:</strong> Bracket Buyers generate the highest average revenue per customer at $1,373 but only $79 in net profit after return costs are accounted for. Loyal Buyers spend less but deliver 4.7 times more net profit per customer. Revenue alone is a misleading measure of customer value.</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Customer distribution by segment</div>', unsafe_allow_html=True)
        fig_pie = px.pie(segments, values="Customer Count", names="Segment",
            color="Segment", color_discrete_map=SEG_COLORS, hole=0.45)
        fig_pie.update_layout(height=300, margin=dict(t=10,b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Return rate by segment</div>', unsafe_allow_html=True)
        fig_ret = go.Figure(go.Bar(
            x=segments["Segment"], y=segments["Avg Return Rate %"],
            marker_color=[SEG_COLORS[s] for s in segments["Segment"]],
            text=[f"{v}%" for v in segments["Avg Return Rate %"]],
            textposition="outside",
        ))
        fig_ret.update_layout(height=300, plot_bgcolor="white",
            yaxis=dict(title="Avg Return Rate %", gridcolor="#F1F1F1", ticksuffix="%"),
            xaxis=dict(title=""), margin=dict(t=10,b=20))
        st.plotly_chart(fig_ret, use_container_width=True)

    st.markdown('<div class="section-title">Segment comparison table</div>', unsafe_allow_html=True)
    disp = segments.copy()
    for col in ["Avg Revenue per Customer CAD","Avg Net Profit per Customer CAD","Total Segment Revenue CAD","Total Segment Net Profit CAD"]:
        disp[col] = disp[col].apply(lambda x: f"${x:,.2f}")
    st.dataframe(disp, use_container_width=True, hide_index=True)

# ── TAB 2: TRUE PROFITABILITY ─────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Revenue vs true net profit by segment</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning">Revenue and profit tell completely different stories by segment. A Bracket Buyer generates 70% more revenue than a Loyal Buyer on average. But after return processing costs, return shipping, and the value of returned goods are subtracted, their net profit is 79% lower. This is the gap that free returns policy hides.</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(name="Avg Revenue", x=segments["Segment"],
            y=segments["Avg Revenue per Customer CAD"], marker_color="#94A3B8"))
        fig_rev.add_trace(go.Bar(name="Avg Net Profit", x=segments["Segment"],
            y=segments["Avg Net Profit per Customer CAD"],
            marker_color=[SEG_COLORS[s] for s in segments["Segment"]]))
        fig_rev.update_layout(barmode="group", height=340, plot_bgcolor="white",
            yaxis=dict(title="CAD per customer", gridcolor="#F1F1F1", tickformat="$,.0f"),
            xaxis=dict(title=""),
            legend=dict(orientation="h",y=1.1),
            margin=dict(t=10,b=20))
        st.plotly_chart(fig_rev, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">% of customers who are profitable by segment</div>', unsafe_allow_html=True)
        fig_prof = go.Figure(go.Bar(
            x=segments["Segment"],
            y=segments["% Customers Profitable"],
            marker_color=[SEG_COLORS[s] for s in segments["Segment"]],
            text=[f"{v}%" for v in segments["% Customers Profitable"]],
            textposition="outside",
        ))
        fig_prof.add_hline(y=80, line_dash="dot", line_color="#888", annotation_text="80% benchmark")
        fig_prof.update_layout(height=340, plot_bgcolor="white",
            yaxis=dict(title="% Profitable", gridcolor="#F1F1F1", ticksuffix="%", range=[0,110]),
            xaxis=dict(title=""), margin=dict(t=10,b=20))
        st.plotly_chart(fig_prof, use_container_width=True)

    st.markdown('<div class="section-title">Customer-level profitability distribution</div>', unsafe_allow_html=True)
    seg_filter = st.multiselect("Filter segment", list(SEG_COLORS.keys()), default=list(SEG_COLORS.keys()), key="prof_filter")
    filtered_cust = customers[customers["Segment"].isin(seg_filter)]
    fig_hist = px.histogram(filtered_cust, x="Total Net Profit CAD", color="Segment",
        nbins=50, barmode="overlay", opacity=0.7, color_discrete_map=SEG_COLORS)
    fig_hist.add_vline(x=0, line_dash="dash", line_color="#C0392B", annotation_text="Break-even")
    fig_hist.update_layout(height=300, plot_bgcolor="white",
        xaxis=dict(title="Net Profit per Customer (CAD)", gridcolor="#F1F1F1", tickformat="$,.0f"),
        yaxis=dict(title="Number of customers", gridcolor="#F1F1F1"),
        legend=dict(orientation="h",y=1.1),
        margin=dict(t=10,b=20))
    st.plotly_chart(fig_hist, use_container_width=True)

# ── TAB 3: RETURN PATTERNS ────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Return rate and cost by product category</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_cat = px.bar(categories.sort_values("Return Rate %", ascending=True),
            x="Return Rate %", y="Category", orientation="h",
            color="Return Rate %", color_continuous_scale=["#27AE60","#F59E0B","#C0392B"],
            text="Return Rate %")
        fig_cat.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_cat.update_layout(height=300, plot_bgcolor="white",
            xaxis=dict(title="Return Rate %", gridcolor="#F1F1F1", ticksuffix="%"),
            yaxis=dict(title=""), coloraxis_showscale=False, margin=dict(t=10,b=20))
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        fig_cost = px.bar(categories.sort_values("Return Cost as % of Revenue", ascending=True),
            x="Return Cost as % of Revenue", y="Category", orientation="h",
            color="Return Cost as % of Revenue", color_continuous_scale=["#27AE60","#F59E0B","#C0392B"],
            text="Return Cost as % of Revenue")
        fig_cost.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_cost.update_layout(height=300, plot_bgcolor="white",
            xaxis=dict(title="Return cost as % of revenue", gridcolor="#F1F1F1", ticksuffix="%"),
            yaxis=dict(title=""), coloraxis_showscale=False, margin=dict(t=10,b=20))
        st.plotly_chart(fig_cost, use_container_width=True)

    st.markdown('<div class="section-title">Monthly return volume trend</div>', unsafe_allow_html=True)
    monthly = orders.groupby("Month").agg(
        Total_Orders=("Order ID","count"),
        Returned_Orders=("Returned", lambda x: (x=="Yes").sum()),
    ).reset_index()
    monthly["Return Rate %"] = (monthly["Returned_Orders"] / monthly["Total_Orders"] * 100).round(1)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(name="Total Orders", x=monthly["Month"], y=monthly["Total_Orders"], marker_color="#94A3B8", opacity=0.6))
    fig_trend.add_trace(go.Scatter(name="Return Rate %", x=monthly["Month"], y=monthly["Return Rate %"],
        yaxis="y2", line=dict(color="#C0392B",width=2), mode="lines+markers"))
    fig_trend.update_layout(height=300, plot_bgcolor="white",
        yaxis=dict(title="Orders", gridcolor="#F1F1F1"),
        yaxis2=dict(title="Return Rate %", overlaying="y", side="right", ticksuffix="%"),
        xaxis=dict(title="", tickangle=45),
        legend=dict(orientation="h",y=1.1),
        margin=dict(t=10,b=60))
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown('<div class="section-title">Top return reasons</div>', unsafe_allow_html=True)
    returned_orders = orders[orders["Returned"]=="Yes"]
    reasons = returned_orders["Return Reason"].value_counts().reset_index()
    reasons.columns = ["Reason","Count"]
    reasons["% of Returns"] = (reasons["Count"] / len(returned_orders) * 100).round(1)
    fig_reasons = px.bar(reasons, x="Count", y="Reason", orientation="h",
        color="Count", color_continuous_scale=["#94A3B8","#C0392B"], text="% of Returns")
    fig_reasons.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_reasons.update_layout(height=300, plot_bgcolor="white",
        xaxis=dict(title="Number of returns", gridcolor="#F1F1F1"),
        yaxis=dict(title=""), coloraxis_showscale=False, margin=dict(t=10,b=20))
    st.plotly_chart(fig_reasons, use_container_width=True)

# ── TAB 4: SCENARIOS ──────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Returns policy scenario modelling</div>', unsafe_allow_html=True)
    st.markdown('<div class="finding">Three scenarios are modelled against the current baseline. Scenario B applies a $12 return fee to Serial Returners. Scenario C replaces free returns for Bracket Buyers with a Fit Guarantee — one free exchange per order instead of full returns. Scenario C produces a better outcome because it retains the Bracket Buyer segment while reducing the cost of their behaviour.</div>', unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)
    scenario_data = scenarios.to_dict("records")
    colors = ["kpi-blue","kpi-amber","kpi-green"]
    for col,(sc,cls) in zip([col1,col2,col3],zip(scenario_data,colors)):
        with col:
            vs = f"+${sc['vs Current']:,.0f}" if sc["vs Current"] > 0 else f"${sc['vs Current']:,.0f}" if sc["vs Current"] < 0 else "Baseline"
            st.markdown(f"""<div class="kpi {cls}">
                <div class="kpi-label">{sc['Scenario'].split('—')[0].strip()}</div>
                <div class="kpi-value">${sc['Net Profit CAD']:,.0f}</div>
                <div class="kpi-note">Net profit &nbsp;|&nbsp; {vs} vs current</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Net profit comparison across scenarios</div>', unsafe_allow_html=True)
        fig_sc = px.bar(scenarios, x="Scenario", y="Net Profit CAD",
            color="vs Current", color_continuous_scale=["#C0392B","#94A3B8","#27AE60"],
            text="Net Profit CAD")
        fig_sc.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig_sc.update_layout(height=340, plot_bgcolor="white",
            yaxis=dict(title="Net Profit (CAD)", gridcolor="#F1F1F1", tickformat="$,.0f"),
            xaxis=dict(title="", tickangle=10, tickfont=dict(size=10)),
            coloraxis_showscale=False, margin=dict(t=10,b=80))
        st.plotly_chart(fig_sc, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Cost saving vs revenue impact by scenario</div>', unsafe_allow_html=True)
        fig_breakdown = go.Figure()
        fig_breakdown.add_trace(go.Bar(name="Cost Saving", x=scenarios["Scenario"],
            y=scenarios["Cost Saving CAD"], marker_color="#27AE60"))
        fig_breakdown.add_trace(go.Bar(name="Revenue Impact", x=scenarios["Scenario"],
            y=scenarios["Revenue Impact CAD"], marker_color="#C0392B"))
        fig_breakdown.update_layout(barmode="group", height=340, plot_bgcolor="white",
            yaxis=dict(title="CAD", gridcolor="#F1F1F1", tickformat="$,.0f"),
            xaxis=dict(title="", tickangle=10, tickfont=dict(size=10)),
            legend=dict(orientation="h",y=1.1),
            margin=dict(t=10,b=80))
        st.plotly_chart(fig_breakdown, use_container_width=True)

    st.markdown('<div class="section-title">Scenario detail</div>', unsafe_allow_html=True)
    disp_sc = scenarios.copy()
    for col in ["Revenue Impact CAD","Cost Saving CAD","Net Profit CAD","vs Current"]:
        disp_sc[col] = disp_sc[col].apply(lambda x: f"${x:,.0f}")
    st.dataframe(disp_sc, use_container_width=True, hide_index=True)

st.divider()
st.markdown("**Data note:** All order and customer data is synthetic and generated for portfolio purposes. NorthStyle Co. is a fictional Canadian fashion retailer. Return rates and cost structures are modelled on publicly available ecommerce industry benchmarks. Prepared by Simran Saran as part of The Case Files portfolio series.")
