import streamlit as st
import math
from htbuilder import HtmlElement, div, hr, a, p, styles
from htbuilder.units import percent, px


# Title & Subtitle
title = '<p style="font-size: 42px">Germination Calculator</p>'
subtitle = '<p style="font-size: 24px, color:#3e4a41''">caculate the number of seeds needed for your garden</p>'
st.markdown(title, unsafe_allow_html=True)
st.markdown(subtitle, unsafe_allow_html=True)

# setup columns to make input boxes smaller
row_input = st.columns([0.5, 0.5])

# input
with row_input[0]:
    desired_plants = st.number_input('Enter the number of seedlings you want', min_value=1, max_value=1000, value=1)

prompt1 = '<p style="font-size: 10px, color:#c4c4c4">Any numbers larger than 250 will take exponentially longer to compute</p>'
st.markdown(prompt1, unsafe_allow_html=True)


with row_input[0]:
    germination_rate = st.number_input('Enter the germination rate of the seeds', min_value=0.0, max_value=1.0, value=0.6)

prompt2_1 = '<p style="font-size: 18px, color:Grey">If 60%, enter 0.60</p>'
st.markdown(prompt2_1, unsafe_allow_html=True)


with row_input[0]:
    confidence_interval = st.number_input('Enter the confidence interval', min_value=0.0, max_value=1.0, value=0.95)

prompt3_1 = '<p style="font-size: 18px, color:Gray">Recommended: 95%, the closer to 100%, the slower you will get your result.</p>'
st.markdown(prompt3_1, unsafe_allow_html=True)


@st.cache_data
def get_seed_count(p, k, confidence):
    n = int(k / p)

    inv_prob = 0
    while inv_prob < confidence:
        cum_prob = 0
        for i in range(k):
            log_a = math.log(math.comb(n, i))
            log_b = i * math.log(p)
            log_c = (n-i) * math.log(1-p)
            log_prob = log_a + log_b + log_c
            if log_prob < -100:
                prob = 0
            else:
                prob = math.exp(log_prob)
            cum_prob += prob

        inv_prob = 1 - cum_prob
        n += 1

    seeds = n - 1
    final_probability = round(inv_prob, 4)

    return seeds, final_probability

if st.button("Get your estimated number of seeds to plant"):
    seeds, final_probability = get_seed_count(germination_rate, desired_plants, confidence_interval)
    st.write(f"You should plant {seeds} seeds to have a {final_probability*100}% chance of getting {desired_plants} seedlings.")


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def footer():
    myargs = [
        "Created by Emily Cardwell  |  ",
        link("https://emilycardwell.com", "emilycardwell.com"),
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer()
