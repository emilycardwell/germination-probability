import streamlit as st
from htbuilder import HtmlElement, div, hr, a, p, styles
from htbuilder.units import percent, px
import math

@st.cache_data
def get_seed_count(p, k, confidence):

    def calc_seeds(p, k, confidence):
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
        return inv_prob, seeds

    if k > 250:
        mult = k//250
        rem = k % 250
        k_prob, k_seeds = calc_seeds(p, 250, confidence)
        r_prob, r_seeds = calc_seeds(p, rem, confidence)
        f_seeds = (k_seeds * mult) + r_seeds
        f_prob = min(k_prob, r_prob)
        return f_prob, f_seeds
    else:
        return calc_seeds(p, k, confidence)

def body():
    # Background
    st.html(
        """
        <style>
            .stApp {
                background-image: url(https://i.postimg.cc/jdsrt0B8/app-background-opaque.png);
                background-size: cover;
            }

            h1 {
                text-align: center;
                font-size: 42px;
                font-weight:600;
            }

            h2 {
                text-align: center;
                font-size: 18px;
                font-style: italic;
                font-weight:300;
                line-height: 1.0;
                color: darkgreen;
            }

            h3 {
                font-size: 18px;
                line-height: 1.2;
                font-weight:400;
            }

            body {
                font-size: 14px;
                line-height: 1.0;
                color: darkgreen;
            }
        </style>
        """
    )

    # Title & Subtitle
    st.html(
        '''
        <h1>Germination Calculator</h1>
        <h2>Calculate the number of seeds you should sow for X number of seedlings</h2>
        <br>
        '''
    )

    # intput seedlings
    row1 = st.columns([0.7, 0.1, 0.2])

    with row1[0]:
        prompt1 = '''
            <h3>Enter the number of seedlings you want</h3>
            '''
        st.html(prompt1)
        with row1[2]:
            st.markdown('')
            desired_plants = st.number_input('Enter the number of seedlings you want',
                                            min_value=1, max_value=10000, value=10,
                                            label_visibility='collapsed')

    st.markdown('######')

    # input germination rate
    row2 = st.columns([0.7, 0.1, 0.2])
    with row2[0]:
        prompt2 = '''
            <h3>Enter the germination rate of the seeds (60% = 0.6)</h3>
            '''
        st.html(prompt2)
        with row2[2]:
            st.markdown('')
            germination_rate = st.number_input('Enter the germination rate of the seeds',
                                            min_value=0.1, max_value=1.0, value=0.6,
                                            label_visibility='collapsed')

    st.markdown('######')

    # input confidence interval
    row3 = st.columns([0.7, 0.1, 0.2])
    with row3[0]:
        prompt3 = '''
            <h3>Enter the minimum confidence interval (95% recommended)</h3>
            '''
        st.html(prompt3)
        with row3[2]:
            st.markdown('')
            confidence_interval = st.number_input('Enter the confidence interval',
                                                min_value=0.50, max_value=0.99, value=0.95,
                                                label_visibility='collapsed')

    st.markdown('###')

    if st.button("Get your estimated number of seeds to plant"):
        try:
            final_probability, seeds = get_seed_count(germination_rate, desired_plants, confidence_interval)

            response_row = st.columns([0.7, 0.3])
            with response_row[0]:
                response1 = f'''
                    <h3 style="
                        color: green;
                        font-size: 17px;
                        font-weight: 500;
                        line-height: 2.0;">
                    To have a {round(final_probability*100, 2)}% chance of getting \
                    {desired_plants} seedlings, you should plant:
                    </h3>
                    '''
                st.html(response1)
                with response_row[1]:
                    response2 = f'''
                        <p style="
                            color: darkred;
                            background-color: white;
                            border: 1px solid black;
                            line-height: 2.0;
                            font-size: 24px;
                            text-align: center;">
                        {seeds} seeds
                        </p>
                        '''
                    st.html(response2)

        except:
            st.html(
                '''
                <body>An unknown error occurred. Check parameters.<body>
                <body>If the error persists, please make an issue <body>\
                <a href="https://github.com/emilycardwell/germination-probability/issues">here</a>
                '''
            )

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

    st.html(style)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.html(str(foot))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def footer():
    myargs = [
        "Created by Emily Cardwell  |  ",
        link("https://emilycardwell.com", "emilycardwell.com"),
    ]
    layout(*myargs)


if __name__ == "__main__":
    body()
    footer()
