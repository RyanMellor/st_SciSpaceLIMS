import streamlit as st

from helpers import sci_setup

sci_setup.setup_page("SciSpace LIMS")
sci_setup.connect_google_sheets('SciSpaceLIMS', st.secrets["gcp_service_account"])

    
# PAGES = {
#     'ELN Integration': electronic_lab_notebook,
#     'Data Management': data_management,
#     'Standard Operating Procedures': standard_operating_procedures,
#     'Quality Management System': quality_management_system,
#     'Inventory Management': inventory_management,
#     'Integration and Interoperability': integration_interoperability,
#     'Reporting and Analytics': reporting_analytics,
#     'Regulatory Compliance': regulatory_compliance,
#     'Security and Audit Trails': security_audit_trails,
#     'Chain of Custody': chain_of_custody,
# }

def main():

    # st.sidebar.markdown("""
    # <u>L</u>aboratory  
    # <u>I</u>nformation  
    # <u>M</u>anagement  
    # <u>S</u>ystem
    # """,
    # unsafe_allow_html=True)

    pass

if __name__ == '__main__':
    main()
