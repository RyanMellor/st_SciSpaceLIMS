import streamlit as st

import pandas as pd
from io import BytesIO
from uuid import uuid4
import json

import fitz

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, ListStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageTemplate, Frame, Table, TableStyle, ListFlowable, ListItem
from reportlab.platypus.flowables import HRFlowable, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
pdf_styles = getSampleStyleSheet()

from helpers import sci_report, sci_setup

sci_setup.setup_page("Standard Operating Procedures")
sci_setup.connect_google_sheets('SciSpaceLIMS', st.secrets["gcp_service_account"])

def main():

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

    worksheet = st.session_state['sh'].worksheet('sops')

    # Fetch existing data
    df = pd.DataFrame(worksheet.get_all_records())
    df.dropna(how='all', inplace=True)
    df = df[[col for col in df.columns if 'Unnamed' not in col]]
    df.sort_values(by=['id'], inplace=True)
    df.reset_index(drop=True, inplace=True)

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

                # Related Documents
                elements.append(Paragraph("Related Documents", pdf_styles['Heading2']))
                for k, v in query_dict["related_documents"].items():
                    elements.append(Paragraph(f"<b>{k}:</b> {v}", pdf_styles['Normal']))
                elements += hr

                # Revision History
                elements.append(Paragraph("Revision History", pdf_styles['Heading2']))
                revision_history = pd.DataFrame(query_dict["revision_history"])
                revision_history.columns = [" ".join(i.split("_")).capitalize() for i in revision_history.columns]
                elements.append(sci_report.df2table(revision_history))
                elements += hr

                # Build the PDF document
                doc.build(elements, canvasmaker=sci_report.NumberedCanvas)
                pdf_bytes = buffer.getbuffer().tobytes()
                # pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

                # Use fitz to convert PDF to PNG
                pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                pdf_pngs = []
                for page in pdf_document:
                    pix = page.get_pixmap()
                    png = pix.tobytes("png")
                    pdf_pngs.append(png)

                with st.expander("PDF", expanded=True):
                    st.download_button("Download PDF", data=pdf_bytes, file_name=f"{query_dict['id']} - {query_dict['title']}.pdf")
                    for i, png in enumerate(pdf_pngs):
                        st.image(png, caption=f"Page {i+1}")

                
                # # Embedding PDF in HTML
                # pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="600" height="900" type="application/pdf"></iframe>'

                # # Displaying File
                # st.markdown(pdf_display, unsafe_allow_html=True)
                
                # md_title = f"# {query_dict['title']}"
                # md_purpose = query_dict['purpose']
                # md_scope_covered = "\n".join(
                #     [f"- {x}" for x in query_dict['scope_covered']])
                # md_scope_not_covered = "\n".join(
                #     [f"- {x}" for x in query_dict['scope_not_covered']])
                # md_applications = query_dict['applications']
                # md_definitions = "\n".join(
                #     [f"- **{k}**: {v}" for k, v in query_dict['definitions'].items()])
                # md_responsibilities = "\n".join(
                #     [f"- **{k}**: {v}" for k, v in query_dict['responsibilities'].items()])
                # md_procedure = ""
                # for k, v in query_dict['procedure'].items():
                #     md_procedure += f"\n### {k}\n"
                #     for i, x in enumerate(v):
                #         md_procedure += f"- {x}\n"
                # md_ppe = "\n".join(
                #     [f"- **{k}**: {v}" for k, v in query_dict['ppe'].items()])
                # md_hazards_and_mitigation = "\n".join(
                #     [f"- **{k}**: {v}" for k, v in query_dict['hazards_and_mitigation'].items()])
                # md_emergency_procedures = "\n".join(
                #     [f"- **{k}**: {v}" for k, v in query_dict['emergency_procedures'].items()])

                # md = "\n".join([
                #     md_title,
                #     "## Purpose",
                #     md_purpose,
                #     "## Scope",
                #     "### Covered",
                #     md_scope_covered,
                #     "### Not covered",
                #     md_scope_not_covered,
                #     "## Applications",
                #     md_applications,
                #     "## Definitions",
                #     md_definitions,
                #     "## Responsibilities",
                #     md_responsibilities,
                #     "## Procedure",
                #     md_procedure,
                #     "## Health and Safety",
                #     "### PPE",
                #     md_ppe,
                #     "### Hazards and mitigation",
                #     md_hazards_and_mitigation,
                #     "### Emergency procedures",
                #     md_emergency_procedures,
                # ])
                # print(md)
                # st.markdown(md, unsafe_allow_html=True)

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


if __name__ == '__main__':
    main()