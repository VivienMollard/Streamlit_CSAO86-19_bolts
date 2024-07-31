import streamlit as st
import forallpeople as si
import plotly.graph_objects as go
from handcalcs.decorator import handcalc

import calculations as calc

si.environment('structural')

############################  SIDEBAR  ############################

st.sidebar.title('Common parameters')

# Checkbox to enable calculation and graph display
calculate_graph = st.sidebar.checkbox('Display Comparison Graph (takes few seconds)', value=False)
st.sidebar.write('')

# CONFIGURATION
st.sidebar.subheader('Configuration of the connection')
n_s = st.sidebar.number_input('Number of shear planes (u)', value=1, min_value=1, max_value=2)

# BOLTS PROPERTIES
st.sidebar.subheader('Bolts properties')
d_F = st.sidebar.number_input('Bolts diameter (mm)', value=12.7)
n_F = st.sidebar.number_input('Number of fasteners (mm)', value=1)
f_ym = st.sidebar.number_input("Bolt's steel Yield strength (MPa)", value=310)
f_um = st.sidebar.number_input("Bolt's steel Ultimate strength (MPa)", value=310)
f_y = calc.fy_bolt(f_ym, f_um)
st.sidebar.write(f"Mean value for fy (MPa): {f_y}")

# FACTORS
st.sidebar.subheader('Factors')
K_D = st.sidebar.number_input('Duration factor', value=1.0)
K_SF = st.sidebar.number_input('Service factor', value=1.0)
K_ST = st.sidebar.number_input('Net tension factor', value=1.0)
K_T = st.sidebar.number_input('Treatment factor', value=1.0)
K = K_D * K_SF * K_ST * K_T
st.sidebar.write(f"Resulting factor K' is: {K}")

# st.sidebar.selectbox('Test', ['A', 'B', 'C'])

############################  MAIN WINDOW  ############################

# TITLES
st.title('TIMBER DESIGN')
st.subheader('Bolted connection design according to CSA O86-14')
st.write('(for now limited to 2 wooden members)')


# IMAGES
with st.container(border=True):
    st.write("********   IMAGES TO ADD HERE   **********")
    

# SUM-UP
with st.container(border=True):
    top_placeholder_1 = st.empty()
    top_placeholder_2 = st.empty()
    top_placeholder_3 = st.empty()
    top_placeholder_4 = st.empty()


# INPUTS FOR EACH MEMBER
with st.expander("INPUTS FOR EACH MEMBER"):
    col11, col12 = st.columns(2)

    with col11:
        st.subheader('Member 1')
        t_1 = st.number_input('M1 thickness (mm)', value=100)
        h_1 = st.number_input('M1 depth (mm)', value=200)
        g_1 = st.number_input('M1 wood density(u)', value=0.42)
        teta_1 = st.slider('M1 load angle / grain (deg)', value=0, min_value=0, max_value=90)

    with col12:
        st.subheader('Member 2')
        t_2 = st.number_input('M2 thickness (mm)', value=100)
        h_2 = st.number_input('M2 depth (mm)', value=200)
        g_2 = st.number_input('M2 wood density(u)', value=0.42)
        teta_2 = st.slider('M2 load angle / grain (deg)', value=0, min_value=0, max_value=90)
    

# CALCULATION DETAILS FOR EACH MEMBER
with st.expander("DETAILED CALCULATIONS FOR EACH MEMBER"):
    col21, col22 = st.columns(2)
    
    with col21:
        st.subheader('Member 1')
        
        st.write("Wood Embedment strength")
        f_1P = calc.f_iP(g_1, d_F)
        f_1Q = calc.f_iQ(g_1, d_F)
        f_1teta = calc.f_iteta(teta_1, f_1P, f_1Q, K_D, K_SF, K_T)[1]
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
  
# CALCULATION DETAILS FOR YIELDING OF THE CONNECTION

with st.expander("CALCULATION DETAILS FOR YIELDING OF THE CONNECTION"):

    # Résulats unit yielding
    results = calc.n_u(n_s, t_1, t_2, f_1, f_2, f_y, d_F)
    n_u_latex = results[0]
    n_u_value = results[1][0]
    n_u_allValues = results[1][1]
    n_ua, n_ub, n_uc, n_ud, n_ue, n_uf, n_ug = n_u_allValues
    # Résulats yielding
    phi_y = 0.8
    N_r_latex, N_r_value  = calc.N_r(n_u_value, n_s, n_F, phi_y)
    
    # st.latex(f'n_{{u}}= {n_u_value}')
    # st.latex(f'n_{{s}}= {n_s}')
    # st.latex(f'\\phi_y = {phi_y}')
    st.latex(N_r_latex)
    
    # Mise à jour de l'espace réservé en haut de la page
    top_placeholder_1.markdown(f"- Yielding Resistance $N_r = {N_r_value*1E-3:.2f}$ kN", unsafe_allow_html=True)
    top_placeholder_2.markdown(f"- Row Shear Resistance $PR_r = $ not included yet", unsafe_allow_html=True)
    top_placeholder_3.markdown(f"- Yielding Resistance $PG_r = $ not included yet", unsafe_allow_html=True)
    top_placeholder_4.markdown(f"- Yielding Resistance $QS_r = $ not included yet", unsafe_allow_html=True)

    st.write("=================== Details per mode ======================== ")
    st.write("") 
    st.write("Mode a:")
    st.latex(f'n_{{ua}} = {(n_ua)}')
    st.write("Mode b:")
    st.latex(f'n_{{ub}}= {n_ub}')
    st.write("Mode c:")
    st.latex(f'n_{{uc}} = {n_uc}')
    st.write("Mode d:")
    st.latex(f'n_{{ud}} = {n_ud}')
    st.write("Mode e:")
    st.latex(f'n_{{ue}} = {n_ue}')
    st.write("Mode f:")
    st.latex(f'n_{{uf}} = {n_uf}')
    st.write("Mode g:")
    st.latex(f'n_{{ug}}= {n_ug}')
    st.write("") 
    
    st.write("================  Detailed substitutions ====================")
    st.latex(f'n_u = {n_u_latex}')

# COMPARISON FOR DIFFERENT DIAMETERS
with st.expander("COMPARISON FOR DIFFERENT DIAMETERS"):
    

    
    if calculate_graph:
        diameters, Nr_for_diameters= calc.calculate_Nr_for_diameters(n_s, n_F, t_1, t_2, f_y, teta_1, teta_2, g_1, g_2)
        
        # Plot lines and bars (GRAPH)
        fig = go.Figure()

        # Add line plot
        fig.add_trace(go.Scatter(x=diameters, y=Nr_for_diameters, mode='lines+markers', name='N_r vs Diameter', line=dict(color='red')))

        # Add bar plot
        fig.add_trace(go.Bar(x=diameters, y=Nr_for_diameters, name='N_r vs Diameter', marker=dict(color='lightblue'), width=0.8))

        # Update layout
        fig.update_layout(
            title='Factored Yield strength depending on bolt diameter',
            xaxis_title='Bolts diameter d_f (mm)',
            yaxis_title='Factored Yield strength N_r (N)',
        )

        st.plotly_chart(fig)
                
        # Values (List of list)
        st.write(diameters)
        st.write(Nr_for_diameters)
