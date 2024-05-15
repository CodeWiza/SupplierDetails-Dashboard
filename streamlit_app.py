import streamlit as st
import json
import pycountry

# Set the page configuration
st.set_page_config(page_title="Supplier Analysis", page_icon=":bar_chart:", layout="wide")
st.title("Supplier Discovery")

# Create a text input for the search bar
search_term = st.text_input("", placeholder="🔍 Search for your Suppliers")

# Predefined search options and related categories
search_options = ["Stainless Steel Suppliers", "Safety Gloves Suppliers", "PVC Pipes Suppliers"]
related_categories = {
    "Stainless Steel Suppliers": ["Stainless Steel", "Stainless Steel Bars", "Stainless Steel Rods", "Stainless Steel Plates", "Stainless Steel Rings"],
    "Safety Gloves Suppliers": ["Industrial Gloves", "Disposable Gloves", "Latex Gloves", "Work Gloves", "Leather Gloves"],
    "PVC Pipes Suppliers": ["Furniture Grade PVC Pipe", "Clear PVC Plastic Pipe", "Plastic Pipe", "Aluminium Pipe", "Steel Pipe"]
}

# Filter the data based on the search term
filtered_option = search_term if search_term in search_options else None

# Create checkboxes for selecting recommendation parameters
selected_suppliers = []
with st.expander(label="Select Recommendation Parameters", expanded=True):
    cols = st.columns([1, 1, 1])
    cols[0].write("Financial health")
    cols[1].write("Reviews")
    cols[2].write("Legal Issues")

    # Financial health checkboxes
    cols = st.columns([1, 1, 1])
    stable_checkbox = cols[0].checkbox("Stable")
    growing_checkbox = cols[0].checkbox("Growing")

    # Reviews checkboxes
    three_and_above_checkbox = cols[1].checkbox("3 and above")
    four_and_above_checkbox = cols[1].checkbox("4 and above")

    # Legal Issues checkboxes
    no_financial_wrongdoing_checkbox = cols[2].checkbox("No financial wrongdoing")
    no_board_member_issues_checkbox = cols[2].checkbox("No Board Member issues")

# Display the logo in the sidebar
st.sidebar.image("https://raw.githubusercontent.com/CodeWiza/PriceBenchmarking-Dashboard/main/logo.png", use_column_width=True)

# Load JSON files
with open('C:\Devanshi_Padhy_New\My Projects\EaseworkAI\Supply Chain Dashboard\\1.json', 'r') as f:
    data1 = json.load(f)

with open('C:\Devanshi_Padhy_New\My Projects\EaseworkAI\Supply Chain Dashboard\\2.json', 'r') as f:
    data2 = json.load(f)

with open('C:\Devanshi_Padhy_New\My Projects\EaseworkAI\Supply Chain Dashboard\\3.json', 'r') as f:
    data3 = json.load(f)

# Streamlit app
st.subheader("Stainless Steel Suppliers")

# Sidebar for location filters
with st.sidebar:
    st.subheader("Location Filters")
    location_filter_type = st.radio("Select Location Filter Type", ["By Country/State", "By Zip Code"])

    if location_filter_type == "By Country/State":
        # Get a list of country names
        country_names = [country.name for country in pycountry.countries]

        selected_countries = st.sidebar.multiselect("Select Country", country_names)

        if selected_countries:
            state_options = []
            for country_name in selected_countries:
                country_code = pycountry.countries.get(name=country_name).alpha_2
                states = pycountry.subdivisions.get(country_code=country_code)
                state_names = [state.name for state in states]
                state_options.extend(state_names)

            state_province = st.sidebar.multiselect("Select State/Province", state_options)

    else:
        located_within = st.multiselect("Located Within", ["50 Miles", "100 Miles", "200 Miles"])
        zip_code = st.text_input("Enter Zip Code")

    if filtered_option:
        st.subheader("Related Categories")
        selected_categories = st.multiselect("Select Related Categories", related_categories[filtered_option])

    st.subheader("Company Type")
    company_type_options = ["Manufacturer", "Custom Manufacturer", "Distributor", "Service Company", "Manufacturers' Rep", "Finishing Service Company"]
    selected_company_types = st.multiselect("Select Company Types", company_type_options)

    st.subheader("Quality Certifications")
    quality_certifications_options = ["AISC", "API Spec Q1", "ASME BPVC", "QS 9000", "EN ISO 13485:2012", "CSA W47.1", "Pressure Equipment Directive (2014/68/EU)", "IATF 16949:2016", "ISO 45001:2018"]
    selected_quality_certifications = st.multiselect("Select Quality Certifications", quality_certifications_options)

# Main content
# Display data from the first JSON file
col1, col2 = st.columns(2)
with col1.expander(label="**Introduction of Product**", expanded=True):
    st.write(data1["1.Introducation of product"])

with col2.expander(label="**Overview of Product**", expanded=True):
    st.write(data1["2.Overview of product"])

with col2.expander("**Conclusion**", expanded=True):
    st.write(data1["4.Conculsion"])

with col1.expander(label="**References**", expanded=True):
    reference_links = data1["5.Reference"].split(", ")
    reference_links = [link.split(": ")[1] if ": " in link else link for link in reference_links]

    table_rows = ""
    for link in reference_links:
        description = link.split("//")[1].split("/")[0]
        table_rows += f"<tr><td><a href='{link}' target='_blank'>{link}</a></td><td>{description}</td></tr>"

    st.markdown("""
        <details>
        <summary>Show References in Table</summary>
        <div style="overflow-x: auto;">
            <table style="width:100%;">
                <tr>
                    <th>Link</th>
                    <th>Description</th>
                </tr>
                {table_rows}
            </table>
        </div>
        </details>
        """.format(table_rows=table_rows), unsafe_allow_html=True)

# Create checkboxes for selecting suppliers
selected_suppliers = []
with st.expander(label="Select your supplier", expanded=True):
    cols = st.columns([1, 3, 1.5, 1.5, 2])  # Adjusted column widths
    cols[0].write("Select")
    cols[1].write("Supplier Name")
    cols[2].write("Country")
    cols[3].write("City")
    cols[4].write("Invitation")

    for supplier in data1["3.Top suppliers in Russia"]:
        cols = st.columns([1, 3, 1.5, 1.5, 2])  # Adjusted column widths
        checkbox_value = cols[0].checkbox("", key=supplier["Company_name"])
        cols[1].write(supplier["Company_name"])
        cols[2].write(supplier["company_country"])
        cols[3].write(supplier.get("city", "-"))
        invitation_button = cols[4].button("Send Invite", key=f"invite_{supplier['Company_name']}")

        if checkbox_value:
            selected_suppliers.append(supplier)

        # Display a success message when the "Send Invite" button is clicked
        if invitation_button:
            st.success(f"Invitation sent to {supplier['Company_name']}")

# Function to generate recommendation based on supplier and data2
def generate_recommendation(supplier, data2):
    recommendation = {
        "Company": supplier["Company_name"],
        "Why the recommendation": "",
        "Positives": [],
        "Key Concerns": []
    }

    positives = data2.get("Positives", {})
    if positives:
        recommendation["Positives"] = list(positives.values())

    concerns = data2.get("Key Concerns", {})
    if concerns:
        recommendation["Key Concerns"] = list(concerns.values())

    return recommendation

# If no supplier is selected, display a message
if not selected_suppliers:
    st.write("Please select at least one supplier.")
else:
    # Create tabs for each selected supplier
    tab_labels = [f"{supplier['Company_name']}" for supplier in selected_suppliers]
    try:
        variable_names = st.tabs(tab_labels)
        for i, tab_name in enumerate(variable_names):
            with tab_name:
                supplier = selected_suppliers[i]

                # Display supplier summary and details
                col1, col2 = st.columns(2)
                with col1.expander(label="**Company Summary**", expanded=True):
                    st.write(f"{supplier['summary']}")

                with col2.expander(label="**Company Details**", expanded=True):
                    st.write(f"**Company Name:** {supplier['Company_name']}")
                    st.write(f"**Website:** {supplier['Company_websitelink']}")
                    st.write(f"**Country:** {supplier['company_country']}")
                    if "product offerings" in supplier:
                        st.write(f"**Product Offerings:** {supplier['product offerings']}")
                    if "reviews" in supplier:
                        st.write(f"**Reviews:** {supplier['reviews']}")
                    if "Email" in supplier:
                        st.write(f"**Email:** {supplier['Email']}")
                    if "Phone_number" in supplier:
                        st.write(f"**Phone Number:** {supplier['Phone_number']}")

                with col1.expander(label="**Financial Summary**", expanded=True):
                    st.write(data2["Financial_highlights"])

                # Display legal issues from the third JSON file
                with col2.expander(label="**News**", expanded=True):
                    supplier_data = data3.get(supplier["Company_name"], {})
                    st.markdown(":grey[**Legal Issues**]")
                    st.write(supplier_data.get("**Legal Issues**", "No legal issues reported."))
                    st.markdown(":grey[**Financial Wrongdoing**]")
                    st.write(supplier_data.get("Financial Wrongdoing", "No financial wrongdoings reported."))
                    st.markdown(":grey[**Labor Strike**]")
                    st.write(supplier_data.get("Labour Strike", "No labor strikes reported."))

                with col1.expander(label="**Board Members**", expanded=True):
                    for member in supplier_data.get("Board Members", []):
                        st.write(f"- {member}")

                with col1.expander(label="**Issues with Board Members**", expanded=True):
                    st.write(supplier_data.get("Issues with Board Members", "No issues reported."))

                # Display recommendations
                with st.expander(label="Recommendations", expanded=True):
                    recommendation = generate_recommendation(supplier, data2)
                    st.write(f"**Company:** {recommendation['Company']}")

                    if recommendation["Why the recommendation"]:
                        st.write(f"**Why the recommendation:** {recommendation['Why the recommendation']}")
                    else:
                        st.write("**Why the recommendation:** No specific recommendation reason available.")

                    if recommendation['Positives']:
                        st.write("**Positives:**")
                        for positive in recommendation['Positives']:
                            st.write(f"- {positive}")
                    else:
                        st.write("**Positives:** No positives available.")

                    if recommendation['Key Concerns']:
                        st.write("**Key Concerns:**")
                        for concern in recommendation['Key Concerns']:
                            st.write(f"- {concern}")
                    else:
                        st.write("**Key Concerns:** No key concerns available.")

    except StreamlitAPIException:
        st.write("")
                

