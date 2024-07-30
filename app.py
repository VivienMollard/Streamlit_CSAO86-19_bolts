import streamlit as st
import forallpeople as si
import plotly.graph_objects as go

import calculations as calc

si.environment('structural')

# SIDEBAR
st.sidebar.title('Common parameters')
st.sidebar.subheader('Bolts properties')
d_F = st.sidebar.number_input('Bolts diameter (mm)', value=12.7)
n_F = st.sidebar.number_input('Number of fasteners (mm)', value=1)
f_ym = st.sidebar.number_input("Bolt's steel Yield strength (MPa)", value=310)
f_um = st.sidebar.number_input("Bolt's steel Ultimate strength (MPa)", value=310)

st.sidebar.subheader('Factors')
K_D = st.sidebar.number_input('Duration factor', value=1.0)
K_SF = st.sidebar.number_input('Service factor', value=1.0)
K_ST = st.sidebar.number_input('Net tension factor', value=1.0)
K_T = st.sidebar.number_input('Treatment factor', value=1.0)


st.sidebar.selectbox('Select', ['', 'B', 'C'])

# MAIN WINDOW - TOP
st.title('TIMBER DESIGN')
st.subheader('Bolted connection design according to CSA O86-14')
st.write('(for now limited to 2 wooden members)')

# MAIN WINDOW - CONTAINER
container1 = st.container(border=True)

with container1:
    st.write("DATA FOR EACH MEMBER")

# MAIN WINDOW - COLUMNS
col1, col2 = st.columns(2)

with col1:
    st.subheader('Member 1')
    t1 = st.number_input('M1 thickness (mm)', value=100)
    h1 = st.number_input('M1 depth (mm)', value=200)
    g1 = st.number_input('M1 wood density(u)', value=0.42)
    teta1 = st.number_input('M1 load angle / grain (deg)', value=0)

with col2:
    st.subheader('Member 2')
    t2 = st.number_input('M2 thickness (mm)', value=100)
    h2 = st.number_input('M2 depth (mm)', value=200)
    g2 = st.number_input('M2 wood density(u)', value=0.42)
    teta2 = st.number_input('M2 load angle / grain (deg)', value=90)


# MAIN WINDOW - CONTAINER
container2 = st.container(border=True)

with container2:
    st.subheader('Calculations details')
    st.write("In progress...")
    
# MAIN WINDOW - CONTAINER
container3 = st.container(border=True)

with container3:
    st.subheader('Results')
    st.write("In progress...")

