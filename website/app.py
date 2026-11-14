"""
Chicago's Crime Mix
A plain language website for the Urban Crime Pattern Clustering in Chicago (2020 to 2025) project.
All numbers come from the summary tables in app_data, exported from the analysis notebook.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Chicago's Crime Mix", page_icon="🏙️", layout="wide")

DATA = Path(__file__).parent / "app_data"

PROFILE_COLORS = {"Violence heavy": "#C0392B", "Theft heavy": "#2166AC", "Mixed": "#4D9221"}
PROFILE_ORDER = ["Theft heavy", "Mixed", "Violence heavy"]
PROFILE_BLURB = {
    "Theft heavy": "Things go missing more often than people get hurt. These are busy places with shops, offices, "
                   "nightlife and visitors, which means plenty of opportunity for theft.",
    "Violence heavy": "A bigger share of reported crime involves people directly: fights, assaults and robberies. "
                      "These areas also tend to face more economic hardship.",
    "Mixed": "A bit of everything, close to the city's overall mix. No single kind of crime stands out.",
}
PROFILE_WHERE = {
    "Theft heavy": "Downtown, the north lakefront and O'Hare",
    "Violence heavy": "Much of the West and South Sides",
    "Mixed": "The northwest and southwest edges of the city",
}
CRIME_TYPES = ["Theft", "Battery", "Criminal Damage", "Assault", "Motor Vehicle Theft", "Robbery", "Burglary"]
CRIME_MEANING = {
    "Theft": "something taken without force or threat, such as shoplifting or a stolen phone",
    "Battery": "physically attacking someone",
    "Criminal Damage": "damaging property, such as vandalism or broken windows",
    "Assault": "threatening or attempting to attack someone",
    "Motor Vehicle Theft": "stealing a car or other vehicle",
    "Robbery": "taking something from a person by force or threat",
    "Burglary": "breaking into a building to steal",
}
YEARS = list(range(2020, 2026))
CRIME_SHORT = {"Theft": "theft", "Battery": "battery", "Criminal Damage": "criminal damage", "Assault": "assault",
               "Motor Vehicle Theft": "car theft", "Robbery": "robbery", "Burglary": "burglary"}


def display_name(name):
    return "the Loop" if name == "Loop" else name


def join_words(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


# --------------------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------------------
@st.cache_data
def load_data():
    areas = pd.read_csv(DATA / "areas.csv")
    areas = areas.sort_values("Community").reset_index(drop=True)
    count_cols = [f"Count {t}" for t in CRIME_TYPES]
    areas["Total Crimes"] = areas[count_cols].sum(axis=1)
    areas["Crimes per 1,000 per year"] = areas["Total Crimes"] / areas["Population"] * 1000 / 6
    areas["Violence to theft"] = (areas["Count Battery"] + areas["Count Assault"]) / areas["Count Theft"]

    city_counts = areas[count_cols].sum()
    city_shares = (city_counts / city_counts.sum() * 100)
    city_shares.index = CRIME_TYPES

    daily = pd.read_csv(DATA / "daily.csv", parse_dates=["Date"])
    temps = pd.read_csv(DATA / "temperature_effects.csv")
    return areas, city_shares, daily, temps


areas, city_shares, daily, temps = load_data()


def temp_effect(group, model="Controlled"):
    row = temps[(temps["Crime group"] == group) & (temps["Model"] == model)].iloc[0]
    return row["Percent per 10°F"], row["CI low"], row["CI high"]


# --------------------------------------------------------------------------------------
# Look and feel
# --------------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"], .stMarkdown, p, li, label { font-family: 'Inter', sans-serif; }
    h1, h2, h3, .hero-title { font-family: 'Fraunces', Georgia, serif !important; letter-spacing: -0.01em; }
    .block-container { padding-top: 4.5rem; max-width: 1150px; }
    .hero-title { font-size: 2.9rem; line-height: 1.1; font-weight: 800; margin: 0 0 0.6rem 0; color: #1F1B16; }
    .hero-sub { font-size: 1.2rem; color: #4A4238; max-width: 760px; margin-bottom: 1.4rem; }
    .eyebrow { text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.78rem; font-weight: 600; color: #8A6D3B; }
    .stat { background: #FFFFFF; border: 1px solid #E8E1D6; border-radius: 14px; padding: 1rem 1.2rem; }
    .stat .num { font-family: 'Fraunces', serif; font-size: 2.2rem; font-weight: 800; color: #1F1B16; line-height: 1.1; }
    .stat .lbl { color: #6B6155; font-size: 0.95rem; }
    .card { background: #FFFFFF; border: 1px solid #E8E1D6; border-radius: 16px; padding: 1.2rem 1.3rem; height: 100%;
            border-top: 6px solid var(--accent); }
    .card h4 { font-family: 'Fraunces', serif; margin: 0 0 0.4rem 0; color: var(--accent); font-size: 1.35rem; }
    .card p { margin: 0 0 0.5rem 0; color: #3A332B; }
    .card .where { font-size: 0.88rem; color: #6B6155; }
    .badge { display: inline-block; padding: 0.25rem 0.8rem; border-radius: 999px; color: #fff; font-weight: 600;
             font-size: 0.95rem; background: var(--accent); }
    .chip { display: inline-block; padding: 0.35rem 0.6rem; border-radius: 8px; color: #fff; font-weight: 600;
            font-size: 0.8rem; margin: 0 0.25rem 0.3rem 0; text-align: center; min-width: 92px; }
    .dyk { background: #FFF6E5; border-left: 5px solid #E0A526; border-radius: 10px; padding: 0.9rem 1.1rem; margin: 0.4rem 0 1rem 0; }
    .dyk b { color: #8A5A00; }
    .note { color: #6B6155; font-size: 0.9rem; }
    .light { display: flex; gap: 0.9rem; align-items: flex-start; background: #FFFFFF; border: 1px solid #E8E1D6;
             border-radius: 14px; padding: 1rem 1.1rem; margin-bottom: 0.8rem; }
    .light .dot { width: 22px; height: 22px; border-radius: 50%; flex: 0 0 22px; margin-top: 3px; }
    .light h5 { margin: 0 0 0.2rem 0; font-size: 1.05rem; }
    .light p { margin: 0; color: #3A332B; }
    .big-sentence { font-family: 'Fraunces', serif; font-size: 1.45rem; line-height: 1.35; color: #1F1B16; margin: 0.4rem 0 1rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


def did_you_know(text):
    st.markdown(f'<div class="dyk"><b>Did you know?</b> {text}</div>', unsafe_allow_html=True)


def badge(profile):
    return f'<span class="badge" style="--accent:{PROFILE_COLORS[profile]}">{profile}</span>'


def one_in(share):
    n = max(1, round(100 / share))
    return "almost 1 in 2" if n == 2 and share < 50 else f"about 1 in {n}"


def add_basemap(fig):
    """Light street map drawn from raster tiles, so the circles still show if the tiles are slow to load."""
    fig.update_layout(map_layers=[{
        "below": "traces", "sourcetype": "raster",
        "sourceattribution": "© OpenStreetMap contributors © CARTO",
        "source": ["https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"]}])
    return fig


def base_layout(fig, height=380):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", size=13, color="#3A332B"),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title_text=""))
    return fig


# --------------------------------------------------------------------------------------
# Page 1: Home
# --------------------------------------------------------------------------------------
def page_home():
    st.markdown('<div class="eyebrow">Chicago, 2020 to 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Two neighborhoods can have the same amount of crime and a completely different story.</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">We looked at over a million reported crimes and asked a simple question: '
                'what <i>kind</i> of crime does each Chicago neighborhood see? The answer sorts the city into three '
                'crime mix profiles.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, num, lbl in [(c1, "1,065,190", "reported crimes analysed"),
                          (c2, "77", "community areas, the city's official neighborhoods"),
                          (c3, "6 years", "of data, from 2020 to 2025")]:
        col.markdown(f'<div class="stat"><div class="num">{num}</div><div class="lbl">{lbl}</div></div>',
                     unsafe_allow_html=True)

    st.write("")
    st.subheader("Meet the three profiles")
    cols = st.columns(3)
    for col, p in zip(cols, PROFILE_ORDER):
        n = int((areas["Profile"] == p).sum())
        theft = areas.loc[areas["Profile"] == p, "Share Theft"].mean()
        col.markdown(
            f'<div class="card" style="--accent:{PROFILE_COLORS[p]}"><h4>{p}</h4>'
            f'<p>{PROFILE_BLURB[p]}</p>'
            f'<p><b>{n} neighborhoods.</b> On average {theft:.0f}% of their reported crime is theft.</p>'
            f'<div class="where">Mostly found in: {PROFILE_WHERE[p]}</div></div>',
            unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([3, 2])
    with left:
        st.subheader("What makes this different?")
        st.markdown(
            "Most crime maps only tell you **how much** crime there is. That hides a lot. A busy downtown street and a "
            "quiet residential block can report similar numbers for completely different reasons.\n\n"
            "Looking at the **mix** of crime tells you more about what is actually going on, and it turns out to line "
            "up closely with how much economic hardship a neighborhood faces.")
        st.page_link(PAGES["neighborhood"], label="Find your neighborhood", icon="🔎")
        st.page_link(PAGES["map"], label="See the whole city on a map", icon="🗺️")
    with right:
        did_you_know("The Loop logged about <b>415 thefts for every 1,000 residents</b> over these six years, the highest "
                     "in the city. That's not because Loop residents are unlucky: the hundreds of thousands of workers, "
                     "shoppers and tourists who pass through are not counted as residents.")
        summer = daily.loc[daily["Season"] == "Summer", "Total_Crime"].mean()
        winter = daily.loc[daily["Season"] == "Winter", "Total_Crime"].mean()
        did_you_know(f"An average summer day in Chicago sees about <b>{summer - winter:.0f} more reported crimes</b> "
                     f"than an average winter day ({summer:.0f} against {winter:.0f}).")

    st.markdown('<p class="note">Profiles describe the kind of crime that gets <i>reported</i> to police. They are not a '
                'judgment of the people who live in a neighborhood, and they are not a safety rating.</p>',
                unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# Page 2: Find your neighborhood
# --------------------------------------------------------------------------------------
def certainty_text(row):
    agree = int(row["Methods agreeing"]) + 1
    if agree == 4:
        return "Clear fit", f"All 4 methods we tried put {display_name(row['Community'])} in this profile."
    if agree == 3:
        return "Mostly fits", f"3 of the 4 methods we tried agree. {display_name(row['Community']).capitalize() if row['Community'] == 'Loop' else row['Community']} sits close to a border."
    return "On the border", f"Only 2 of the 4 methods agree, so its mix sits between two profiles."


def change_text(row):
    path = [row[f"Profile {y}"] for y in YEARS]
    place = display_name(row["Community"])
    if row["Stable All Years"]:
        text = f"Looked at year by year, {place} fell in the **{path[0]}** group every single year from 2020 to 2025."
    else:
        counts = pd.Series(path).value_counts()
        main = counts.index[0]
        years_other = [str(y) for y, p in zip(YEARS, path) if p != main]
        others = join_words(dict.fromkeys(p for p in path if p != main))
        text = (f"Looked at year by year, {place} was mostly **{main}**, but looked more like **{others}** in "
                f"{join_words(years_other)}. Its mix moves a little from year to year.")
    if path.count(row["Profile"]) < 3:
        text += (f" Over all six years combined its mix counts as {row['Profile']}, while most single years lean "
                 f"the other way, a sign it sits right on the border between two profiles.")
    return text


def share_chart(rows):
    fig = go.Figure()
    for label, shares, color in reversed(rows):
        fig.add_trace(go.Bar(y=CRIME_TYPES, x=[shares[t] for t in CRIME_TYPES], name=label, orientation="h",
                             marker_color=color, hovertemplate="%{y}: %{x:.1f}%<extra>" + label + "</extra>"))
    fig = base_layout(fig, height=440)
    fig.update_layout(barmode="group", yaxis=dict(autorange="reversed"), xaxis_title="Share of reported crime (%)",
                      legend=dict(traceorder="reversed"))
    return fig


def area_shares(row):
    return pd.Series({t: row[f"Share {t}"] for t in CRIME_TYPES})


def page_neighborhood():
    st.title("Find your neighborhood")
    st.write("Pick any of Chicago's 77 community areas to see its crime mix story.")

    names = areas["Community"].tolist()
    default = names.index("Lincoln Park")
    c1, c2 = st.columns([2, 1])
    name = c1.selectbox("Neighborhood", names, index=default)
    compare = c2.toggle("Compare with another neighborhood")
    other = None
    if compare:
        other = c2.selectbox("Compare with", [n for n in names if n != name],
                             index=[n for n in names if n != name].index("Englewood") if name != "Englewood" else 0)

    row = areas[areas["Community"] == name].iloc[0]
    shares = area_shares(row)
    p = row["Profile"]

    st.markdown(f"## {display_name(name)[0].upper() + display_name(name)[1:]} {badge(p)}", unsafe_allow_html=True)
    st.write(PROFILE_BLURB[p])

    theft, city_theft = shares["Theft"], city_shares["Theft"]
    ratio = (shares / city_shares).drop("Theft")
    standout = ratio.idxmax()
    place = display_name(name)
    if one_in(theft) == one_in(city_theft):
        more = "a little above" if theft > city_theft else "a little below"
        sentence = (f"In {place}, {one_in(theft)} reported crimes is a theft ({theft:.0f}%), "
                    f"{more} the city as a whole ({city_theft:.0f}%).")
    else:
        sentence = (f"In {place}, {one_in(theft)} reported crimes is a theft ({theft:.0f}%). "
                    f"Across Chicago it's {one_in(city_theft)} ({city_theft:.0f}%).")
    if ratio[standout] > 1.15:
        sentence += f" {CRIME_SHORT[standout].capitalize()} is also more common here than in the city overall."
    st.markdown(f'<div class="big-sentence">{sentence}</div>', unsafe_allow_html=True)

    left, right = st.columns([3, 2])
    with left:
        st.markdown("#### Crime mix compared with Chicago")
        rows = [(display_name(name), shares, PROFILE_COLORS[p])]
        if other:
            orow = areas[areas["Community"] == other].iloc[0]
            ocol = PROFILE_COLORS[orow["Profile"]]
            if orow["Profile"] == p:
                ocol = "#1F1B16"
            rows.append((display_name(other), area_shares(orow), ocol))
        rows.append(("Chicago overall", city_shares, "#C9C0B3"))
        st.plotly_chart(share_chart(rows), width="stretch")
        with st.expander("What do these crime types mean?"):
            st.markdown("\n".join(f"- **{t}**: {CRIME_MEANING[t]}" for t in CRIME_TYPES))

    with right:
        label, detail = certainty_text(row)
        st.markdown("#### How sure are we?")
        st.markdown(f"**{label}.** {detail}")

        st.markdown("#### Economic hardship")
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=row["Hardship Index"], number={"font": {"size": 40, "family": "Fraunces"}},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#1F1B16", "thickness": 0.3},
                   "steps": [{"range": [0, 33], "color": "#E9F1E1"}, {"range": [33, 66], "color": "#F8EBC8"},
                             {"range": [66, 100], "color": "#F4D3CE"}]}))
        gauge.update_layout(height=200, margin=dict(l=30, r=40, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(gauge, width="stretch")
        st.markdown(f'<p class="note">Hardship Index from 0 to 100, combining unemployment, poverty, income, '
                    f'education, crowded housing and the share of very young and old residents. The city median is '
                    f'{areas["Hardship Index"].median():.0f}; higher means more hardship.</p>', unsafe_allow_html=True)

    st.markdown("#### Has it changed since 2020?")
    chips = "".join(f'<span class="chip" style="background:{PROFILE_COLORS[row[f"Profile {y}"]]}">{y}<br>'
                    f'{row[f"Profile {y}"]}</span>' for y in YEARS)
    st.markdown(chips, unsafe_allow_html=True)
    st.markdown(change_text(row))

    st.markdown("#### Does warm weather matter here?")
    eff = row["Temp Effect per 10F"]
    median_eff = areas["Temp Effect per 10F"].median()
    if pd.isna(eff):
        st.write(f"{display_name(name)[0].upper() + display_name(name)[1:]} has fewer than one reported crime a day on average, which is too few to measure a "
                 "reliable temperature effect.")
    elif eff < 1:
        st.write(f"Hardly at all. On a day 10°F warmer than usual for the time of year, reported crime in {display_name(name)} "
                 f"barely changes. Across the city the typical increase is about {median_eff:.0f}%.")
    else:
        st.write(f"On a day 10°F warmer than usual for the time of year, reported crime in {display_name(name)} tends to be about "
                 f"**{eff:.0f}% higher**. Across the city the typical increase is about {median_eff:.0f}%.")
    st.markdown('<p class="note">Estimates for smaller neighborhoods are less precise because they have fewer '
                'crimes to learn from.</p>', unsafe_allow_html=True)

    if name == "Loop":
        did_you_know("The Loop's theft share is high partly because so many people visit without living there. "
                     "Criminologists call this the routine activity effect: crime happens where people and "
                     "opportunities meet.")
    if name == "Oakland":
        did_you_know("Oakland saw a sharp rise in car thefts from late 2022 to 2023, which briefly changed its "
                     "crime mix. Car theft then eased but stayed above its 2020 level.")


# --------------------------------------------------------------------------------------
# Page 3: Map
# --------------------------------------------------------------------------------------
def page_map():
    st.title("The city at a glance")
    st.write("Each circle is one community area, placed at its centre. Hover over a circle to see its name.")

    view = st.radio("Colour the map by", ["Crime mix profile", "Economic hardship"], horizontal=True)
    df = areas.copy()
    df["Hardship"] = df["Hardship Index"]
    df["Theft share (%)"] = df["Share Theft"].round(1)

    if view == "Crime mix profile":
        fig = px.scatter_map(df, lat="Latitude", lon="Longitude", color="Profile", hover_name="Community",
                             hover_data={"Latitude": False, "Longitude": False, "Hardship": ":.1f",
                                         "Theft share (%)": True, "Profile": True},
                             color_discrete_map=PROFILE_COLORS, category_orders={"Profile": PROFILE_ORDER},
                             zoom=9.6, center={"lat": 41.835, "lon": -87.69}, map_style="white-bg")
    else:
        fig = px.scatter_map(df, lat="Latitude", lon="Longitude", color="Hardship", hover_name="Community",
                             hover_data={"Latitude": False, "Longitude": False, "Hardship": ":.1f",
                                         "Profile": True},
                             color_continuous_scale=["#F3EDE2", "#E0A526", "#8E2B1E"], range_color=[0, 85],
                             zoom=9.6, center={"lat": 41.835, "lon": -87.69}, map_style="white-bg")
    fig.update_traces(marker=dict(size=17, opacity=0.9))
    add_basemap(fig)
    fig.update_layout(height=640, margin=dict(l=0, r=0, t=0, b=0), legend=dict(title="", x=0.01, y=0.01,
                      bgcolor="rgba(255,255,255,0.85)"))
    st.plotly_chart(fig, width="stretch")

    st.markdown("**Try switching between the two views.** The red violence heavy areas on the West and South Sides "
                "line up closely with the darker high hardship areas, while the blue theft heavy areas sit where "
                "hardship is lowest. Location was never used to build the profiles, so this pattern came from the "
                "crime mix alone.")
    st.markdown('<p class="note">Circles mark the centre of each community area, not the exact places where crimes '
                'happened.</p>', unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# Page 4: Weather
# --------------------------------------------------------------------------------------
def page_weather():
    st.title("Does weather matter?")
    st.write("Yes, and you can feel it. Warm days bring more reported crime across Chicago, even after accounting "
             "for the day of the week, the month and the year.")

    st.markdown("#### Move the thermometer")
    warmer = st.slider("How much warmer than usual is the day? (°F)", 0, 25, 10)
    v, _, _ = temp_effect("Violent")
    pr, _, _ = temp_effect("Property")
    v_pct = ((1 + v / 100) ** (warmer / 10) - 1) * 100
    p_pct = ((1 + pr / 100) ** (warmer / 10) - 1) * 100
    v_base = daily["Violent"].mean()
    p_base = daily["Property"].mean()

    c1, c2 = st.columns(2)
    c1.metric("Violent crime (battery, assault, robbery)", f"+{v_pct:.1f}%",
              f"about {v_base * v_pct / 100:.0f} more reports on a typical day", delta_color="off")
    c2.metric("Property crime (theft, damage, car theft, burglary)", f"+{p_pct:.1f}%",
              f"about {p_base * p_pct / 100:.0f} more reports on a typical day", delta_color="off")
    st.markdown(f'<p class="note">Based on {len(daily):,} days. On a typical day Chicago records about {v_base:.0f} '
                f'violent and {p_base:.0f} property crimes of these types. This is an average pattern over six '
                f'years, not a forecast for tomorrow.</p>', unsafe_allow_html=True)

    st.markdown("Violent crime reacts a little more to heat than property crime does. The gap is small, about one "
                "percentage point for every 10°F, but it shows up consistently in the data.")

    st.markdown("#### Crime and temperature, month by month")
    m = daily.set_index("Date").resample("MS").agg({"Total_Crime": "mean", "TAVG": "mean"}).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=m["Date"], y=m["Total_Crime"], name="Average reported crimes per day",
                             line=dict(color="#1F1B16", width=2.5)))
    fig.add_trace(go.Scatter(x=m["Date"], y=m["TAVG"], name="Average temperature (°F)", yaxis="y2",
                             line=dict(color="#E0A526", width=2.5, dash="dot")))
    fig = base_layout(fig, height=400)
    fig.update_layout(yaxis=dict(title="Crimes per day"), yaxis2=dict(title="°F", overlaying="y", side="right",
                      showgrid=False), hovermode="x unified")
    st.plotly_chart(fig, width="stretch")
    st.write("The two lines rise and fall together every year. The overall level also climbed after 2021, which "
             "is why the analysis compares each day with others in the same month and year.")

    st.markdown("#### The seasons")
    order = ["Winter", "Spring", "Summer", "Fall"]
    s = daily.groupby("Season")["Total_Crime"].mean().reindex(order).reset_index()
    fig2 = px.bar(s, x="Season", y="Total_Crime", text=s["Total_Crime"].round(0).astype(int),
                  color="Season", color_discrete_map={"Winter": "#7FA7C9", "Spring": "#8DBF7A",
                                                      "Summer": "#E0A526", "Fall": "#C9733A"},
                  labels={"Total_Crime": "Average reported crimes per day", "Season": ""})
    fig2 = base_layout(fig2, height=340)
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, width="stretch")

    did_you_know("The single busiest day in the data, May 31, 2020, had nothing to do with weather. It was a "
                 "mild 59°F day during the unrest after the killing of George Floyd, and the spike was driven "
                 "mainly by property crime.")


# --------------------------------------------------------------------------------------
# Page 5: Hardship and crime
# --------------------------------------------------------------------------------------
def page_hardship():
    st.title("Hardship and crime")
    st.markdown('<div class="big-sentence">Neighborhoods facing more hardship tend to have a different <i>kind</i> '
                'of crime, more than a different <i>amount</i>.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### The kind of crime")
        fig = px.scatter(areas, x="Hardship Index", y="Violence to theft", color="Profile", hover_name="Community",
                         color_discrete_map=PROFILE_COLORS, category_orders={"Profile": PROFILE_ORDER},
                         labels={"Violence to theft": "Battery and assault cases per theft"},
                         hover_data={"Violence to theft": ":.2f", "Hardship Index": ":.1f"})
        fig.update_traces(marker=dict(size=11, line=dict(width=0.5, color="white")))
        st.plotly_chart(base_layout(fig, 400), width="stretch")
        st.write("As hardship rises, battery and assault make up more of the crime mix compared with theft. "
                 "The points form a clear, tight upward band.")
    with c2:
        st.markdown("#### The amount of crime")
        fig = px.scatter(areas, x="Hardship Index", y="Crimes per 1,000 per year", color="Profile",
                         hover_name="Community", color_discrete_map=PROFILE_COLORS,
                         category_orders={"Profile": PROFILE_ORDER},
                         labels={"Crimes per 1,000 per year": "Reported crimes per 1,000 residents a year"},
                         hover_data={"Crimes per 1,000 per year": ":.0f", "Hardship Index": ":.1f"})
        fig.update_traces(marker=dict(size=11, line=dict(width=0.5, color="white")))
        st.plotly_chart(base_layout(fig, 400), width="stretch")
        st.write("The total amount of crime also rises with hardship, but the points are much more scattered. "
                 "Busy low hardship areas like the Loop sit near the top.")

    st.markdown("#### In numbers")
    st.write("The crime mix explains about **72%** of the differences in hardship between neighborhoods. The total "
             "amount of crime explains only about **19%**. Theft on its own shows almost no link to hardship.")

    order = ["Violence heavy", "Mixed", "Theft heavy"]
    med = areas.groupby("Profile")["Hardship Index"].median().reindex(order)
    cols = st.columns(3)
    for col, p in zip(cols, order):
        col.markdown(f'<div class="card" style="--accent:{PROFILE_COLORS[p]}"><h4>{p}</h4>'
                     f'<p>Typical hardship score</p><div class="stat" style="border:none;padding:0">'
                     f'<div class="num">{med[p]:.1f}</div></div></div>', unsafe_allow_html=True)

    st.write("")
    st.info("**Linked does not mean caused.** These patterns show that hardship and the crime mix go together. "
            "They do not show that hardship causes crime, and reported crime also depends on how often people "
            "report and how areas are policed.", icon="⚖️")


# --------------------------------------------------------------------------------------
# Page 6: How sure are we?
# --------------------------------------------------------------------------------------
def light(color, title, text):
    st.markdown(f'<div class="light"><div class="dot" style="background:{color}"></div><div><h5>{title}</h5>'
                f'<p>{text}</p></div></div>', unsafe_allow_html=True)


def page_sure():
    st.title("How sure are we?")
    st.write("A pattern is only useful if it holds up. We checked our answer in four different ways. "
             "Green means it held up well, amber means it held up in part.")

    green, amber = "#4D9221", "#E0A526"
    core = int(areas["Robust core"].sum())
    stable = int(areas["Stable All Years"].sum())
    light(amber, "A completely different grouping method",
          f"We repeated the grouping with a second family of methods (hierarchical clustering) in three versions. "
          f"<b>{core} of 77 neighborhoods</b> landed in the same profile every time, including the clearest theft "
          f"heavy and violence heavy areas. The others sit near a border between two profiles.")
    light(green, "The link with hardship",
          "Under every method we tried, hardship followed the same order: highest in violence heavy areas, lowest in "
          "theft heavy areas. This held even though hardship was never used to build the groups.")
    light(green, "A different way of measuring the mix",
          "Treating rare crimes like robbery more fairly (a log ratio transformation) kept <b>61 of 77</b> "
          "neighborhoods in the same profile, and 34 of the 35 violence heavy areas.")
    light(amber, "Year by year",
          f"<b>{stable} of 77</b> neighborhoods kept the same profile in all six years. The contrast between theft "
          f"and other crime is very steady over time. Finer differences between the other crime types move around "
          f"from year to year.")

    st.markdown("#### Clear fits and border areas")
    df = areas.copy()
    df["Fit"] = np.where(df["Robust core"], "Clear fit", "Near a border")
    fig = px.scatter_map(df, lat="Latitude", lon="Longitude", color="Profile", hover_name="Community",
                         size=np.where(df["Robust core"], 16, 8), size_max=16,
                         hover_data={"Latitude": False, "Longitude": False, "Fit": True, "Profile": True},
                         color_discrete_map=PROFILE_COLORS, category_orders={"Profile": PROFILE_ORDER},
                         zoom=9.45, center={"lat": 41.835, "lon": -87.69}, map_style="white-bg")
    add_basemap(fig)
    fig.update_layout(height=560, margin=dict(l=0, r=0, t=0, b=0),
                      legend=dict(title="", x=0.01, y=0.01, bgcolor="rgba(255,255,255,0.85)"))
    st.plotly_chart(fig, width="stretch")
    st.write("Big circles are clear fits; small circles are near a border. Border areas tend to sit where the "
             "theft heavy, mixed and violence heavy parts of the city meet, which suggests the crime mix changes "
             "gradually across the city rather than at sharp lines.")


# --------------------------------------------------------------------------------------
# Page 7: About
# --------------------------------------------------------------------------------------
def page_about():
    st.title("About this project")
    st.write("This website presents a student data science project for the course Computer Programming for Data "
             "Science and AI at the Asian Institute of Technology (AIT), taught by Dr. Chantri Polprasert.")
    st.markdown("**Project:** Urban Crime Pattern Clustering in Chicago (2020 to 2025)  \n**Team:** NEKOLAB")

    st.markdown("#### How it works, in one paragraph")
    st.write("For each neighborhood we worked out what share of its reported crime fell into each of seven types. "
             "A clustering method called K-Means then grouped neighborhoods with similar mixes into three profiles. "
             "Hardship and weather were never used to build the groups; they were brought in afterwards to see "
             "whether the profiles connect to them. Nothing on this site predicts future crime.")

    st.markdown("#### Where the data comes from")
    st.markdown(
        "- **Crime:** City of Chicago Data Portal, *Crimes, 2001 to Present*, filtered to 2020 to 2025 and seven crime "
        "types (theft, battery, criminal damage, assault, motor vehicle theft, robbery, burglary). "
        "[data.cityofchicago.org](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)\n"
        "- **Weather:** NOAA National Centers for Environmental Information, daily summaries for Chicago O'Hare "
        "airport. [ncei.noaa.gov](https://www.ncei.noaa.gov/cdo-web/)\n"
        "- **Hardship:** Great Cities Institute, University of Illinois Chicago, Hardship Index from 2019 to 2023 "
        "survey estimates. [greatcities.uic.edu](https://greatcities.uic.edu/)\n"
        "- **Population and neighborhood centres:** Chicago Health Atlas. "
        "[chicagohealthatlas.org](https://chicagohealthatlas.org/)")

    st.markdown("#### What to keep in mind")
    st.markdown(
        "- **Reported crime is not all crime.** Some crimes are reported more than others, and reporting and "
        "policing differ between neighborhoods.\n"
        "- **Population counts are older** (2011 to 2015) than the crime data, so per resident figures are "
        "approximate.\n"
        "- **Busy places look busier.** Rates are per resident, so areas with many visitors, like the Loop, "
        "look higher than they feel.\n"
        "- **One weather station** at O'Hare stands in for the whole city.\n"
        "- **Patterns, not causes.** Links with hardship and weather describe what goes together, not what "
        "causes what.\n"
        "- **Not a safety rating.** A theft heavy area is not automatically safe, and a violence heavy area is "
        "not automatically dangerous for a visitor.")


# --------------------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------------------
PAGES = {
    "home": st.Page(page_home, title="Home", icon="🏙️", default=True),
    "neighborhood": st.Page(page_neighborhood, title="Find your neighborhood", icon="🔎", url_path="neighborhood"),
    "map": st.Page(page_map, title="The map", icon="🗺️", url_path="map"),
    "weather": st.Page(page_weather, title="Does weather matter?", icon="🌡️", url_path="weather"),
    "hardship": st.Page(page_hardship, title="Hardship and crime", icon="⚖️", url_path="hardship"),
    "sure": st.Page(page_sure, title="How sure are we?", icon="✅", url_path="how-sure"),
    "about": st.Page(page_about, title="About", icon="ℹ️", url_path="about"),
}

nav = st.navigation(list(PAGES.values()), position="top")
nav.run()
