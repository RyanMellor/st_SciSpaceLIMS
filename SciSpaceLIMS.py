import streamlit as st

import pandas as pd
from datetime import datetime
import base64
from io import BytesIO
from collections import defaultdict
from uuid import uuid4
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import json

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, ListStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageTemplate, Frame, Table, TableStyle, ListFlowable, ListItem
from reportlab.platypus.flowables import HRFlowable, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# from pydantic import BaseModel, Field, validator
# from typing import List, Dict

pdf_styles = getSampleStyleSheet()

def quality_management_system():
    st.header('Quality Management System')
    st.caption("""
    The Quality Management System (QMS) is designed to help maintain the high standards of your laboratory.  
    This particular implementation is based on the WHO Laboratory Quality Management System handbook, which can be found [here](https://www.who.int/publications/i/item/9789241548274).  
    Your laboratory should maintain a QMS manual that describes the policies and procedures for your laboratory.  
    Your needs may vary, so you may need to modify the QMS to fit your laboratory.
    """)

    for category in lqms_structure:
        # Create an expander for each category
        with st.expander(category['title']):
            # Display the description for the category
            st.markdown(
                f"""
                <p style='color: gray;'>{category['description']}</p>
                
                ---
                
                """,
                unsafe_allow_html=True,)
            
            # Loop through the subcategories for the category
            for subcategory in category['subcategories']:
                # Display the subcategory name and description
                st.markdown(
                    f"""
                    <b>{subcategory['title']}</b>
                    <p style='color: gray;'>{subcategory['description']}</p>
                    """,
                    unsafe_allow_html=True,)
                
                try:
                    st.markdown(
                    f"""
                    <p style='color: grey; font-size:12px'>Example: </p>
                    <p style='color: cornflowerblue; font-size:12px'>{subcategory['example']}</p>
                    """,
                    unsafe_allow_html=True,)
                except:
                    pass
                
def inventory_management():
    st.header('Inventory Management')
    st.caption("""
    Inventory management is the process of tracking and managing your laboratory inventory. \n
    """)    

    reagents, samples, supplies, equipment = st.tabs(['Reagents', 'Samples', 'Supplies', 'Equipment'])
    
    with reagents:
        manage_inventory("inventory_reagents")

    with samples:
        manage_inventory("inventory_samples")

    with supplies:
        manage_inventory("inventory_supplies")

    with equipment:
        manage_inventory("inventory_equipment")


def manage_inventory(inventory_type):
    abvs = {
        'inventory_reagents': 'RE',
        'inventory_samples': 'SA',
        'inventory_supplies': 'SU',
        'inventory_equipment': 'EQ'
    }

    # Get the Google Sheet
    worksheet = sh.worksheet(inventory_type)

    # Fetch existing data
    df = pd.DataFrame(worksheet.get_all_records())

    # Search
    search_term = st.text_input(f'Search', key=f'{inventory_type}_search')
    # available_applications = list(set(worksheet.col_values(3)))
    # filter_application = st.multiselect('Filter by Application', available_applications, default=available_applications, key=f'{inventory_type}_filter_application')


    # Display existing data
    search_df = df[df.astype(str).apply(lambda x: x.str.contains(search_term, case=False).any(), axis=1)]
    st.dataframe(search_df)

    # add, remove, update = st.tabs(['Add', 'Remove', 'Update'])
    # with add:
    #     new_item = pd.DataFrame().from_dict(
    #         {field['column_name']: None for field in database_structures[inventory_type][1:]}, orient='index').T
    #     new_item = st.experimental_data_editor(new_item)
    #     if st.button('Add Item', key=f'{inventory_type}_add'):
    #         new_item = new_item.to_dict('records')[0]
    #         new_item['id'] = f'{abvs[inventory_type]}-{str(uuid4())[:6]}'

    #         # Append new SOP to the dataframe
    #         df = df.append(new_item, ignore_index=True)

    #         # Save updated dataframe to Google Sheets
    #         set_with_dataframe(worksheet, df)

    #         # Display success message
    #         new_item_name = new_item['name']
    #         st.success(f'Successfully added {new_item_name} to {inventory_type}.')

    # with remove:
    #     remove_id = st.text_input(f'Item ID', key=f'{inventory_type}_remove_id')
    #     if remove_id:
    #         st.dataframe(df[df['id'] == remove_id])
    #         if st.button('Remove Selected Item', key=f'{inventory_type}_remove'):
    #             df = df[df['id'] != remove_id]
    #             worksheet.clear()
    #             worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    #             # set_with_dataframe(worksheet, df)
    #             st.success(f'Successfully removed {remove_id} from {inventory_type}.')
        
    # with update:
    #     update_id = st.text_input(f'Item ID', key=f'{inventory_type}_update_id')
    #     if update_id:
    #         update_item = df[df['id'] == update_id]
    #         update_item = st.experimental_data_editor(update_item, key=f'{inventory_type}_update_item')
    #         if st.button('Update Selected Item', key=f'{inventory_type}_update'):
    #             update_item = update_item.to_dict('records')[0]
    #             df = df[df['id'] != update_id]
    #             df = df.append(update_item, ignore_index=True)
    #             set_with_dataframe(worksheet, df)
    #             st.success(f'Successfully updated {update_id} in {inventory_type}.')


def data_management():
    st.header('Data Management')
    st.caption("""
    Data Management is the process of collecting, storing, and retrieving data in a way that is secure, reliable, and easy to use.
    """)
    st.write("Coming soon")


def standard_operating_procedures():
    st.header('Standard Operating Procedures (SOPs)')

    sop_categories = {
            'Quality Assurance and Control': 'QU',
            'Equipment': 'EQ',
            'Analytical': 'AN',
            'Procedure': 'PR',
            'Safety': 'SA'
        }
        
    # sop_tags = {
    #     'tag_qc_qa': 'QC and QA',
    #     'tag_safety': 'Safety',
    #     'tag_equipment': 'Equipment',
    #     'tag_analytical': 'Analytical',
    #     'tag_documentation': 'Documentation',
    #     'tag_waste': 'Waste',
    #     'tag_training': 'Training',
    #     'tag_chemical': 'Chemical',
    #     'tag_biological': 'Biological',
    # }

    page_description = """
    Standard Operating Procedures (SOPs) are detailed instructions for how to perform a specific task in your laboratory.  
    SOPs should be written for all tasks that are performed in your laboratory.
    Categories of SOPs include:
    """
    for category, code in sop_categories.items():
        page_description+= f'\n * {category}  '

    st.caption(page_description)

    st.warning("SOP database is currently under construction. Everything on this page is subject to change.")

    worksheet = sh.worksheet('sops')

    # Fetch existing data
    df = pd.DataFrame(worksheet.get_all_records())
    df.dropna(how='all', inplace=True)
    df = df[[col for col in df.columns if 'Unnamed' not in col]]

    # Filter options
    filter_term = st.text_input(f'Search', key=f'sop_search')

    filter_category = st.multiselect('Filter by Category', sop_categories.keys(), default=list(sop_categories.keys()))

    # Apply filters
    df_filter = df.copy()

    # Find rows which contain the filter term in any column
    df_filter = df_filter[df_filter.astype(str).sum(axis=1).str.contains(filter_term, case=False)]

    # Find rows where the category is in the filter_category list
    df_filter = df_filter[df_filter['category'].isin(filter_category)]

    #Display filtered data
    st.dataframe(df_filter[['id', 'title', 'purpose']], use_container_width=True)

    view, create = st.tabs(['View', 'Create'])
    with view:
        view_id = st.selectbox('SOP ID', df_filter['id'].values, format_func=lambda x: f'{x} - {df_filter[df_filter["id"] == x]["title"].values[0]}')
        if view_id:
            query_df = df[df['id'] == view_id]
            if not query_df.empty:
                query_df_t = query_df.T
                query_df_t.columns = ['value']

                query_dict = query_df_t.to_dict()['value']
                for k, v in query_dict.items():
                    try:
                        query_dict[k] = json.loads(v)
                    except:
                        pass

                # Create a PDF
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer)
                
                # Create a list of elements to add to the PDF
                elements = []
                hr = [Spacer(1, 10), HRFlowable(width="100%")]
               
                # ID and Title
                elements.append(Paragraph(query_dict['id'], pdf_styles['Normal']))
                elements.append(Paragraph(query_dict["title"], pdf_styles['Heading1']))
                elements += hr
                
                # Purpose
                elements.append(Paragraph("Purpose", pdf_styles['Heading2']))
                elements.append(Paragraph(query_dict["purpose"], pdf_styles['Normal']))
                elements += hr
                
                # Scope
                elements.append(Paragraph("Scope", pdf_styles['Heading2']))
                elements.append(Paragraph("Covered", pdf_styles['Heading3']))
                for x in query_dict["scope_covered"]:
                    elements.append(Paragraph(f"• {x}", pdf_styles['Normal']))
                elements.append(Paragraph("Not covered", pdf_styles['Heading3']))
                for x in query_dict["scope_not_covered"]:
                    elements.append(Paragraph(f"• {x}", pdf_styles['Normal']))
                elements += hr
                
                # Applications
                elements.append(Paragraph("Applications", pdf_styles['Heading2']))
                elements.append(Paragraph(query_dict["applications"], pdf_styles['Normal']))
                elements += hr
                
                # Definitions
                elements.append(Paragraph("Definitions", pdf_styles['Heading2']))
                for k, v in query_dict["definitions"].items():
                    elements.append(Paragraph(f"<b>{k}:</b> {v}", pdf_styles['Normal']))
                elements += hr
                
                # Responsibilities
                elements.append(Paragraph("Responsibilities", pdf_styles['Heading2']))
                for k, v in query_dict["responsibilities"].items():
                    elements.append(Paragraph(f"<b>{k}:</b> {v}", pdf_styles['Normal']))
                elements += hr
               
                # Procedure
                elements.append(Paragraph("Procedure", pdf_styles['Heading2']))
                for k, v in query_dict["procedure"].items():
                    elements.append(Paragraph(k, pdf_styles['Heading3']))
                    for x in v:
                        elements.append(Paragraph(f"• {x}", pdf_styles['Normal']))
                elements += hr
                
                # Health and Safety
                elements.append(Paragraph("Health and Safety", pdf_styles['Heading2']))
                elements.append(Paragraph("PPE", pdf_styles['Heading3']))
                for k, v in query_dict["ppe"].items():
                    elements.append(Paragraph(f"<b>{k}:</b> {v}", pdf_styles['Normal']))
                elements.append(Paragraph("Hazards and mitigation", pdf_styles['Heading3']))
                for k, v in query_dict["hazards_and_mitigation"].items():
                    elements.append(Paragraph(f"<b>{k}:</b> {v}", pdf_styles['Normal']))
                elements.append(Paragraph("Emergency procedures", pdf_styles['Heading3']))
                for k, v in query_dict["emergency_procedures"].items():
                    elements.append(Paragraph(f"<b>{k}:</b> {v}", pdf_styles['Normal']))
                elements += hr

                # Build the PDF document
                doc.build(elements, canvasmaker=NumberedCanvas)
                pdf_bytes = buffer.getbuffer().tobytes()
                pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

                # Embedding PDF in HTML
                pdf_display = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="600" height="900" type="application/pdf">'

                # Displaying File
                st.markdown(pdf_display, unsafe_allow_html=True)

    # with create:

    #     sop_dict = {
    #         'id': '',
    #         'category': '',
    #         'category_code': '',
    #         'number': '',
    #         'version': '',
    #         'effective_date': '',
    #         'title': '',
    #         'purpose': '',
    #         'scope': '',
    #         'responsibilities': '',
    #         'procedure': '',
    #         'related_documents': '',
    #         'revision_history': '',
    #     }

    #     valid_id = True
        
    #     # User input for new SOP ID
    #     sop_category = st.selectbox('SOP Category', list(sop_categories.keys()))
    #     sop_category_code = sop_categories[sop_category]
    #     sop_number = st.number_input('SOP Number', min_value=1, max_value=9999, value=1, format='%04d')
    #     sop_version = st.number_input('SOP Version', min_value=1, max_value=99, value=1, format='%02d')

    #     # Generate SOP ID
    #     sop_id_without_version = f'{sop_category_code}-{sop_number:04d}'
    #     sop_id = f'{sop_category_code}-{sop_number:04d}-v{sop_version:02d}'

    #     sop_category_next = int(df[df['category'] == sop_category]['number'].max() + 1)

    #     sop_id_versions = df[df['id'].str.contains(sop_id_without_version)]
    #     if not sop_id_versions.empty:
    #         sop_id_latest_version_number = int(sop_id_versions['version'].max())
    #         sop_id_latest_version = sop_id_versions[sop_id_versions['version'] == sop_id_latest_version_number]
    #         sop_dict = sop_id_latest_version.to_dict('records')[0]
    #         sop_id_title = sop_id_versions['title'].values[0]

    #     # Check if SOP ID and version number already exists
    #     if sop_id in df['id'].values:
    #         st.error(f'''
    #         {sop_id} already exists  

    #         {sop_id_without_version} refers to {sop_id_title}, the latest version is {sop_id_latest_version_number:02d}  

    #         The next available SOP number in the {sop_category} category is {sop_category_next:04d}
    #         ''')
    #         valid_id = False

    #     # if not sop_version == sop_id_latest_version_number + 1:
    #     #     st.error(f'''
    #     #     {sop_id_without_version} refers to {sop_id_title}, the latest version is {sop_id_latest_version_number:02d}
    #     #     ''')
    #     #     valid_id = False

    #     # if not sop_number == sop_category_next:
    #     #     st.error(f'''
    #     #     The next available SOP number in the {sop_category} category is {sop_category_next:04d}
    #     #     ''')
        
    #     if not valid_id:
    #         return None
            
    #     st.info(f'New SOP ID: {sop_id}')

    #     sop_dict['id'] = sop_id
    #     sop_dict['category'] = sop_category
    #     sop_dict['category_code'] = sop_category_code
    #     sop_dict['number'] = sop_number
    #     sop_dict['version'] = sop_version

    #     sop_dict['effective_date'] = st.date_input('Effective Date', value=datetime.now(), help='The date that this SOP will go into effect')
    #     sop_dict['title'] = st.text_input('Title', value=sop_dict['title'], help='The title of this SOP, should be descriptive and concise')
    #     sop_dict['purpose'] = st.text_area('Purpose', value=sop_dict['purpose'], help='The purpose of this SOP, including why it is needed and what it is used for')
    #     sop_dict['scope'] = st.text_area('Scope', value=sop_dict['scope'], help='The scope of this SOP, including what is covered and what is not covered')
    #     sop_dict['responsibilities'] = st.text_area('Responsibilities', value=sop_dict['responsibilities'], help='The responsibilities of each role in this SOP')
    #     sop_dict['procedure'] = st.text_area('Procedures', value=sop_dict['procedure'], help='The procedures for this SOP, including step-by-step instructions, safety precautions, and quality control measures')
    #     sop_dict['related_documents'] = st.text_area('Related Documents', value=sop_dict['related_documents'], help='Any related documents that are referenced in this SOP')
    #     sop_dict['revision_history'] = st.text_area('Revision History', value=sop_dict['revision_history'], help='The revision history for this SOP, including the date, version number, person responsible, and description of changes')

    #     if st.button('Save SOP'):
    #         # Append new SOP to the dataframe
    #         df = df.append(sop_dict, ignore_index=True)

    #         # Save updated dataframe to Google Sheets
    #         set_with_dataframe(worksheet, df)

    #         # Display success message
    #         st.success(f'Successfully added SOP: {sop_id}')


def electronic_lab_notebook():
    st.header('Electronic Lab Notebook (ELN)')
    st.caption("""
    An electronic lab notebook (ELN) is a digital version of a paper lab notebook.  
    ELNs can be used to record and store data, and can be integrated with your LIMS to automatically import data.
    """)
    st.write("Coming soon")


def integration_interoperability():
    st.header('Integration and Interoperability')
    st.caption("""
    Integration and interoperability are the processes of connecting your LIMS to other systems and instruments in your laboratory.  
    This might include connecting to instruments to automatically import data, or connecting to other systems to share data.
    """)
    st.write("Coming soon")


def reporting_analytics():
    st.header('Reporting and Analytics')
    st.caption("""
    Reporting and analytics are the processes of generating reports and analyzing data to help you make informed decisions.
    """)
    st.write("Coming soon")


def regulatory_compliance():
    st.header('Regulatory Compliance')
    st.caption("""
    Regulatory compliance is the process of ensuring that your laboratory is following all applicable laws, regulations, and standards.
    """)
    st.write("Coming soon")


def security_audit_trails():
    st.header('Security and Audit Trails')
    st.caption("""
    Security and audit trails are the processes of ensuring that your laboratory data is secure and that you can track who has accessed or modified data.
    """)
    st.write("Coming soon")


def chain_of_custody():
    st.header('Chain of Custody')
    st.caption("""
    Chain of custody is the process of tracking the movement of samples and data through your laboratory.
    """)
    st.write("Coming soon")

    

lqms_structure = [
    {
        "title":"Organization",
        "description": "The organization section describes the structure of the laboratory, including the organizational chart, personnel responsibilities, and conflict of interest policies.",
        "subcategories": [
            {
                "title": "Conflict of interest",
                "description": "Conflict of interest policies are used to ensure that laboratory personnel do not have any conflicts of interest that could affect the quality of their work.",
                "example": "The laboratory is not engaged in any activity that might influence its technical judgment.  The laboratory is not committed to any commercial, financial or other pressure provided by any particular organization that could influence its technical judgment or affect its competencies and trust.",
            },
            {
                "title": "Organization chart",
                "description": "The organization chart is used to show the structure of the laboratory, including the roles and responsibilities of each position.",
            },
            {
                "title": "Internal communication",
                "description": "Internal communication policies are used to ensure that laboratory personnel are communicating effectively with each other.",
            },
            {
                "title": "Personnel responsibilities",
                "description": "Personnel responsibilities are used to ensure that laboratory personnel are performing their duties in accordance with the laboratory's policies and procedures.",
            }
        ]
    },
    {
        "title": "Facilities and Safety",
        "description": "The facilities and safety section describes the facilities and safety procedures of the laboratory, including the laboratory layout, equipment, and safety precautions.",
        "subcategories": [
            {
                "title": "Facilities",
                "description": "Facilities are used to describe the physical layout of the laboratory, including the location of equipment and workstations.",
            },
            {
                "title": "Security",
                "description": "Security is used to describe the security measures that are in place to protect the laboratory from unauthorized access.",
            },
            {
                "title": "Working environment",
                "description": "Working environment is used to describe the working conditions in the laboratory, including noise levels and temperature.",
            },
            {
                "title": "Waste disposal",
                "description": "Waste disposal is used to describe the procedures for disposing of waste in the laboratory.",
            },
        ]
    },
    {
        "title": "Equipment",
        "description": "The management of the laboratory ensures that equipment is properly selected, installed, validated, maintained and disposed of according to established procedures and manufacturer's instructions to meet the needs of the laboratory to perform quality diagnostic testing.",

        "subcategories": [
            {
                "title": "Selection of equipment",
                "description": "Selection of equipment is used to describe the process for selecting equipment in the laboratory.",
            },
            {
                "title": "Installation and acceptance Criteria",
                "description": "Installation and acceptance criteria are used to describe the process for installing and accepting equipment in the laboratory.",
            },
            {
                "title": "Equipment Inventory and master file",
                "description": "Equipment inventory and master file are used to describe the process for maintaining an inventory of equipment in the laboratory.",
            },
            {
                "title": "Validation",
                "description": "Validation is used to describe the process for validating equipment in the laboratory.",
            },
            {
                "title": "Preventive maintenance and repair",
                "description": "Preventive maintenance and repair are used to describe the process for maintaining and repairing equipment in the laboratory.",
            },
            {
                "title": "Decommissioning",
                "description": "Decommissioning is used to describe the process for decommissioning equipment in the laboratory.",
            },
        ]
    },
    {
        "title": "Purchasing and Inventory",
        "description": "The purchasing and inventory section describes the purchasing and inventory procedures of the laboratory, including the purchasing of supplies and equipment, and the inventory of supplies and equipment.",
        "subcategories": [
            {
                "title": "Reagents and consumables management",
                "description": "Reagents and consumables management is used to describe the process for managing reagents and consumables in the laboratory.",
            },
            {
                "title": "Selection and evaluation of providers",
                "description": "Selection and evaluation of providers is used to describe the process for selecting and evaluating providers in the laboratory.",
            },
            {
                "title": "Procurement",
                "description": "Procurement is used to describe the process for procuring supplies and equipment in the laboratory.",
            },
            {
                "title": "Stock management and inventory",
                "description": "Stock management and inventory is used to describe the process for managing stock and inventory in the laboratory.",
            },
            {
                "title": "Referral laboratories / subcontracting",
                "description": "Referral laboratories / subcontracting is used to describe the process for referring samples to other laboratories in the laboratory.",
            },
        ],
    },
    {
        "title": "Process Management",
        "description": "The process management section describes the process management procedures of the laboratory, including the process for sample collection, sample processing, and sample analysis.",
        "subcategories": [
            {
                "title": "Sample management",
                "description": "Sample management is used to describe the process for managing samples in the laboratory.",
            },
            {
                "title": "Method validation",
                "description": "Method validation is used to describe the process for validating methods in the laboratory.",
            },
            {
                "title": "List of examinations",
                "description": "List of examinations is used to describe the list of examinations that are performed in the laboratory.",
            },
            {
                "title": "Restrictive list",
                "description": "Restrictive list is used to describe the list of examinations that are not performed in the laboratory.",
            },
            {
                "title": "Quality control",
                "description": "Quality control is used to describe the process for performing quality control in the laboratory.",
            },
            {
                "title": "Reporting",
                "description": "Reporting is used to describe the process for reporting results in the laboratory.",
            },
            {
                "title": "Sample retention and disposal",
                "description": "Sample retention and disposal is used to describe the process for retaining and disposing of samples in the laboratory.",
            },
        ],
    },
    {
        "title": "Assessments",
        "description": "The assessments section describes the assessments procedures of the laboratory, including the internal audits, external audits, and proficiency testing.",
        "subcategories": [
            {
                "title": "Internal audits",
                "description": "Internal audits are used to describe the process for performing internal audits in the laboratory.",
            },
            {
                "title": "Review and follow up of corrective actions",
                "description": "Review and follow up of corrective actions are used to describe the process for reviewing and following up on corrective actions in the laboratory.",
            },
            {
                "title": "Quality indicators",
                "description": "Quality indicators are used to describe the quality indicators that are used in the laboratory.",
            },
            {
                "title": "Staff suggestions",
                "description": "Staff suggestions are used to describe the process for collecting staff suggestions in the laboratory.",
            },
            {
                "title": "Review of requests, methods and sampling requirements",
                "description": "Review of requests, methods and sampling requirements are used to describe the process for reviewing requests, methods and sampling requirements in the laboratory.",
            },
            {
                "title": "External Quality Assessment/ Proficiency testing",
                "description": "External Quality Assessment/ Proficiency testing are used to describe the process for performing external quality assessment and proficiency testing in the laboratory.",
            },
            {
                "title": "Customer feedback",
                "description": "Customer feedback is used to describe the process for collecting customer feedback in the laboratory.",
            },
            {
                "title": "External audits",
                "description": "External audits are used to describe the process for performing external audits in the laboratory.",
            }
        ],
    },
    {
        "title": "Personnel",
        "description": "The personnel section describes the personnel procedures of the laboratory, including the recruitment, training, and performance appraisal of personnel.",
        "subcategories": [
            {
                "title": "Recruitment",
                "description": "Recruitment is used to describe the process for recruiting personnel in the laboratory.",
            },
            {
                "title": "Personnel file / health file",
                "description": "Personnel file / health file is used to describe the process for maintaining personnel files and health files in the laboratory.",
            },
            {
                "title": "Integration and clearance",
                "description": "Integration and clearance is used to describe the process for integrating and clearing personnel in the laboratory.",
            },
            {
                "title": "Training",
                "description": "Training is used to describe the process for training personnel in the laboratory.",
            },
            {
                "title": "Staff competency",
                "description": "Staff competency is used to describe the process for assessing staff competency in the laboratory.",
            },
            {
                "title": "Personnel performance appraisal",
                "description": "Personnel performance appraisal is used to describe the process for appraising personnel performance in the laboratory.",
            },
            {
                "title": "Continuous education",
                "description": "Continuous education is used to describe the process for providing continuous education in the laboratory.",
            },
            {
                "title": "Non-permanent personnel",
                "description": "Non-permanent personnel is used to describe the process for managing non-permanent personnel in the laboratory.",
            },
        ]
    },
    {
        "title": "Customer Focus",
        "description": "The customer focus section describes the customer focus procedures of the laboratory, including the customer focus policy, customer satisfaction measurement, and claims management.",
        "subcategories": [
            {
                "title": "Customers satisfaction measurement",
                "description": "Customers satisfaction measurement is used to describe the process for measuring customers satisfaction in the laboratory.",
            },
            {
                "title": "Claims management",
                "description": "Claims management is used to describe the process for managing claims in the laboratory.",
            },
        ]
    },
    {
        "title": "Nonconforming Event Management",
        "description": "The nonconforming event management section describes the nonconforming event management procedures of the laboratory, including the nonconforming event management policy, nonconforming event management, and corrective action.",
        "subcategories": [
            {
                "title": "Corrective Actions",
                "description": "Corrective Actions is used to describe the process for performing corrective actions in the laboratory.",
            },
        ]
    },
    {
        "title": "Continual Improvement",
        "description": "The continual improvement section describes the continual improvement procedures of the laboratory, including the continual improvement policy, continual improvement, and continual improvement plan.",
        "subcategories": [
            {
                "title": "Quality indicators",
                "description": "Quality indicators are used to describe the quality indicators that are used in the laboratory.",
            },
            {
                "title": "Management review",
                "description": "Management review is used to describe the process for performing management review in the laboratory.",
            },
            {
                "title": "Preventive action",
                "description": "Preventive action is used to describe the process for performing preventive action in the laboratory.",
            },
        ]
    },
    {
        "title": "Documents and Records",
        "description": "The documents and records section describes the documents and records procedures of the laboratory, including the documents and records policy, documents and records control, and documents and records management.",
        "subcategories": [
            {
                "title": "Documentation management",
                "description": "Documentation management is used to describe the process for managing documentation in the laboratory.",
            },
            {
                "title": "Documents and records control",
                "description": "Documents and records control is used to describe the process for controlling documents and records in the laboratory.",
            },
            {
                "title": "Archiving",
                "description": "Archiving is used to describe the process for archiving documents and records in the laboratory.",
            },
            {
                "title": "Review of contracts",
                "description": "Review of contracts is used to describe the process for reviewing contracts in the laboratory.",
            }
        ]
    },
    {
        "title": "Information Management",
        "description": "The information management section describes the information management procedures of the laboratory, including the information management policy, information management, and information management plan.",
        "subcategories": [
            {
                "title": "Information system - Security",
                "description": "Information system - Security is used to describe the process for securing the information system in the laboratory.",
            },
            {
                "title": "Confidentiality",
                "description": "Confidentiality is used to describe the process for maintaining confidentiality in the laboratory.",
            },
        ]
    },
]

equipment_calssification = [
    {"application": "Analytical", "type": "Chromatography", "sub_type": "High Performance Liquid Chromatography (HPLC)"},
    {"application": "Analytical", "type": "Chromatography", "sub_type": "Gas Chromatography (GC)"},
    {"application": "Analytical", "type": "Chromatography", "sub_type": "Thin Layer Chromatography (TLC)"},
    {"application": "Analytical", "type": "Spectroscopy", "sub_type": "Ultraviolet-Visible (UV-Vis)"},
    {"application": "Analytical", "type": "Spectroscopy", "sub_type": "Fourier Transform Infrared (FTIR)"},
    {"application": "Analytical", "type": "Spectroscopy", "sub_type": "Nuclear Magnetic Resonance (NMR)"},
    {"application": "Analytical", "type": "Spectroscopy", "sub_type": "Raman"},
    {"application": "Analytical", "type": "Spectroscopy", "sub_type": "X-Ray Fluorescence (XRF)"},
    {"application": "Analytical", "type": "Spectroscopy", "sub_type": "X-Ray Diffraction (XRD)"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Optical Microscopy"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Scanning Electron Microscopy (SEM)"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Transmission Electron Microscopy (TEM)"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Atomic Force Microscopy (AFM)"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Scanning Probe Microscopy (SPM)"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Confocal Microscopy"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Fluorescence Microscopy"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Scanning Tunneling Microscopy (STM)"},
    {"application": "Analytical", "type": "Microscopy", "sub_type": "Raman Microscopy"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Enzyme-Linked Immunosorbent Assay (ELISA)"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Polymerase Chain Reaction (PCR)"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Western Blot"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Gel Electrophoresis"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Flow Cytometry"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Circular Dichroism (CD)"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Fluorescence Resonance Energy Transfer (FRET)"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Surface Plasmon Resonance (SPR)"},
    {"application": "Analytical", "type": "Bioanalysis", "sub_type": "Isothermal Titration Calorimetry (ITC)"},
    {"application": "Analytical", "type": "Thermal Analysis", "sub_type": "Differential Scanning Calorimetry (DSC)"},
    {"application": "Analytical", "type": "Thermal Analysis", "sub_type": "Thermogravimetric Analysis (TGA)"},
    {"application": "Analytical", "type": "Mass Spectrometry", "sub_type": "Matrix-Assisted Laser Desorption/Ionization Time-of-Flight (MALDI-TOF)"},
    {"application": "Analytical", "type": "Mass Spectrometry", "sub_type": "Electrospray Ionization (ESI)"},
    {"application": "Analytical", "type": "Mass Spectrometry", "sub_type": "Gas Chromatography-Mass Spectrometry (GC-MS)"},
    {"application": "Analytical", "type": "Mass Spectrometry", "sub_type": "Liquid Chromatography-Mass Spectrometry (LC-MS)"},
    {"application": "Analytical", "type": "Mass Spectrometry", "sub_type": "Inductively Coupled Plasma-Mass Spectrometry (ICP-MS)"},
    {"application": "Analytical", "type": "Particle Size Analysis", "sub_type": "Dynamic Light Scattering (DLS)"},
    {"application": "Analytical", "type": "Particle Size Analysis", "sub_type": "Laser Diffraction"},
    {"application": "Analytical", "type": "Particle Size Analysis", "sub_type": "Nano Particle Tracking Analysis (NTA)"},
    {"application": "Process", "type": "Drying", "sub_type": "Vacuum Oven"},
    {"application": "Process", "type": "Drying", "sub_type": "Freeze Dryer"},
    {"application": "Process", "type": "Drying", "sub_type": "Spray Dryer"},
    {"application": "Process", "type": "Drying", "sub_type": "Electrospinning/Electrospraying"},
    {"application": "Process", "type": "Drying", "sub_type": "Rotary Evaporator"},
    {"application": "Process", "type": "Homogenization", "sub_type": "Probe Sonicator"},
    {"application": "Process", "type": "Homogenization", "sub_type": "Ultrasonic Bath"},
    {"application": "Process", "type": "Homogenization", "sub_type": "High-Pressure Homogenizer"},
    {"application": "Process", "type": "Homogenization", "sub_type": "Ball Mill"},
    {"application": "Process", "type": "Separation", "sub_type": "Centrifuge"},
    {"application": "Process", "type": "Separation", "sub_type": "Filtration"},
    {"application": "Process", "type": "Separation", "sub_type": "Chromatography"},
    {"application": "Process", "type": "Separation", "sub_type": "Dialysis"},
    {"application": "Process", "type": "Separation", "sub_type": "Evaporation"},
    {"application": "Process", "type": "Separation", "sub_type": "Extraction"},
    {"application": "Process", "type": "Sterilization", "sub_type": "Autoclave"},
    {"application": "Process", "type": "Sterilization", "sub_type": "Dry Heat Oven"},
    {"application": "Process", "type": "Sterilization", "sub_type": "UV Light"},
    {"application": "Process", "type": "Sterilization", "sub_type": "Gamma Irradiation"},
]

equipment_calssification_dict = defaultdict(dict)
for item in equipment_calssification:
    equipment_calssification_dict[item['application']][item['type']] = item['sub_type']

# database_structures = {
#     "inventory_equipment": ['id', 'name', 'type', 'sub_type', 'manufacturer', 'model', 'serial_number', 'location', 'notes'],
#     "inventory_reagents": ['id', 'name', 'supplier', 'catalog_number', 'lot_number', 'expiration_date', 'cas', 'location', 'notes'],
#     "inventory_samples": ['id', 'name', 'type', 'description', 'owner', 'location', 'notes'],
#     "inventory_supplies": ['id', 'name', 'description', 'supplier', 'catalog_number', 'location', 'notes'],
#     "sops": ['id', 'category', 'number', 'version', 'title', 'effective_date', 'purpose', 'related_documents', 'scope', 'procedure', 'references'],
#     }

database_structures = {
    "inventory_equipment": [
        {"column_name": "id", "formated_name": "ID", "type": "string", "description": "Unique identifier for the equipment", "required": True, "unique": True, "primary_key": True, "foreign_key": False, "default": None, "example": "EQ-99414a"},
        {"column_name": "name", "formated_name": "Name", "type": "string", "description": "Name of the equipment", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "HPLC - Agilent 1260 Infinity II"},
        {"column_name": "application", "formated_name": "Application", "type": "string", "description": "Application of the equipment", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Analytical"},
        {"column_name": "type", "formated_name": "Type", "type": "string", "description": "Type of equipment", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Chromatography"},
        {"column_name": "sub_type", "formated_name": "Sub Type", "type": "string", "description": "Sub type of equipment", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "High Performance Liquid Chromatography (HPLC)"},
        {"column_name": "manufacturer", "formated_name": "Manufacturer", "type": "string", "description": "Manufacturer of the equipment", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Agilent"},
        {"column_name": "model", "formated_name": "Model", "type": "string", "description": "Model of the equipment", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "1260 Infinity II"},
        {"column_name": "serial_number", "formated_name": "Serial Number", "type": "string", "description": "Serial number of the equipment", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "US12345678"},
        {"column_name": "location", "formated_name": "Location", "type": "string", "description": "Location of the equipment", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Lab 1"},
        {"column_name": "notes", "formated_name": "Notes", "type": "string", "description": "Notes about the equipment", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Used for HPLC analysis"},       
    ],
    "inventory_reagents": [
        {"column_name": "id", "formated_name": "ID", "type": "string", "description": "Unique identifier for the reagent", "required": True, "unique": True, "primary_key": True, "foreign_key": False, "default": None, "example": "RRE-02c045"},
        {"column_name": "name", "formated_name": "Name", "type": "string", "description": "Name of the reagent", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Acetonitrile"},
        {"column_name": "supplier", "formated_name": "Supplier", "type": "string", "description": "Supplier of the reagent", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Fisher Scientific"},
        {"column_name": "catalog_number", "formated_name": "Catalog Number", "type": "string", "description": "Catalog number of the reagent", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "A998-4"},
        {"column_name": "lot_number", "formated_name": "Lot Number", "type": "string", "description": "Lot number of the reagent", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "123456"},
        {"column_name": "expiration_date", "formated_name": "Expiration Date", "type": "date", "description": "Expiration date of the reagent", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "2021-12-31"},
        {"column_name": "cas", "formated_name": "CAS", "type": "string", "description": "Chemical Abstracts Service (CAS) number of the reagent", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "75-05-8"},
        {"column_name": "location", "formated_name": "Location", "type": "string", "description": "Location of the reagent", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Lab 1"},
        {"column_name": "notes", "formated_name": "Notes", "type": "string", "description": "Notes about the reagent", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Stored in flammable cabinet"},
    ],
    "inventory_samples": [
        {"column_name": "id", "formated_name": "ID", "type": "string", "description": "Unique identifier for the sample", "required": True, "unique": True, "primary_key": True, "foreign_key": False, "default": None, "example": "SA-ad6b54"},
        {"column_name": "name", "formated_name": "Name", "type": "string", "description": "Name of the sample", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Sample 1"},
        {"column_name": "type", "formated_name": "Type", "type": "string", "description": "Type of sample", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Chemical"},
        {"column_name": "description", "formated_name": "Description", "type": "string", "description": "Description of the sample", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Sample of chemical X"},
        {"column_name": "owner", "formated_name": "Owner", "type": "string", "description": "Owner of the sample", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "John Smith"},
        {"column_name": "location", "formated_name": "Location", "type": "string", "description": "Location of the sample", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Lab 1"},
        {"column_name": "notes", "formated_name": "Notes", "type": "string", "description": "Notes about the sample", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Stored in freezer"},
    ],
    "inventory_supplies": [
        {"column_name": "id", "formated_name": "ID", "type": "string", "description": "Unique identifier for the supply", "required": True, "unique": True, "primary_key": True, "foreign_key": False, "default": None, "example": "SU-30acb7"},
        {"column_name": "name", "formated_name": "Name", "type": "string", "description": "Name of the supply", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Gloves, Nitrile, M"},
        {"column_name": "category", "formated_name": "Category", "type": "string", "description": "Category of the supply", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "PPE"},
        {"column_name": "description", "formated_name": "Description", "type": "string", "description": "Description of the supply", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Nitrile gloves, size medium"},
        {"column_name": "supplier", "formated_name": "Supplier", "type": "string", "description": "Supplier of the supply", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Fisher Scientific"},
        {"column_name": "catalog_number", "formated_name": "Catalog Number", "type": "string", "description": "Catalog number of the supply", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "11889610"},
        {"column_name": "location", "formated_name": "Location", "type": "string", "description": "Location of the supply", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Lab 1"},
        {"column_name": "notes", "formated_name": "Notes", "type": "string", "description": "Notes about the supply", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Stored in cabinet"},
    ],
    "sops": [
        {"column_name": "id", "formated_name": "ID", "type": "string", "description": "Unique identifier for the SOP", "required": True, "unique": True, "primary_key": True, "foreign_key": False, "default": None, "example": "QA-0001-v01"},
        {"column_name": "category", "formated_name": "Category", "type": "string", "description": "Category of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Quality Assurance"},
        {"column_name": "number", "formated_name": "Number", "type": "int", "description": "Number of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": 1},
        {"column_name": "version", "formated_name": "Version", "type": "int", "description": "Version of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": 1},
        {"column_name": "title", "formated_name": "Title", "type": "string", "description": "Title of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "Document Control Procedure"},
        {"column_name": "effective_date", "formated_name": "Effective Date", "type": "date", "description": "Effective date of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "2021-01-01"},
        {"column_name": "purpose", "formated_name": "Purpose", "type": "string", "description": "Purpose of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "To ensure that all documents are controlled and that only current versions are available for use."},
        {"column_name": "scope", "formated_name": "Scope", "type": "string", "description": "Scope of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None,
            "example": "This procedure applies to all documents that form part of the laboratorys Quality Management System (QMS), including SOPs, work instructions, forms, protocols, and reports."},
        {"column_name": "responsibilities", "formated_name": "Responsibilities", "type": "string", "description": "Responsibilities of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": """
            1. Document Controller: Responsible for maintaining and updating the Document Control Register, and for distributing controlled documents.
            2. Department Heads: Responsible for ensuring documents within their area are kept current and staff are trained on the latest revisions.
            3. All Employees: Responsible for following the most current version of each document.
            """},
        {"column_name": "procedure", "formated_name": "Procedure", "type": "string", "description": "Procedure of the SOP", "required": True, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": """
            ## 1. Document Creation
            Documents should be written in clear, concise language, and follow the laboratorys standard format. Once drafted, documents should be reviewed and approved by the document owner and department head.
            ## 2. Document Review and Approval
            All new or revised documents must be reviewed for adequacy by the department head and approved by the Quality Assurance department. The review and approval must be documented.
            ## 3. Document Distribution
            Upon approval, the Document Controller should distribute the document to all relevant parties, and ensure obsolete versions are withdrawn. The distribution and receipt of controlled documents should be recorded.
            ## 4. Document Revision
            Any changes to a document must go through the same review and approval process as a new document. Each revision should be given a new version number, and the changes should be summarized in a revision history table in the document.
            ## 5. Document Archiving
            Superseded versions of documents should be archived for a defined period according to the laboratorys record retention policy.
            ## 6. Document Training
            All affected personnel should be trained on new or revised documents prior to implementation. Training should be documented.
            """},
        {"column_name": "references", "formated_name": "References", "type": "string", "description": "References of the SOP", "required": False, "unique": False, "primary_key": False, "foreign_key": False, "default": None, "example": "ISO 17025:2017"},
    ],
}


# Define custom styles for PDF generation
pdf_title_style = ParagraphStyle(
    "title",
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=30,
    textColor="#333333",
)
pdf_section_style = ParagraphStyle(
    "section",
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=24,
    textColor="#333333",
    spaceBefore=5 * mm,
    spaceAfter=2.5 * mm,
)
pdf_text_style = ParagraphStyle(
    "text",
    fontName="Helvetica",
    fontSize=12,
    leading=18,
    textColor="#666666",
    spaceBefore=2.5 * mm,
    spaceAfter=2.5 * mm,
    alignment=TA_JUSTIFY,
)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 20*mm, f"Page {self._pageNumber} of {page_count}")

def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    page_num_total = doc.page
    text = f"Page {page_num} of {page_num_total}"
    canvas.drawRightString(200*mm, 20*mm, text)
    # canvas.drawCentredString(100*mm, 20*mm, "Document controlled only when viewed on the SciSpaceLIMS")
    
def df2table(df):
    return Table([[Paragraph(col) for col in df.columns]] + df.values.tolist(),
      style=[
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white])],
      hAlign = 'LEFT')


PAGES = {
    # 'ELN Integration': electronic_lab_notebook,
    # 'Data Management': data_management,
    'Quality Management System': quality_management_system,
    'Standard Operating Procedures': standard_operating_procedures,
    'Inventory Management': inventory_management,
    # 'Integration and Interoperability': integration_interoperability,
    # 'Reporting and Analytics': reporting_analytics,
    # 'Regulatory Compliance': regulatory_compliance,
    # 'Security and Audit Trails': security_audit_trails,
    # 'Chain of Custody': chain_of_custody,
}


# Connect to Google Sheets
gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])

sh = gc.open('SciSpaceLIMS')


def main():

    st.set_page_config(page_title='SciSpace LIMS', page_icon=':blue_book:', layout='wide', initial_sidebar_state='auto')

    st.sidebar.markdown("""
    <u>L</u>aboratory  
    <u>I</u>nformation  
    <u>M</u>anagement  
    <u>S</u>ystem
    """,
    unsafe_allow_html=True)
    choice = st.sidebar.selectbox('Select Page', list(PAGES.keys()), label_visibility='collapsed')
    PAGES[choice]()

if __name__ == '__main__':
    main()
