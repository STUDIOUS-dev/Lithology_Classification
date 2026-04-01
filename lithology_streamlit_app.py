import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import joblib
import os
import glob
from datetime import datetime
import json

# SVG Icons for consistent UI
SVG_ICONS = {
    'rock': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L4 7v10l8 5 8-5V7z"/><path d="M12 22V12"/><path d="M12 12L4 7"/><path d="M12 12l8-5"/></svg>',
    'upload': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    'chart': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    'metrics': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/></svg>',
    'download': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    'refresh': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 4v6h-6"/><path d="M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
    'search': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    'folder': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    'file': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>',
    'check': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    'error': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    'warning': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    'info': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    'alert': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    'target': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    'settings': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    'trophy': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17"/><path d="M14 14.66V17"/><path d="M18 22l-1-6H7l-1 6"/><path d="M8 22v-3h8v3"/><path d="M12 2a6 6 0 0 0-6 6v2.2c0 .6.4 1.1 1 1.3A6 6 0 0 0 12 14a6 6 0 0 0 5-2.5c.6-.2 1-.7 1-1.3V8a6 6 0 0 0-6-6z"/></svg>',
    'expand': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 6 9 12 15 18"/></svg>',
    'link': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    'magic': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 4V2"/><path d="M15 16v-2"/><path d="M8 9h2"/><path d="M20 9h2"/><path d="M17.8 11.8 19 13"/><path d="M15 9h0"/><path d="M17.8 6.2 19 5"/><path d="m3 21 9-9"/><path d="M12.2 6.2 11 5"/></svg>',
    'lightbulb': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    'ruler': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/></svg>',
}

def icon(name: str, size: int = 24) -> str:
    """Return SVG icon HTML string"""
    svg = SVG_ICONS.get(name, SVG_ICONS['info'])
    return f'<span style="display:inline-flex; vertical-align:middle; margin-right:0.5rem;">{svg}</span>'

# Data Quality Analysis Class for Lithology
class LithologyDataQualityAnalyzer:
    """Analyze data quality issues for lithology classification"""

    def __init__(self):
        # Define expected ranges for lithology features
        self.parameter_ranges = {
            'GR': (0, 300),        # Gamma Ray (API units)
            'RHOB': (1.0, 3.5),    # Bulk Density (g/cc)
            'NPHI': (-0.1, 1.0),   # Neutron Porosity (v/v)
            'RDEP': (0.1, 10000),  # Deep Resistivity (Ohm·m)
            'DTC': (40, 300),      # Sonic Transit Time (μs/ft)
            'PEF': (0.5, 10.0),    # Photoelectric Factor
            'DEPTH_MD': (0, 10000) # Measured Depth (meters)
        }

        # Expected lithology classes
        self.expected_lithologies = [
            'Sandstone', 'Shale', 'Limestone', 'Dolomite',
            'Anhydrite', 'Salt', 'Coal', 'Marl', 'Mudstone'
        ]

    def analyze_data_quality(self, data, selected_features, target_column=None):
        """
        Comprehensive data quality analysis for lithology data

        Parameters:
        -----------
        data : pd.DataFrame
            Input dataset
        selected_features : list
            List of features to analyze
        target_column : str, optional
            Target column name for lithology labels

        Returns:
        --------
        dict: Dictionary containing quality analysis results
        """
        quality_report = {
            'null_data': pd.DataFrame(),
            'out_of_bounds': pd.DataFrame(),
            'invalid_lithology': pd.DataFrame(),
            'summary_stats': {},
            'recommendations': []
        }

        # Analyze null values
        null_analysis = self._analyze_null_values(data, selected_features, target_column)
        quality_report['null_data'] = null_analysis['null_rows']
        quality_report['summary_stats']['null_summary'] = null_analysis['summary']

        # Analyze out-of-bounds values
        bounds_analysis = self._analyze_out_of_bounds(data, selected_features)
        quality_report['out_of_bounds'] = bounds_analysis['oob_rows']
        quality_report['summary_stats']['bounds_summary'] = bounds_analysis['summary']

        # Analyze lithology labels if target column provided
        if target_column and target_column in data.columns:
            lithology_analysis = self._analyze_lithology_labels(data, target_column)
            quality_report['invalid_lithology'] = lithology_analysis['invalid_rows']
            quality_report['summary_stats']['lithology_summary'] = lithology_analysis['summary']

        # Generate recommendations
        quality_report['recommendations'] = self._generate_recommendations(
            null_analysis, bounds_analysis, len(data), target_column
        )

        return quality_report

    def _analyze_null_values(self, data, features, target_column):
        """Analyze null values in the dataset"""
        null_summary = {}
        null_rows_list = []

        # Analyze features
        for feature in features:
            if feature in data.columns:
                null_mask = data[feature].isnull()
                null_count = null_mask.sum()
                null_percentage = (null_count / len(data)) * 100

                null_summary[feature] = {
                    'count': null_count,
                    'percentage': null_percentage
                }

                if null_count > 0:
                    null_rows = data[null_mask].copy()
                    null_rows['Issue_Type'] = f'Null_{feature}'
                    null_rows['Issue_Description'] = f'Missing value in {feature}'
                    null_rows_list.append(null_rows)

        # Analyze target column if provided
        if target_column and target_column in data.columns:
            null_mask = data[target_column].isnull()
            null_count = null_mask.sum()
            null_percentage = (null_count / len(data)) * 100

            null_summary[target_column] = {
                'count': null_count,
                'percentage': null_percentage
            }

            if null_count > 0:
                null_rows = data[null_mask].copy()
                null_rows['Issue_Type'] = f'Null_{target_column}'
                null_rows['Issue_Description'] = f'Missing lithology label'
                null_rows_list.append(null_rows)

        # Combine all null rows
        if null_rows_list:
            all_null_rows = pd.concat(null_rows_list, ignore_index=True)
        else:
            all_null_rows = pd.DataFrame()

        return {
            'null_rows': all_null_rows,
            'summary': null_summary
        }

    def _analyze_out_of_bounds(self, data, features):
        """Analyze out-of-bounds values in the dataset"""
        bounds_summary = {}
        oob_rows_list = []

        for feature in features:
            if feature in data.columns and feature in self.parameter_ranges:
                min_val, max_val = self.parameter_ranges[feature]

                # Find out-of-bounds values
                oob_mask = (data[feature] < min_val) | (data[feature] > max_val)
                oob_count = oob_mask.sum()
                oob_percentage = (oob_count / len(data)) * 100

                bounds_summary[feature] = {
                    'count': oob_count,
                    'percentage': oob_percentage,
                    'expected_range': f'{min_val} - {max_val}',
                    'actual_range': f'{data[feature].min():.2f} - {data[feature].max():.2f}'
                }

                if oob_count > 0:
                    oob_rows = data[oob_mask].copy()
                    oob_rows['Issue_Type'] = f'OutOfBounds_{feature}'
                    oob_rows['Issue_Description'] = f'{feature} outside range {min_val}-{max_val}'
                    oob_rows['Expected_Range'] = f'{min_val}-{max_val}'
                    oob_rows['Actual_Value'] = data.loc[oob_mask, feature]
                    oob_rows_list.append(oob_rows)

        if oob_rows_list:
            all_oob_rows = pd.concat(oob_rows_list, ignore_index=True)
        else:
            all_oob_rows = pd.DataFrame()

        return {
            'oob_rows': all_oob_rows,
            'summary': bounds_summary
        }

    def _analyze_lithology_labels(self, data, target_column):
        """Analyze lithology label validity"""
        unique_lithologies = data[target_column].dropna().unique()

        # Find invalid lithology labels
        invalid_mask = ~data[target_column].isin(self.expected_lithologies + [np.nan])
        invalid_count = invalid_mask.sum()
        invalid_percentage = (invalid_count / len(data)) * 100

        summary = {
            'unique_count': len(unique_lithologies),
            'invalid_count': invalid_count,
            'invalid_percentage': invalid_percentage,
            'unique_lithologies': list(unique_lithologies),
            'expected_lithologies': self.expected_lithologies
        }

        # Get invalid rows
        if invalid_count > 0:
            invalid_rows = data[invalid_mask].copy()
            invalid_rows['Issue_Type'] = 'Invalid_Lithology'
            invalid_rows['Issue_Description'] = 'Unexpected lithology label'
            invalid_rows['Invalid_Label'] = data.loc[invalid_mask, target_column]
        else:
            invalid_rows = pd.DataFrame()

        return {
            'invalid_rows': invalid_rows,
            'summary': summary
        }

    def _generate_recommendations(self, null_analysis, bounds_analysis, total_rows, target_column):
        """Generate data quality recommendations"""
        recommendations = []

        # Null value recommendations
        for feature, stats in null_analysis['summary'].items():
            if stats['percentage'] > 50:
                recommendations.append(
                    f"[HIGH] {feature}: {stats['percentage']:.1f}% missing values. "
                    f"Consider removing this feature or finding alternative data."
                )
            elif stats['percentage'] > 20:
                recommendations.append(
                    f"[MODERATE] {feature}: {stats['percentage']:.1f}% missing values. "
                    f"Review data collection for this parameter."
                )
            elif stats['percentage'] > 5:
                recommendations.append(
                    f"[INFO] {feature}: {stats['percentage']:.1f}% missing values. "
                    f"Consider imputation strategies."
                )

        # Out-of-bounds recommendations
        for feature, stats in bounds_analysis['summary'].items():
            if stats['percentage'] > 10:
                recommendations.append(
                    f"[CRITICAL] {feature}: {stats['percentage']:.1f}% values outside expected range. "
                    f"Check data calibration and quality."
                )
            elif stats['percentage'] > 1:
                recommendations.append(
                    f"[WARNING] {feature}: {stats['percentage']:.1f}% values outside expected range. "
                    f"Review outliers and data collection."
                )

        # Overall recommendations
        total_issues = len(null_analysis['null_rows']) + len(bounds_analysis['oob_rows'])
        if total_issues > total_rows * 0.3:
            recommendations.append(
                "[CRITICAL] High data quality issues (>30%). Extensive cleaning required."
            )
        elif total_issues > total_rows * 0.1:
            recommendations.append(
                "[WARNING] Moderate data quality issues (>10%). Data cleaning recommended."
            )
        else:
            recommendations.append(
                "[OK] Good data quality. Suitable for machine learning."
            )

        return recommendations

# Page configuration
st.set_page_config(
    page_title="Lithology Classifier",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class LithologyApp:
    def __init__(self):
        self.models = {}
        self.preprocessing_objects = None
        self.evaluation_results = {}
        self.feature_columns = ['GR', 'RHOB', 'NPHI', 'RDEP', 'DTC', 'PEF']

    def _ensure_imputer_compatibility(self, imputer):
        """Ensure SimpleImputer has _fill_dtype for compatibility across sklearn versions."""
        if imputer is None:
            raise ValueError("Imputer cannot be None")

        if hasattr(imputer, '_fill_dtype'):
            return imputer

        if hasattr(imputer, 'statistics_') and imputer.statistics_ is not None:
            try:
                imputer._fill_dtype = imputer.statistics_.dtype
            except Exception:
                imputer._fill_dtype = np.float64
        else:
            imputer._fill_dtype = np.float64

        return imputer

    def smart_column_mapping(self, df):
        """Intelligently map column names to expected feature names"""
        column_mapping = {
            # Gamma Ray variations
            'gamma': 'GR', 'gamma_ray': 'GR', 'gr': 'GR', 'GAMMA': 'GR', 'GAMMA_RAY': 'GR',

            # Bulk Density variations
            'density': 'RHOB', 'bulk_density': 'RHOB', 'rhob': 'RHOB', 'den': 'RHOB',
            'DENSITY': 'RHOB', 'BULK_DENSITY': 'RHOB', 'DEN': 'RHOB',

            # Neutron Porosity variations
            'neutron': 'NPHI', 'neutron_porosity': 'NPHI', 'nphi': 'NPHI', 'neu': 'NPHI',
            'NEUTRON': 'NPHI', 'NEUTRON_POROSITY': 'NPHI', 'NEU': 'NPHI',

            # Deep Resistivity variations
            'resistivity': 'RDEP', 'deep_resistivity': 'RDEP', 'rdep': 'RDEP', 'res': 'RDEP',
            'RESISTIVITY': 'RDEP', 'DEEP_RESISTIVITY': 'RDEP', 'RES': 'RDEP',

            # Delta Time Compressional variations
            'dt': 'DTC', 'delta_time': 'DTC', 'dtc': 'DTC', 'sonic': 'DTC',
            'DT': 'DTC', 'DELTA_TIME': 'DTC', 'SONIC': 'DTC',

            # Photoelectric Factor variations
            'pe': 'PEF', 'photoelectric': 'PEF', 'pef': 'PEF', 'photo': 'PEF',
            'PE': 'PEF', 'PHOTOELECTRIC': 'PEF', 'PHOTO': 'PEF'
        }

        # Create a copy of the dataframe
        df_mapped = df.copy()
        mapping_applied = {}

        # Apply column mapping
        for col in df.columns:
            col_clean = col.strip()
            if col_clean in column_mapping:
                new_name = column_mapping[col_clean]
                if new_name not in df_mapped.columns:  # Avoid duplicate columns
                    df_mapped = df_mapped.rename(columns={col: new_name})
                    mapping_applied[col] = new_name

        return df_mapped, mapping_applied

    def load_models(self):
        """Load trained models and preprocessing objects"""

        # Direct file approach - list directory and filter manually
        model_files = []
        preprocessing_files = []

        with st.expander("Model loading details", expanded=False):
            st.info("Searching for trained models...")

            try:
                if not os.path.exists("model_results"):
                    st.error("model_results directory does not exist!")
                    return False

                # List all files in model_results directory
                all_files = os.listdir("model_results")
                st.info(f"Found {len(all_files)} files in model_results directory")

                # Filter files manually
                for filename in all_files:
                    full_path = os.path.join("model_results", filename)
                    if os.path.isfile(full_path) and filename.endswith('.joblib'):
                        if '_model_' in filename:
                            model_files.append(full_path)
                            st.success(f"Found model: {filename}")
                        elif filename.startswith('preprocessing_objects_'):
                            preprocessing_files.append(full_path)
                            st.success(f"Found preprocessing: {filename}")

                st.info(f"Summary: {len(model_files)} models, {len(preprocessing_files)} preprocessing files")

                # Show all files for debugging
                st.info("**All files in model_results:**")
                for filename in sorted(all_files):
                    full_path = os.path.join("model_results", filename)
                    if os.path.isfile(full_path):
                        file_size = os.path.getsize(full_path)
                        st.write(f"   {filename} ({file_size:,} bytes)")
                    else:
                        st.write(f"   {filename} (directory)")

            except Exception as e:
                st.error(f"Error scanning directory: {str(e)}")
                return False

        if not model_files or not preprocessing_files:
            st.error("No trained models found!")
            st.info("Expected files:")
            st.info("   - Files ending with '_model_YYYYMMDD_HHMMSS.joblib'")
            st.info("   - Files starting with 'preprocessing_objects_'")
            return False

        try:
            # Load latest models
            latest_timestamp = max([f.split('_')[-1].replace('.joblib', '') for f in model_files])
            st.info(f"Using models from timestamp: {latest_timestamp}")

            models_loaded = 0
            for model_file in model_files:
                if latest_timestamp in model_file:
                    # Handle both Windows and Unix path separators
                    filename = os.path.basename(model_file)
                    model_name = filename.split('_model_')[0]

                    st.info(f"Loading {model_name} model from {model_file}")
                    try:
                        self.models[model_name] = joblib.load(model_file)
                    except Exception as e:
                        st.error(f"Model loading failed for {model_name}: {e}. The model may need to be retrained on the current sklearn version.")
                        st.stop()
                    models_loaded += 1

            st.success(f"Loaded {models_loaded} models: {list(self.models.keys())}")

            # Load preprocessing objects
            latest_preprocessing = max(preprocessing_files, key=os.path.getctime)
            st.info(f"Loading preprocessing objects from {latest_preprocessing}")
            try:
                self.preprocessing_objects = joblib.load(latest_preprocessing)
            except Exception as e:
                st.error(f"Preprocessing objects loading failed: {e}. The preprocessing objects may need to be regenerated on the current sklearn version.")
                st.stop()

            # Load evaluation results if available
            eval_files = glob.glob("model_results/evaluation_results_*.json")
            if eval_files:
                latest_eval = max(eval_files, key=os.path.getctime)
                with open(latest_eval, 'r') as f:
                    self.evaluation_results = json.load(f)
                st.info(f"Loaded evaluation results from {latest_eval}")

            return True

        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            st.error(f"Error details: {type(e).__name__}")
            import traceback
            st.code(traceback.format_exc())
            return False

    def preprocess_data(self, df):
        """Preprocess input data using saved preprocessing objects"""
        if self.preprocessing_objects is None:
            raise ValueError("Preprocessing objects not loaded")

        # Extract available features
        available_features = [col for col in self.feature_columns if col in df.columns]

        if len(available_features) < 3:
            raise ValueError(f"Insufficient features. Need at least 3, got {len(available_features)}")

        X = df[available_features].copy()

        # Apply preprocessing
        self.preprocessing_objects['imputer'] = self._ensure_imputer_compatibility(self.preprocessing_objects['imputer'])

        X_imputed = pd.DataFrame(
            self.preprocessing_objects['imputer'].transform(X),
            columns=available_features,
            index=X.index
        )

        X_scaled = pd.DataFrame(
            self.preprocessing_objects['scaler'].transform(X_imputed),
            columns=available_features,
            index=X_imputed.index
        )

        return X_scaled, available_features

    def predict(self, df, model_name='random_forest'):
        """Make predictions on input data"""
        X_processed, features = self.preprocess_data(df)

        model = self.models[model_name]
        predictions = model.predict(X_processed)
        probabilities = model.predict_proba(X_processed)

        # Decode predictions
        label_encoder = self.preprocessing_objects['label_encoder']
        predicted_labels = label_encoder.inverse_transform(predictions)

        return {
            'predictions': predicted_labels,
            'probabilities': probabilities,
            'class_names': label_encoder.classes_,
            'features_used': features
        }

def main():
    # Header
    st.markdown(f'{icon("rock")} <span style="font-size:2rem; font-weight:700;">Lithology Classification System</span>',
                unsafe_allow_html=True)

    # Sidebar debug toggle (hidden by default)
    show_debug = st.sidebar.checkbox("Show debug info", value=False,
                                     help="Toggle path/debug details")
    if show_debug:
        with st.sidebar.expander("Debug Info", expanded=False):
            st.write(f"Current directory: {os.getcwd()}")
            st.write(f"Model results exists: {os.path.exists('model_results')}")

    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Predict lithology classes from well log data using advanced ML models<br>
            Features: GR, RHOB, NPHI, RDEP, DTC, PEF | Models: Random Forest & XGBoost
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize app
    app = LithologyApp()

    # Sidebar
    st.sidebar.header("Configuration")

    # Load models
    if st.sidebar.button("Load Models", type="primary"):
        with st.spinner("Loading trained models..."):
            if app.load_models():
                # Store models and preprocessing objects in session state
                st.session_state.models_loaded = True
                st.session_state.app_models = app.models
                st.session_state.app_preprocessing = app.preprocessing_objects
                st.session_state.app_evaluation = app.evaluation_results
                st.sidebar.success("Models loaded successfully!")
                st.rerun()  # Refresh to show loaded models
            else:
                st.session_state.models_loaded = False

    # Auto-load models if not already loaded
    if not hasattr(st.session_state, 'models_loaded') or not st.session_state.models_loaded:
        st.info("Auto-loading trained models...")
        with st.spinner("Loading trained models..."):
            if app.load_models():
                # Store models and preprocessing objects in session state
                st.session_state.models_loaded = True
                st.session_state.app_models = app.models
                st.session_state.app_preprocessing = app.preprocessing_objects
                st.session_state.app_evaluation = app.evaluation_results
                st.success("Models loaded successfully!")
                st.rerun()  # Refresh the app to show the loaded models
            else:
                st.warning("Could not auto-load models. Please use the 'Load Models' button in the sidebar.")
                st.info("Tip: Make sure you have run the training pipeline: `python lithology_ml_pipeline.py`")
                return
    else:
        # Restore models from session state
        if hasattr(st.session_state, 'app_models'):
            app.models = st.session_state.app_models
            app.preprocessing_objects = st.session_state.app_preprocessing
            app.evaluation_results = st.session_state.app_evaluation

    # Model selection
    if app.models:
        selected_model = st.sidebar.selectbox(
            "Select Model",
            list(app.models.keys()),
            help="Choose which trained model to use for predictions"
        )
    else:
        st.error("No models available")
        return

    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["Data Upload & Prediction", "Visualizations",
                                      "Model Performance", "Export Results"])

    with tab1:
        st.markdown(f"{icon('upload')} <strong>Upload Well Log Data</strong>", unsafe_allow_html=True)

        # File upload
        uploaded_file = st.file_uploader(
            "Choose a CSV file with well log data",
            type=['csv'],
            help="Upload a CSV file containing well log measurements"
        )

        if uploaded_file is not None:
            try:
                # Smart CSV loading with different separators
                df = None
                separators = [',', ';', '\t', '|']

                for sep in separators:
                    try:
                        df_test = pd.read_csv(uploaded_file, sep=sep, nrows=5, on_bad_lines='skip')
                        if df_test.shape[1] > 1:  # More than one column means good separator
                            uploaded_file.seek(0)  # Reset file pointer
                            df = pd.read_csv(uploaded_file, sep=sep, on_bad_lines='skip')
                            st.info(f"Detected separator: '{sep}' | Columns: {df.shape[1]}")
                            if df.shape[0] < df_test.shape[0] * 100:  # Warn if many lines were skipped
                                st.warning("Some malformed lines were skipped during parsing")
                            break
                        uploaded_file.seek(0)  # Reset file pointer for next attempt
                    except Exception as e:
                        uploaded_file.seek(0)  # Reset file pointer
                        continue

                if df is None:
                    # Fallback to comma separator
                    df = pd.read_csv(uploaded_file, on_bad_lines='skip')
                    st.warning("Using default comma separator")

                st.success(f"Data loaded successfully! Shape: {df.shape}")

                # Apply smart column mapping
                df_mapped, mapping_applied = app.smart_column_mapping(df)

                if mapping_applied:
                    st.info("**Column Mapping Applied:**")
                    for old_name, new_name in mapping_applied.items():
                        st.write(f"   '{old_name}' -> '{new_name}'")
                    df = df_mapped  # Use the mapped dataframe

                # Display data preview
                st.subheader("Data Preview")
                st.dataframe(df.head(10))

                # Data Quality Analysis
                st.subheader("Data Quality Analysis")

                # Initialize quality analyzer
                quality_analyzer = LithologyDataQualityAnalyzer()

                # Perform quality analysis
                analysis_features = ['GR', 'RHOB', 'NPHI', 'RDEP', 'DTC', 'PEF', 'DEPTH_MD']
                analysis_features = [col for col in analysis_features if col in df.columns]

                # Check if target column exists for training data
                target_column = None
                possible_targets = ['FORCE_2020_LITHOFACIES_LITHOLOGY', 'Lithology', 'LITHOLOGY', 'lithology']
                for col in possible_targets:
                    if col in df.columns:
                        target_column = col
                        break

                quality_report = quality_analyzer.analyze_data_quality(df, analysis_features, target_column)

                # Display quality metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_null_rows = len(quality_report['null_data'])
                    st.metric("Rows with Null Values", f"{total_null_rows:,}")
                with col2:
                    total_oob_rows = len(quality_report['out_of_bounds'])
                    st.metric("Out-of-Bounds Rows", f"{total_oob_rows:,}")
                with col3:
                    total_invalid_lithology = len(quality_report['invalid_lithology'])
                    st.metric("Invalid Lithology Labels", f"{total_invalid_lithology:,}")
                with col4:
                    total_issues = total_null_rows + total_oob_rows + total_invalid_lithology
                    data_quality_score = max(0, 100 - (total_issues / len(df) * 100))
                    st.metric("Data Quality Score", f"{data_quality_score:.1f}%")

                # Quality recommendations
                if quality_report['recommendations']:
                    st.write("**Data Quality Recommendations:**")
                    for recommendation in quality_report['recommendations']:
                        if "[CRITICAL]" in recommendation or "[HIGH]" in recommendation:
                            st.error(recommendation)
                        elif "[WARNING]" in recommendation or "[MODERATE]" in recommendation:
                            st.warning(recommendation)
                        elif "[OK]" in recommendation:
                            st.success(recommendation)
                        else:
                            st.info(recommendation)

                # Download options for quality issues
                download_col1, download_col2, download_col3 = st.columns(3)

                with download_col1:
                    if not quality_report['null_data'].empty:
                        null_csv = quality_report['null_data'].to_csv(index=False)
                        st.download_button(
                            label="Download Null Data",
                            data=null_csv,
                            file_name=f"lithology_null_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            help="Download rows with missing values"
                        )
                    else:
                        st.info("No null values")

                with download_col2:
                    if not quality_report['out_of_bounds'].empty:
                        oob_csv = quality_report['out_of_bounds'].to_csv(index=False)
                        st.download_button(
                            label="Download Out-of-Bounds",
                            data=oob_csv,
                            file_name=f"lithology_oob_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            help="Download rows with values outside expected ranges"
                        )
                    else:
                        st.info("No out-of-bounds values")

                with download_col3:
                    if not quality_report['invalid_lithology'].empty:
                        invalid_csv = quality_report['invalid_lithology'].to_csv(index=False)
                        st.download_button(
                            label="Download Invalid Lithology",
                            data=invalid_csv,
                            file_name=f"lithology_invalid_labels_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            help="Download rows with unexpected lithology labels"
                        )
                    else:
                        st.info("No invalid labels")

                # Detailed quality analysis
                with st.expander("Detailed Quality Analysis", expanded=False):

                    # Null values analysis
                    if quality_report['summary_stats']['null_summary']:
                        st.write("**Null Values Analysis:**")
                        null_df = pd.DataFrame.from_dict(
                            quality_report['summary_stats']['null_summary'],
                            orient='index'
                        )
                        null_df.index.name = 'Feature'
                        null_df = null_df.reset_index()
                        st.dataframe(null_df, use_container_width=True)

                    # Out-of-bounds analysis
                    if quality_report['summary_stats']['bounds_summary']:
                        st.write("**Out-of-Bounds Analysis:**")
                        bounds_df = pd.DataFrame.from_dict(
                            quality_report['summary_stats']['bounds_summary'],
                            orient='index'
                        )
                        bounds_df.index.name = 'Feature'
                        bounds_df = bounds_df.reset_index()
                        st.dataframe(bounds_df, use_container_width=True)

                    # Lithology analysis
                    if 'lithology_summary' in quality_report['summary_stats']:
                        st.write("**Lithology Labels Analysis:**")
                        lith_summary = quality_report['summary_stats']['lithology_summary']
                        st.write(f"- Unique lithologies found: {lith_summary['unique_count']}")
                        st.write(f"- Invalid labels: {lith_summary['invalid_count']} ({lith_summary['invalid_percentage']:.1f}%)")

                        if lith_summary['unique_lithologies']:
                            st.write("**Found lithologies:**")
                            for lith in sorted(lith_summary['unique_lithologies']):
                                if pd.notna(lith):
                                    st.write(f"  - {lith}")

                # Check available features
                available_features = [col for col in app.feature_columns if col in df.columns]
                missing_features = [col for col in app.feature_columns if col not in df.columns]

                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Available Features:**")
                    for feature in available_features:
                        st.write(f"   - {feature}")

                with col2:
                    if missing_features:
                        st.write("**Missing Features:**")
                        for feature in missing_features:
                            st.write(f"   - {feature}")

                # Show column suggestions if no features found
                if len(available_features) == 0:
                    st.warning("**No standard features detected. Available columns:**")
                    cols_display = st.columns(3)
                    for i, col in enumerate(df.columns[:15]):  # Show first 15 columns
                        with cols_display[i % 3]:
                            st.write(f"- {col}")

                    if len(df.columns) > 15:
                        st.write(f"... and {len(df.columns) - 15} more columns")

                    st.info("**Tip:** The app looks for columns named: GR, RHOB, NPHI, RDEP, DTC, PEF")
                    st.info("**Auto-mapping:** Common variations are automatically mapped (e.g., 'gamma' -> 'GR')")

                # Make predictions
                if len(available_features) >= 3:
                    if st.button("Make Predictions", type="primary"):
                        with st.spinner("Making predictions..."):
                            try:
                                results = app.predict(df, selected_model)

                                # Add predictions to dataframe
                                df_results = df.copy()
                                df_results['Predicted_Lithology'] = results['predictions']
                                df_results['Max_Probability'] = np.max(results['probabilities'], axis=1)

                                st.session_state.prediction_results = df_results
                                st.session_state.prediction_data = results

                                st.success("Predictions completed!")

                                # Display results
                                st.subheader("Prediction Results")
                                st.dataframe(df_results[['Predicted_Lithology', 'Max_Probability'] +
                                           available_features].head(20))

                                # Summary statistics
                                st.subheader("Prediction Summary")
                                lith_counts = pd.Series(results['predictions']).value_counts()

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total Samples", len(df_results))
                                with col2:
                                    st.metric("Unique Lithologies", len(lith_counts))
                                with col3:
                                    avg_confidence = np.mean(np.max(results['probabilities'], axis=1))
                                    st.metric("Avg Confidence", f"{avg_confidence:.3f}")

                            except Exception as e:
                                st.error(f"Prediction error: {str(e)}")
                else:
                    st.error(f"Insufficient features. Need at least 3, got {len(available_features)}")

            except Exception as e:
                st.error(f"Error loading file: {str(e)}")

    with tab2:
        st.markdown(f"{icon('chart')} <strong>Interactive Visualizations</strong>", unsafe_allow_html=True)

        if hasattr(st.session_state, 'prediction_results'):
            df_results = st.session_state.prediction_results
            results = st.session_state.prediction_data

            # Lithology distribution
            st.subheader("Lithology Distribution")
            lith_counts = pd.Series(results['predictions']).value_counts()

            fig_pie = px.pie(
                values=lith_counts.values,
                names=lith_counts.index,
                title="Predicted Lithology Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # Depth vs Lithology (if depth column exists)
            if 'DEPTH_MD' in df_results.columns:
                st.subheader("Lithology vs Depth")

                fig_depth = px.scatter(
                    df_results,
                    x='Predicted_Lithology',
                    y='DEPTH_MD',
                    color='Max_Probability',
                    title="Lithology Predictions vs Depth",
                    color_continuous_scale='Viridis'
                )
                fig_depth.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_depth, use_container_width=True)

            # Feature correlation with predictions
            st.subheader("Feature Analysis")
            available_features = results['features_used']

            if len(available_features) >= 2:
                feature_x = st.selectbox("X-axis feature", available_features)
                feature_y = st.selectbox("Y-axis feature", available_features, index=1)

                fig_scatter = px.scatter(
                    df_results,
                    x=feature_x,
                    y=feature_y,
                    color='Predicted_Lithology',
                    title=f"{feature_x} vs {feature_y} colored by Lithology"
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Upload data and make predictions to see visualizations")

    with tab3:
        st.markdown(f"{icon('metrics')} <strong>Model Performance Metrics</strong>", unsafe_allow_html=True)

        if hasattr(app, 'evaluation_results') and app.evaluation_results:
            st.subheader("Model Comparison")

            # Create comparison dataframe
            comparison_data = []
            for model_name, metrics in app.evaluation_results.items():
                comparison_data.append({
                    'Model': model_name.replace('_', ' ').title(),
                    'Accuracy': f"{metrics['accuracy']:.4f}",
                    'Precision': f"{metrics['precision']:.4f}",
                    'Recall': f"{metrics['recall']:.4f}",
                    'F1-Score': f"{metrics['f1_score']:.4f}"
                })

            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)

            # Best model highlight
            best_model = max(app.evaluation_results.keys(),
                           key=lambda x: app.evaluation_results[x]['f1_score'])
            best_f1 = app.evaluation_results[best_model]['f1_score']

            st.markdown(f"""
            <div class="success-box">
                <h4>Best Performing Model</h4>
                <p><strong>{best_model.replace('_', ' ').title()}</strong> with F1-Score: <strong>{best_f1:.4f}</strong></p>
            </div>
            """, unsafe_allow_html=True)

            # Performance metrics visualization
            st.subheader("Performance Comparison Chart")

            metrics_df = pd.DataFrame(app.evaluation_results).T
            metrics_df.index = [idx.replace('_', ' ').title() for idx in metrics_df.index]

            fig_metrics = px.bar(
                metrics_df.reset_index(),
                x='index',
                y=['accuracy', 'precision', 'recall', 'f1_score'],
                title="Model Performance Comparison",
                labels={'index': 'Model', 'value': 'Score', 'variable': 'Metric'},
                barmode='group'
            )
            fig_metrics.update_layout(xaxis_title="Model", yaxis_title="Score")
            st.plotly_chart(fig_metrics, use_container_width=True)

        else:
            st.info("No evaluation results loaded. Please load models first using the sidebar.")

    with tab4:
        st.markdown(f"{icon('download')} <strong>Export Prediction Results</strong>", unsafe_allow_html=True)

        if hasattr(st.session_state, 'prediction_results'):
            df_results = st.session_state.prediction_results

            st.subheader("Download Options")

            # CSV export
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"lithology_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

            # Summary report
            summary_report = {
                'timestamp': datetime.now().isoformat(),
                'model_used': selected_model,
                'total_samples': len(df_results),
                'lithology_distribution': pd.Series(st.session_state.prediction_data['predictions']).value_counts().to_dict(),
                'average_confidence': float(np.mean(df_results['Max_Probability']))
            }

            st.download_button(
                label="Download Summary Report",
                data=json.dumps(summary_report, indent=2),
                file_name=f"prediction_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        else:
            st.info("Make predictions first to enable export options")

if __name__ == "__main__":
    main()
