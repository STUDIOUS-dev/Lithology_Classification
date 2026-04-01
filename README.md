# <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/mountain.svg" width="28" height="28" style="vertical-align: middle;"> Lithology Classification ML Pipeline

Welcome! This is a production-ready machine learning pipeline I've developed to classify lithology from well log data. Whether you're dealing with standard FORCE 2020 datasets or custom regional logs, this tool is designed to handle the "messy" reality of geoscience data—cleaning, imputing, and predicting with high confidence.

## <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/rocket.svg" width="24" height="24" style="vertical-align: middle;"> What is this?

This project takes raw geophysical well logs (like Gamma Ray, Resistivity, and Density) and uses trained ML models (Random Forest, Extra Trees, or XGBoost) to predict rock types automatically. 

I built this with a focus on **transparency** and **usability**. It's not just a black box; it gives you detailed quality reports, confidence scores, and interactive visualizations to help you understand *why* a certain lithology was predicted.

## <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/sparkles.svg" width="24" height="24" style="vertical-align: middle;"> Key Features

- **Smart Column Mapping**: Don't worry about exact column names. The app automatically recognizes variations like `GR`, `Gamma`, `gamma_ray`, etc.
- **Data Quality Analyzer**: Automatically flags null values, out-of-bounds geophysical readings, and invalid labels before they mess up your predictions.
- **Interactive Streamlit UI**: A clean, modern dashboard for uploading data, tweaking model settings, and visualizing results in real-time.
- **Robust Preprocessing**: Built-in automated imputation and scaling to ensure your data is always model-ready.
- **Model Transparency**: Deep dives into confusion matrices, error analysis, and feature importance.
- **Batch Export**: Run predictions on entire wells and export the results (with confidence scores) to CSV for use in Petrel or Techlog.

## <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/wrench.svg" width="24" height="24" style="vertical-align: middle;"> Setup and Installation

Getting started is straightforward. This project uses pip-tools for reproducible dependency management.

### For Development/Local Use:
```bash
# Clone the repository
git clone https://github.com/yourusername/04_Lithology_Classification_ML.git
cd 04_Lithology_Classification_ML

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux

# Install pip-tools and compile dependencies
pip install pip-tools
pip-compile requirements.in

# Install the compiled requirements
pip install -r requirements.txt
```

### For Streamlit Community Cloud Deployment:
The project is configured for seamless deployment to Streamlit Community Cloud:
- `runtime.txt`: Pins Python version to 3.12 to match the compiled requirements and local environment
- `requirements.in`: Defines flexible version ranges for maintainability
- `requirements.txt`: Auto-generated exact pins for reproducible builds

**Model Deployment Setup:**
Since model files are large (~4GB), they are not stored in the git repository. Instead, the app automatically downloads them from cloud storage on first run:

1. **Upload your trained models** to cloud storage (Google Drive, Dropbox, GitHub Releases, etc.)
2. **Get direct download links** for your model archives
3. **Configure `download_models.py`** with your URLs
4. **Deploy to Streamlit Cloud** - models will download automatically

Simply push to GitHub and deploy - the app handles model setup automatically!

## <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/line-chart.svg" width="24" height="24" style="vertical-align: middle;"> How to Use

### 1. Launch the Dashboard
Run the Streamlit app to start the interactive interface:
```bash
streamlit run lithology_streamlit_app.py
```

### 2. Upload Your Data
Drop in a CSV file. The app currently looks for these features:
- **GR** (Gamma Ray)
- **RHOB** (Bulk Density)
- **NPHI** (Neutron Porosity)
- **RDEP** (Deep Resistivity)
- **DTC** (Sonic Transit Time)
- **PEF** (Photoelectric Factor)

### 3. Predict & Analyze
Choose your model (Random Forest is usually a safe bet for reliability) and watch the results roll in. You can explore the "Visualizations" tab to see how the predictions align with your depth logs.

## <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/folder.svg" width="24" height="24" style="vertical-align: middle;"> Project Structure

- `lithology_streamlit_app.py`: The heart of the project—the interactive UI.
- `download_models.py`: Script to download trained models from cloud storage.
- `litho_data/`: Place your training/testing CSVs here.
- `models/`: Directory for trained `.joblib` artifacts (downloaded automatically, not in repo).
- `model_results/`: Directory for evaluation reports and model files (downloaded automatically, not in repo).
- `requirements.in`: Flexible dependency ranges for maintainability.
- `requirements.txt`: Auto-generated exact pins for reproducible builds.
- `runtime.txt`: Python version pinning for Streamlit Cloud deployment.
- `archive_unused/`: Legacy code and unused files.

## <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/binary.svg" width="24" height="24" style="vertical-align: middle;"> Technical Note: Using the Models in Python

If you want to use the trained models directly in your own scripts:

```python
from joblib import load

# Load the model and preprocessing pipeline
obj = load('models/lithology_model_LATEST.joblib')
model = obj.get('model', obj)

preproc = load('models/lithology_preprocessing_LATEST.joblib')
scaler = preproc['scaler']
imputer = preproc['imputer']

# Your inference code here...
```

## <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/help-circle.svg" width="24" height="24" style="vertical-align: middle;"> Troubleshooting

### Model Download Issues
If models fail to download automatically:

1. **Check your internet connection** - The app needs to download ~4GB of model files
2. **Verify download URLs** in `download_models.py` are accessible
3. **Use manual download** - Run `python download_models.py` locally first
4. **Check file permissions** - Ensure write access to the project directory

### Common Deployment Issues
- **"model_results directory does not exist!"** - Models haven't downloaded yet. Wait for download or use manual download.
- **Import errors** - Ensure `pip install -r requirements.txt` completed successfully
- **Memory issues** - The models require ~8GB RAM for loading. Reduce batch size if needed.

### Model Compatibility
- Models were trained on scikit-learn and XGBoost
- If you get sklearn version mismatch errors, retrain models with current versions
- All preprocessing steps are saved and applied automatically

---
*Built for the ONGC Petrophysical Analysis Team | 2025*
