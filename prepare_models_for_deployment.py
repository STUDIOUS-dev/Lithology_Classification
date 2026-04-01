#!/usr/bin/env python3
"""
Model Preparation Script for Deployment

This script helps prepare your trained models for cloud deployment by:
1. Creating ZIP archives of model files
2. Providing upload instructions for various cloud services
3. Generating direct download links

Usage:
    python prepare_models_for_deployment.py
"""

import os
import zipfile
from pathlib import Path
import shutil

def create_model_archives():
    """Create ZIP archives of models and model_results directories"""

    base_dir = Path(__file__).resolve().parent

    # Check if directories exist
    models_dir = base_dir / "models"
    model_results_dir = base_dir / "model_results"

    if not models_dir.exists():
        print("❌ models/ directory not found!")
        return False

    if not model_results_dir.exists():
        print("❌ model_results/ directory not found!")
        return False

    # Create archives
    archives_created = []

    # Archive models directory
    models_zip = base_dir / "models_archive.zip"
    print("📦 Creating models archive...")
    with zipfile.ZipFile(models_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in models_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(models_dir)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

    archives_created.append(("models", models_zip))

    # Archive model_results directory
    results_zip = base_dir / "model_results_archive.zip"
    print("📦 Creating model_results archive...")
    with zipfile.ZipFile(results_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in model_results_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(model_results_dir)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

    archives_created.append(("model_results", results_zip))

    return archives_created

def get_file_sizes(archives):
    """Get file sizes for the created archives"""
    sizes = {}
    for name, path in archives:
        size_bytes = path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        sizes[name] = f"{size_mb:.1f} MB"
    return sizes

def print_upload_instructions(archives):
    """Print instructions for uploading to various cloud services"""

    print("\n" + "="*60)
    print("📤 UPLOAD INSTRUCTIONS")
    print("="*60)

    sizes = get_file_sizes(archives)

    for name, archive_path in archives:
        print(f"\n🔹 {name.upper()} ARCHIVE: {archive_path.name} ({sizes[name]})")
        print("-" * 40)

        print("📁 Upload to one of these services:")
        print("  • Google Drive: Upload file, right-click → 'Get shareable link'")
        print("  • Dropbox: Upload file, right-click → 'Copy link'")
        print("  • GitHub Releases: Create release, upload as asset")
        print("  • Any direct download service")

        print("\n🔗 Get DIRECT download link:")
        print("  • Google Drive: Change 'https://drive.google.com/file/d/FILE_ID/view'")
        print("    to 'https://drive.google.com/uc?export=download&id=FILE_ID'")
        print("  • Dropbox: Change 'https://www.dropbox.com/s/.../file.zip?dl=0'")
        print("    to 'https://www.dropbox.com/s/.../file.zip?dl=1'")
        print("  • GitHub: Use the download URL from releases")

def update_download_script(archives):
    """Update the download_models.py script with placeholder comments"""

    script_path = Path(__file__).resolve().parent / "download_models.py"

    if not script_path.exists():
        print("⚠️  download_models.py not found, skipping update")
        return

    print("
📝 Update download_models.py:"    print("  1. Open download_models.py")
    print("  2. Find the MODELS_URL and MODEL_RESULTS_URL variables")
    print("  3. Replace with your direct download links")

    for name, archive_path in archives:
        var_name = "MODELS_URL" if name == "models" else "MODEL_RESULTS_URL"
        print(f"  4. Set {var_name} = 'YOUR_{name.upper()}_DOWNLOAD_URL_HERE'")

def main():
    print("🤖 Model Preparation for Deployment")
    print("=" * 50)

    # Create archives
    archives = create_model_archives()

    if not archives:
        print("❌ Failed to create model archives!")
        return

    print("
✅ Archives created successfully!"    for name, path in archives:
        print(f"  • {path}")

    # Print upload instructions
    print_upload_instructions(archives)

    # Update script instructions
    update_download_script(archives)

    print("\n" + "="*60)
    print("🎯 NEXT STEPS")
    print("="*60)
    print("1. Upload the ZIP files to your preferred cloud storage")
    print("2. Get direct download links (see instructions above)")
    print("3. Update download_models.py with the URLs")
    print("4. Test locally: python download_models.py")
    print("5. Deploy to Streamlit Cloud - models will download automatically!")
    print("\n🚀 Your app is now ready for deployment!")

if __name__ == "__main__":
    main()