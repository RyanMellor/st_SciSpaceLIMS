import streamlit as st

from helpers import sci_setup

sci_setup.setup_page("Quality Management System")
sci_setup.connect_google_sheets('SciSpaceLIMS', st.secrets["gcp_service_account"])

def main():
    st.header('Quality Management System')
    st.caption("""
    The Quality Management System (QMS) is designed to help maintain the high standards of your laboratory.  
    This particular implementation is based on the WHO Laboratory Quality Management System handbook, which can be found [here](https://www.who.int/publications/i/item/9789241548274).  
    Your laboratory should maintain a QMS manual that describes the policies and procedures for your laboratory.  
    Your needs may vary, so you may need to modify the QMS to fit your laboratory.
    """)

    # # Get the Google Sheet
    # worksheet = sh.worksheet('quality_management_system')
    
    # # Fetch existing data
    # records = worksheet.get_all_records()
    # def insert(tree, node):
    #     if node["parent_section"] == tree["section"]:
    #         if "child" not in tree:
    #             tree["child"] = [node]
    #         else:
    #             tree["child"].append(node)
    #     elif "child" in tree:
    #         for c in tree["child"]:
    #             insert(c, node)

    # ans_dict = {
    #     "order": 0,
    #     "section": "root",
    #     "parent_section": None
    # }
    # for record in records:
    #     insert(ans_dict, record)

    # ans_dict

    for category in lqms_structure:
        # Create an expander for each category
        with st.expander(category['title']):
            # Display the description for the category
            st.markdown(
                f"""
                <p style='color: grey;'>{category['description']}</p>
                
                ---
                
                """,
                unsafe_allow_html=True,)
            
            # Loop through the subcategories for the category
            for subcategory in category['subcategories']:
                # Display the subcategory name and description
                st.markdown(
                    f"""
                    <b>{subcategory['title']}</b>
                    <p style='color: grey;'>{subcategory['description']}</p>
                    """,
                    unsafe_allow_html=True,)
                
                try:
                    st.markdown(
                    f"""
                    <p style='color: grey;'>Example: </p>
                    <p style='color: grey'>{subcategory['example']}</p>
                    """,
                    unsafe_allow_html=True,)
                except:
                    pass

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

if __name__ == '__main__':
    main()