import os

# Create GitHub Workflow folder
os.makedirs(".github/workflows", exist_ok=True)

workflow_yaml = """name: Build Dev AI APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install --upgrade buildozer cython

    - name: Build APK with Buildozer
      run: |
        buildozer android debug

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v3
      with:
        name: DevAI-APK
        path: bin/*.apk
"""

with open(".github/workflows/build.yml", "w") as f:
    f.write(workflow_yaml)

print("✅ GitHub Action Workflow generated successfully.")
