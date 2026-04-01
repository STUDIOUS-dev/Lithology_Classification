#!/usr/bin/env python3
"""
Model Download Script for Lithology Classification App

This script downloads trained ML models from cloud storage to enable
deployment on platforms that don't support large files in git repositories.

Usage:
    python download_models.py

Requirements:
    pip install requests

Supported storage services:
    - Google Drive (direct download links)
    - Dropbox (direct download links)
    - GitHub Releases
    - Any direct HTTP download URL
"""

import os
import sys
import requests
from pathlib import Path
import zipfile
import tarfile
import shutil
from urllib.parse import urlparse

class ModelDownloader:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parent
        self.models_dir = self.base_dir / "models"
        self.model_results_dir = self.base_dir / "model_results"

    def download_file(self, url, destination_path, chunk_size=8192):
        """Download a file from URL to destination path with progress."""
        try:
            print(f"Downloading from: {url}")
            print(f"Saving to: {destination_path}")

            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))

            with open(destination_path, 'wb') as file:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(".1f", end='', flush=True)

            print(" - Download complete!")
            return True

        except Exception as e:
            print(f"Download failed: {e}")
            return False

    def extract_archive(self, archive_path, extract_to):
        """Extract zip or tar.gz archives."""
        try:
            print(f"Extracting {archive_path} to {extract_to}")

            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif archive_path.suffixes == ['.tar', '.gz'] or archive_path.suffix == '.tgz':
                with tarfile.open(archive_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(extract_to)
            else:
                print(f"Unsupported archive format: {archive_path}")
                return False

            print("Extraction complete!")
            return True

        except Exception as e:
            print(f"Extraction failed: {e}")
            return False

    def download_models_archive(self, models_url, results_url=None):
        """Download and extract model archives."""

        # Create directories
        self.models_dir.mkdir(exist_ok=True)
        if results_url:
            self.model_results_dir.mkdir(exist_ok=True)

        # Download models
        models_archive = self.base_dir / "models_temp.zip"
        if self.download_file(models_url, models_archive):
            if self.extract_archive(models_archive, self.models_dir):
                print("Models downloaded and extracted successfully!")
            else:
                print("Failed to extract models archive")
                return False
        else:
            print("Failed to download models archive")
            return False

        # Clean up temp file
        if models_archive.exists():
            models_archive.unlink()

        # Download model results if provided
        if results_url:
            results_archive = self.base_dir / "model_results_temp.zip"
            if self.download_file(results_url, results_archive):
                if self.extract_archive(results_archive, self.model_results_dir):
                    print("Model results downloaded and extracted successfully!")
                else:
                    print("Failed to extract model results archive")
                    return False
            else:
                print("Failed to download model results archive")
                return False

            # Clean up temp file
            if results_archive.exists():
                results_archive.unlink()

        return True

    def verify_models(self):
        """Verify that required model files exist."""
        required_files = [
            "models/lithology_model.joblib",
            "models/lithology_preprocessing.joblib",
            "models/xgboost_model.joblib"
        ]

        missing_files = []
        for file_path in required_files:
            full_path = self.base_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)

        if missing_files:
            print("Missing model files:")
            for file in missing_files:
                print(f"  - {file}")
            return False

        print("All required model files are present!")
        return True

def main():
    """Main download function - configure URLs here."""

    downloader = ModelDownloader()

    # Configuration - UPDATE THESE URLs
    # You need to upload your model archives to a cloud service and get direct download links

    MODELS_URL = "YOUR_MODELS_ARCHIVE_URL_HERE"  # e.g., Google Drive direct link
    MODEL_RESULTS_URL = "YOUR_MODEL_RESULTS_ARCHIVE_URL_HERE"  # Optional

    print("Lithology Classification Model Downloader")
    print("=" * 50)

    if MODELS_URL == "YOUR_MODELS_ARCHIVE_URL_HERE":
        print("ERROR: Please configure the download URLs in this script!")
        print("\nSteps to configure:")
        print("1. Upload your 'models/' folder as a ZIP archive to Google Drive/Dropbox/etc.")
        print("2. Get the direct download link")
        print("3. Replace YOUR_MODELS_ARCHIVE_URL_HERE with the actual URL")
        print("4. Optionally do the same for model_results/")
        print("5. Run this script again")
        sys.exit(1)

    print("Starting model download...")

    if downloader.download_models_archive(MODELS_URL, MODEL_RESULTS_URL):
        if downloader.verify_models():
            print("\n✅ All models downloaded and verified successfully!")
            print("You can now run the Streamlit app.")
        else:
            print("\n❌ Model verification failed!")
            sys.exit(1)
    else:
        print("\n❌ Model download failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()