import streamlit as st
import forallpeople as si
import plotly.graph_objects as go

import calculations as calc

si.environment('structural')

############################  SIDEBAR  ############################

st.sidebar.title('Common parameters')

# BOLTS PROPERTIES
st.sidebar.subheader('Bolts properties')
d_F = st.sidebar.number_input('Bolts diameter (mm)', value=12.7)
n_F = st.sidebar.number_input('Number of fasteners (mm)', value=1)
f_ym = st.sidebar.number_input("Bolt's steel Yield strength (MPa)", value=310)
f_um = st.sidebar.number_input("Bolt's steel Ultimate strength (MPa)", value=310)
fy = calc.fy_bolt(f_ym, f_um)
st.sidebar.write(f"Mean value for fy (MPa): {fy}")

# FACTORS
st.sidebar.subheader('Factors')
K_D = st.sidebar.number_input('Duration factor', value=1.0)
K_SF = st.sidebar.number_input('Service factor', value=1.0)
K_ST = st.sidebar.number_input('Net tension factor', value=1.0)
K_T = st.sidebar.number_input('Treatment factor', value=1.0)
K = K_D * K_SF * K_ST * K_T
st.sidebar.write(f"Resulting factor K' is: {K}")


st.sidebar.selectbox('Select', ['', 'B', 'C'])

############################  MAIN WINDOW  ############################

# TITLES
st.title('TIMBER DESIGN')
st.subheader('Bolted connection design according to CSA O86-14')
st.write('(for now limited to 2 wooden members)')

# IMAGES
with st.container(border=True):
    st.write("********   IMAGES TO ADD HERE   **********")

# INPUTS FOR EACH MEMBER
with st.expander("INPUTS FOR EACH MEMBER"):
    col11, col12 = st.columns(2)

    with col11:
        st.subheader('Member 1')
        t_1 = st.number_input('M1 thickness (mm)', value=100)
        h_1 = st.number_input('M1 depth (mm)', value=200)
        g_1 = st.number_input('M1 wood density(u)', value=0.42)
        teta_1 = st.number_input('M1 load angle / grain (deg)', value=0)

    with col12:
        st.subheader('Member 2')
        t_2 = st.number_input('M2 thickness (mm)', value=100)
        h_2 = st.number_input('M2 depth (mm)', value=200)
        g_2 = st.number_input('M2 wood density(u)', value=0.42)
        teta_2 = st.number_input('M2 load angle / grain (deg)', value=90)
    

# CALCULATION DETAILS FOR EACH MEMBER
with st.expander("DETAILED CALCULATIONS FOR EACH MEMBER"):
    col21, col22 = st.columns(2)
    
    with col21:
        st.subheader('Member 1')
        
        st.write("Wood Embedment strength")
        f_1P = calc.f_iP(g_1, d_F)
        f_1Q = calc.f_iQ(g_1, d_F)
        f_1teta = calc.f_iteta(teta1, f_1P, f_1Q, K_D, K_SF, K_T)[1]
        # st.latex(f'f_{{iP}} = {f_1P}*Mpa')
        # st.latex(f'f_{{iQ}} = {f_1Q}*Mpa')
        st.latex(f'f_{{i\\theta}} = {f_1teta}*Mpa')
        
        st.write("Final Fi*")
        f_1 = f_1teta
        st.latex(f'f_1 = {f_1}*Mpa')

    with col22:
        st.subheader('Member 2')
        
        st.write("Wood Embedment strength")
        f_2P = calc.f_iP(g_2, d_F)
        f_2Q = calc.f_iQ(g_2, d_F)
        f_2teta = calc.f_iteta(teta_2, f_2P, f_2Q, K_D, K_SF, K_T)[1]
        # st.latex(f'f_{{iP}} = {f_2P}*Mpa')
        # st.latex(f'f_{{iQ}} = {f_2Q}*Mpa')
        st.latex(f'f_{{i\\theta}} = {f_2teta}*Mpa')
        
        st.write("Final Fi *")
        f_2 = f_2teta
        st.latex(f'f_2 = {f_2}*Mpa')
        
    st.write("Note: Final Fi equals wood embedment strength because steel scenario is not included yet")

    
# CALCULATION DETAILS FOR GLOBAL ASSEMBLY
with st.expander("CALCULATION DETAILS FOR GLOBAL ASSEMBLY"):
    st.write('Details for the global assembly')

    


# RESULTS
with st.expander("RESULTS"):
    st.write('Details for the global assembly')

