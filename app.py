import streamlit as st
import streamlit_folium as st_folium
from streamlit_option_menu import option_menu
from Laadpalen import (map_plot, laadpalen_filtered2, laadpalen_filtered1, province_colors, 
                       histogram_contime, data_laadpaaltijd, auto_per_maand, energy_plot, corr_plot, 
                       train_model, start_end_time)

# Custom CSS for enhanced theming and professional look
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');

    /* Background of the main app container */
    .reportview-container {
        background-color: #f4f4f9;
        padding: 10px;
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 10px;
    }

    /* Main title styling */
    h1 {
        font-family: 'Lato', sans-serif;
        color: #2c3e50;
        font-weight: 700;
        text-align: center;
        font-size: 42px;
        margin-bottom: 25px;
    }

    /* Section Header styling */
    h2, h3 {
        font-family: 'Lato', sans-serif;
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 10px;
        font-size: 30px;
    }

    /* Styling for paragraph and content */
    p, .element-container {
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        line-height: 1.6;
        color: #34495e;
        padding: 10px;
    }

    /* Styling the box and correlation matrices headers */
    .header-style {
        font-size: 24px;
        color: #2c3e50;
        font-weight: 600;
        margin-top: 40px;
        margin-bottom: 20px;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 14px;
        color: #7f8c8d;
        border-top: 1px solid #dcdcdc;
        margin-top: 50px;
    }

    /* Hover effect for interactive elements */
    .element-container:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: 0.3s ease;
    }

    /* Add padding for better text readability */
    .element-container {
        padding: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with improved navigation using option_menu
with st.sidebar:
    page = option_menu(
        menu_title="Navigation",
        options=["Car Registrations", "Charging Times & Energy", "Charging Stations Map"],
        icons=["car", "battery", "map"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#2c3e50", "color": "white"},
        }
    )

# Page 1: Car Registrations Section
if page == "Car Registrations":
    st.markdown("<h1>Laadpalen Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("""<div class='element-container'>
                   Welcome to the Laadpalen Dashboard. This dashboard displays an interactive map of charging stations 
                   in the Netherlands. Use the filters below to explore different locations and insights.
                   </div>""", unsafe_allow_html=True)
    
    # Car Registrations Section
    st.markdown("<h2 class='header-style'>Car Registrations per Month</h2>", unsafe_allow_html=True)
    st.markdown("Cumulatief aantal autos’s per brandstofsoort van 2022-01 tot 2024-10.")
    
    auto_per_maand()
    
    # Correlation Plot Section
    st.markdown("<h2 class='header-style'>Correlation Plot</h2>", unsafe_allow_html=True)
    st.markdown("The correlation matrix presents the degree of correlation between certain selected variables.")
    st.write(corr_plot())
    
    # Actual vs Predicted catalogusprijs for the training set
    st.markdown("<h2 class='header-style'>Actual vs Predicted catalogusprijs</h2>", unsafe_allow_html=True)
    st.markdown("This chart shows the relative density in a histogram, showing the actual and the predicted list prices using overlaid bars.")
    train_model()

# Page 2: Charging Times & Energy
elif page == "Charging Times & Energy":
    st.markdown("<h1>Charging Times & Energy Analysis</h1>", unsafe_allow_html=True)

    # Create columns for better layout
    col3, col4 = st.columns(2)

    with col3:
        # Histogram of Charging Times
        st.markdown("<h2 class='header-style'>Histogram of Charging Times</h2>", unsafe_allow_html=True)
        st.markdown("Histogram displaying the frequency of certain charging durations.")
        histogram_contime(data_laadpaaltijd)

    with col4:
        # Energy Plot
        st.markdown("<h2 class='header-style'>Energy Plot</h2>", unsafe_allow_html=True)
        st.markdown("Line chart illustrating total and wasted energy on a weekly and monthly basis.")
        fig = energy_plot(data_laadpaaltijd)
        st.plotly_chart(fig)

    # Start and end time details
    st.markdown("The histogram below shows the distribution of start and end times of cars connecting to charging stations.")
    start_end_time()

# Page 3: Charging Stations Map
elif page == "Charging Stations Map":
    st.markdown("<h1>Charging Stations Map</h1>", unsafe_allow_html=True)
    st.markdown("An interactive map displaying the charging stations in different provinces of the Netherlands.")

    # List of provinces for dropdown selection
    st.markdown("<h2 class='header-style'>Charging Stations Map</h2>", unsafe_allow_html=True)
    province_options = sorted(laadpalen_filtered2['Province'].astype(str).unique())
    selected_province = st.selectbox('Select a Province', province_options)

    # Call the map_plot function with the selected province
    laadpalen_map = map_plot(selected_province)  

    # Display the map using streamlit_folium
    st_folium.st_folium(laadpalen_map, width=800, height=600)  # Adjusted map size

# Footer section
st.markdown(
    """
    <div class="footer">
        <p>© 2024 Laadpalen Dashboard | Data provided by RDW</p>
    </div>
    """,
    unsafe_allow_html=True
)
