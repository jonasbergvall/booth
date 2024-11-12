import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import json
import os

# Load mission statements from JSON file
def load_mission_statements():
    with open('data/mission_statements.json', 'r') as f:
        return json.load(f)

mission_statements_data = load_mission_statements()

# Function to get the brand name based on the selected industry
def get_brand_name(industry):
    for ind in mission_statements_data["industries"]:
        if ind["name"] == industry:
            return ind["brand"]
    return "Brand not found"

# Logo display
logo = '''
<div style="text-align: right; margin-bottom: 20px;">
    <img src="https://bestofworlds.se/img/BoWlogo.png" width="150px">
</div>
'''
st.markdown(logo, unsafe_allow_html=True)

# Function to get the mission statement based on industry, sustainability, and archetype
def get_mission_statement(industry, sustainability, archetype):
    for ind in mission_statements_data["industries"]:
        if ind["name"] == industry:
            return ind["sustainability"].get(sustainability, {}).get(archetype, "Mission statement not found.")
    return "Select an industry, sustainability differentiator, and archetype to see the mission statement."

# Function to get the corresponding image based on sustainability and archetype
def get_mirror_image(sustainability, archetype):
    if sustainability != "Select..." and archetype != "Select...":
        image_folder = sustainability
        image_filename = f"{sustainability[:4]}{archetype}.webp"
        image_path = os.path.join('images', image_folder, image_filename)
        
        if os.path.exists(image_path):
            return Image.open(image_path)
        else:
            st.warning(f"Image not found at path: {image_path}")
            return Image.open('images/booth_exterior.png')  # Return default image
    
    return Image.open('images/booth_exterior.png')  # Return default image if selections are invalid

# Function to round corners of an image
def round_corners(image, radius):
    # Create mask for rounded corners
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
    
    # Apply the mask to the image to round corners
    result = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)
    
    return result

# Main layout and app settings
st.title("Brand Dressing Room")

st.write(
    """
    Welcome to the Brand Personality Dressing Room. This tool is designed to inspire you to explore how sustainability 
    can be integrated into your brand’s personality. Whether you lead with environmental stewardship, champion social responsibility, 
    innovate with technology, or embrace circular economy practices, discover the unique ways sustainability can shape your brand's identity.
    """
)

st.subheader("Select Your Preferences")

# Adjust the layout for dropdown menus
col1, col2, col3 = st.columns(3)

with col1:
    selected_industry = st.selectbox("Select Industry", ["Select..."] + [ind["name"] for ind in mission_statements_data["industries"]], key="industry")
with col2:
    selected_sustainability = st.selectbox("Sustainability Differentiator", ["Select...", "Environmental", "Social", "Innovation", "Circular Economy"], key="sustainability")
with col3:
    archetype_mapping = {
        "Market Leader": "King",
        "Challenger": "Warrior",
        "Innovator": "Magician",
        "Idealist": "Lover"
    }
    archetype_friendly = st.selectbox("Brand Archetype", ["Select...", "Market Leader", "Challenger", "Innovator", "Idealist"], key="archetype_friendly")
    selected_archetype = archetype_mapping.get(archetype_friendly, "Select...")

# Add a container for the layout
col1, col2 = st.columns([2, 1])

# Display the image across the first two-thirds of the space
mirror_image = get_mirror_image(selected_sustainability, selected_archetype)
with col1:
    # Round the image corners with a fixed radius (e.g., 50px)
    rounded_image = round_corners(mirror_image, radius=50)
    st.image(rounded_image, caption=f"Dressing Room", use_column_width=True)

# Custom CSS for rounded corners of the mission box
st.markdown(
    """
    <style>
    .mission-box {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 15px; /* Rounded corners for mission box */
        background-color: #f9f9f9;
        height: 462px; /* Set to match the expected height of the image */
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display the mission statement in the remaining one-third
with col2:
    if selected_industry != "Select..." and selected_sustainability != "Select..." and selected_archetype != "Select...":
        mission_statement = get_mission_statement(
            selected_industry, 
            selected_sustainability, 
            selected_archetype
        )
        brand_name = get_brand_name(selected_industry)
        st.markdown(f"""
        <div class="mission-box">
            <div>
                <h3>{brand_name}</h3>
                <p>{mission_statement}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display placeholder message inside the mission box for consistency
        st.markdown("""
        <div class="mission-box">
            <div>
                <p>Select an industry, sustainability differentiator, and archetype to see the mission statement.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
