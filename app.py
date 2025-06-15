import streamlit as st
from airbnb_predict import AirbnbPricePredictor  # Import your class

# Page config
st.set_page_config(
    page_title="Airbnb Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match the HTML design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        max-width: 800px;
        margin: 1rem auto;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        padding: 0 !important;
    }
    
    .st-emotion-cache-zy6yx3{
        padding-top: 1rem;
        padding-right: 5rem;
        padding-bottom: 5rem;
        padding-left: 5rem;
    }
    
    /* Header section */
    .header-container {
        background: linear-gradient(135deg, #ff416c, #ff4757);
        color: white;
        padding: 30px;
        text-align: center;
        border-radius: 20px 20px 0 0;
        margin: 0 -1rem;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: white !important;
    }
    
    .sub-title {
        font-size: 1.1rem;
        opacity: 0.9;
        color: white !important;
    }
    
    /* Form container */
    .form-container {
        padding: 10px;
        margin: 0 -1rem;
    }
    
    /* Section titles */
    .section-title {
        font-size: 1.3rem;
        color: #333;
        margin-bottom: 15px;
        font-weight: 600;
        border-bottom: 2px solid #ff416c;
        padding-bottom: 5px;
        display: inline-block;
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e1e8ed;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #ff416c;
        box-shadow: 0 0 0 3px rgba(255, 65, 108, 0.1);
    }
    
    .stNumberInput > div > div > input {
        background: white;
        border: 2px solid #e1e8ed;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #ff416c;
        box-shadow: 0 0 0 3px rgba(255, 65, 108, 0.1);
    }
    
    .stTextInput > div > div > input {
        background: white;
        border: 2px solid #e1e8ed;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff416c;
        box-shadow: 0 0 0 3px rgba(255, 65, 108, 0.1);
    }
    
    .st-emotion-cache-br351g {
        font-size: 1.3rem;
    }
            
    /* Button styling */
    .stButton > button {
        width: 100%;
        padding: 15px;
        background: linear-gradient(135deg, #ff416c, #ff4757);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 20px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(255, 65, 108, 0.3);
    }
    
    /* Result styling */
    .result-container {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        margin: 30px 0;
    }
    
    .result-title {
        font-size: 1.5rem;
        margin-bottom: 10px;
        color: white !important;
    }
    
    .price-display {
        font-size: 3rem;
        font-weight: 700;
        margin: 10px 0;
        color: white !important;
    }
    
    .price-subtitle {
        color: white !important;
        opacity: 0.9;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: none;
        border: none;
        color: #ff416c;
        font-size: 1rem;
        text-decoration: underline;
    }
    
    /* Grid layout for form fields */
    .form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 20px;
    }
    
    /* Required field indicator */
    .required-indicator {
        color: #ff416c;
        font-weight: bold;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #ff416c !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 600px) {
        .main-title {
            font-size: 2rem;
        }
        .price-display {
            font-size: 2.5rem;
        }
        .form-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize predictor (cached for performance)
@st.cache_resource
def load_predictor():
    return AirbnbPricePredictor()

# Header
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🏠 Airbnb Price Predictor</h1>
    <p class="sub-title">Get accurate price predictions for your Airbnb listing</p>
</div>
""", unsafe_allow_html=True)

# Form container
st.markdown('<div class="form-container">', unsafe_allow_html=True)

# Required Information Section
st.markdown('<h3 class="section-title">Required Information</h3>', unsafe_allow_html=True)

# Create columns for form layout
col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input(
        "Latitude *",
        value=40.7589,
        format="%.6f",
        help="Property's latitude coordinate",
        key="lat"
    )
    
    neighbourhood_group = st.selectbox(
        "Borough *",
        ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"],
        help="NYC Borough where the property is located",
        key="borough"
    )

with col2:
    longitude = st.number_input(
        "Longitude *", 
        value=-73.9851,
        format="%.6f",
        help="Property's longitude coordinate",
        key="lon"
    )
    
    room_type = st.selectbox(
        "Room Type *",
        ["Entire home/apt", "Private room", "Shared room"],
        help="Type of accommodation",
        key="room"
    )

# Advanced Options
st.markdown('<br>', unsafe_allow_html=True)
with st.expander("+ Show Advanced Options (Optional)", expanded=False):
    st.markdown('<h3 class="section-title">Optional Details</h3>', unsafe_allow_html=True)
    
    adv_col1, adv_col2 = st.columns(2)
    
    with adv_col1:
        neighbourhood = st.text_input(
            "Neighborhood",
            placeholder="e.g., Midtown",
            help="Specific neighborhood name",
            key="neighborhood"
        )
        
        number_of_reviews = st.number_input(
            "Number of Reviews",
            min_value=0,
            value=None,
            help="Total number of reviews",
            key="reviews"
        )
        
        calculated_host_listings_count = st.number_input(
            "Host Listings Count",
            min_value=1,
            value=None,
            help="Number of listings by host",
            key="host_listings"
        )
    
    with adv_col2:
        minimum_nights = st.number_input(
            "Minimum Nights",
            min_value=1,
            value=None,
            help="Minimum nights required for booking",
            key="min_nights"
        )
        
        reviews_per_month = st.number_input(
            "Reviews per Month",
            min_value=0.0,
            value=None,
            step=0.1,
            help="Average reviews per month",
            key="reviews_month"
        )
        
        availability_365 = st.number_input(
            "Days Available per Year",
            min_value=0,
            max_value=365,
            value=None,
            help="Days available for booking per year",
            key="availability"
        )

# Prediction button
if st.button("🔮 Predict Price", key="predict_btn"):
    try:
        # Load predictor
        predictor = load_predictor()
        
        # Make prediction
        with st.spinner("Calculating your Airbnb price..."):
            predicted_price = predictor.predict_price(
                latitude=latitude,
                longitude=longitude,
                neighbourhood_group=neighbourhood_group,
                room_type=room_type,
                neighbourhood=neighbourhood if neighbourhood else None,
                minimum_nights=minimum_nights,
                number_of_reviews=number_of_reviews,
                reviews_per_month=reviews_per_month,
                calculated_host_listings_count=calculated_host_listings_count,
                availability_365=availability_365
            )
        
        # Display result with custom styling
        st.markdown(f"""
        <div class="result-container">
            <h3 class="result-title">Predicted Price</h3>
            <div class="price-display">${predicted_price}</div>
            <p class="price-subtitle">per night</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional success message
        st.success(f"✅ Your predicted nightly rate is ${predicted_price}")
        
        # Show input summary
        with st.expander("📋 Prediction Summary"):
            st.write("**Input Parameters:**")
            summary_text = f"""
            - **Location:** {latitude}, {longitude}
            - **Borough:** {neighbourhood_group}
            - **Room Type:** {room_type}
            """
            
            if neighbourhood:
                summary_text += f"- **Neighborhood:** {neighbourhood}\n"
            if minimum_nights:
                summary_text += f"- **Minimum Nights:** {minimum_nights}\n"
            if number_of_reviews:
                summary_text += f"- **Number of Reviews:** {number_of_reviews}\n"
            if reviews_per_month:
                summary_text += f"- **Reviews per Month:** {reviews_per_month}\n"
            if calculated_host_listings_count:
                summary_text += f"- **Host Listings:** {calculated_host_listings_count}\n"
            if availability_365:
                summary_text += f"- **Available Days:** {availability_365}\n"
                
            st.markdown(summary_text)
                
    except Exception as e:
        st.error(f"❌ Error making prediction: {str(e)}")
        st.info("Please check that your model files are in the correct location and try again.")

# Close form container
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with additional info (styled to match)
with st.sidebar:
    st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("## ℹ️ About")
    st.markdown("""
    This tool predicts Airbnb prices using a trained machine learning model.
    
    **Required files:**
    - `airbnb_gbm_model.pkl`
    - `airbnb_scaler.pkl`
    - `model_metadata.json`
    
    **Tips for better predictions:**
    - Use accurate GPS coordinates
    - Fill in optional fields for more precise results
    - Consider seasonal variations
    """)
    
    st.markdown("## 🗺️ Quick Locations")
    
    if st.button("📍 Times Square", use_container_width=True):
        st.session_state.lat = 40.7580
        st.session_state.lon = -73.9855
        st.rerun()
        
    if st.button("🌉 Brooklyn Bridge", use_container_width=True):
        st.session_state.lat = 40.7061
        st.session_state.lon = -73.9969  
        st.rerun()
        
    if st.button("🌳 Central Park", use_container_width=True):
        st.session_state.lat = 40.7829
        st.session_state.lon = -73.9654
        st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.7); font-size: 0.8rem;">
    Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)