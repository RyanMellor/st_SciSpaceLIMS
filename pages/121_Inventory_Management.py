import streamlit as st
import pandas as pd
from uuid import uuid4
from collections import defaultdict

from helpers import sci_setup

sci_setup.setup_page('Inventory Management')
sci_setup.connect_google_sheets('SciSpaceLIMS', st.secrets['gcp_service_account'])


def main():
    st.caption("""
    Inventory management is the process of tracking and managing your laboratory inventory.  

    The essention inventory types are:
    - Reagents (pure chemicals, buffers, etc.)
    - Samples (biological samples, cell lines, etc.)
    - Supplies (plasticware, pipette tips, etc.)
    - Equipment (microscopes, centrifuges, etc.)
    """)    

    tab_reagents, tab_samples, tab_supplies, tab_equipment = st.tabs(['Reagents', 'Samples', 'Supplies', 'Equipment'])
    
    with tab_reagents:
        manage_inventory("inventory_reagents")

    with tab_samples:
        manage_inventory("inventory_samples")

    with tab_supplies:
        manage_inventory("inventory_supplies")

    with tab_equipment:
        manage_inventory("inventory_equipment")


def manage_inventory(inventory_type):
    abvs = {
        'inventory_reagents': 'RE',
        'inventory_samples': 'SA',
        'inventory_supplies': 'SU',
        'inventory_equipment': 'EQ'
    }

    # Get the Google Sheet
    worksheet = st.session_state['sh'].worksheet(inventory_type)

    # Fetch existing data
    df = pd.DataFrame(worksheet.get_all_records())

    # Search
    search_term = st.text_input(f'Search', key=f'{inventory_type}_search')
    # available_applications = list(set(worksheet.col_values(3)))
    # filter_application = st.multiselect('Filter by Application', available_applications, default=available_applications, key=f'{inventory_type}_filter_application')


    # Display existing data
    search_df = df[df.astype(str).apply(lambda x: x.str.contains(search_term, case=False).any(), axis=1)]
    st.dataframe(search_df)

    tab_add, tab_remove, tab_update = st.tabs(['Add', 'Remove', 'Update'])
    with tab_add:
        new_item = pd.DataFrame().from_dict(
            {field['column_name']: None for field in database_structures[inventory_type][1:]}, orient='index').T
        new_item = st.data_editor(new_item)
        if st.button('Add Item', key=f'{inventory_type}_add'):
            new_item = new_item.to_dict('records')[0]
            new_item['id'] = f'{abvs[inventory_type]}-{str(uuid4())[:6]}'

            # Append new SOP to the dataframe
            df = df.append(new_item, ignore_index=True)

            # Save updated dataframe to Google Sheets
            worksheet.clear()
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
            # set_with_dataframe(worksheet, df)

            # Display success message
            new_item_name = new_item['name']
            st.success(f'Successfully added {new_item_name} to {inventory_type}.')

    with tab_remove:
        remove_id = st.text_input(f'Item ID', key=f'{inventory_type}_remove_id')
        if remove_id:
            st.dataframe(df[df['id'] == remove_id])
            if st.button('Remove Selected Item', key=f'{inventory_type}_remove'):
                df = df[df['id'] != remove_id]
                worksheet.clear()
                worksheet.update([df.columns.values.tolist()] + df.values.tolist())
                # set_with_dataframe(worksheet, df)
                st.success(f'Successfully removed {remove_id} from {inventory_type}.')
        
    with tab_update:
        update_id = st.text_input(f'Item ID', key=f'{inventory_type}_update_id')
        if update_id:
            update_item = df[df['id'] == update_id]
            update_item = st.data_editor(update_item, key=f'{inventory_type}_update_item')
            if st.button('Update Selected Item', key=f'{inventory_type}_update'):
                update_item = update_item.to_dict('records')[0]
                df = df[df['id'] != update_id]
                df = df.append(update_item, ignore_index=True)
                worksheet.clear()
                worksheet.update([df.columns.values.tolist()] + df.values.tolist())
                # set_with_dataframe(worksheet, df)
                st.success(f'Successfully updated {update_id} in {inventory_type}.')

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

if __name__ == '__main__':
    main()