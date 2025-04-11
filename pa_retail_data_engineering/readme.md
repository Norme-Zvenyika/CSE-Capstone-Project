# Data Engineering Pipeline

This pipeline performs an Extract, Transform, and Load (ETL) process on your JSON files. Follow the steps below to configure and run it:

1. **Configure the Pipeline:**
   - Open the file: `admin/__main__.py`.
   - Locate the `start_path` variable.
   - Set `start_path` to the directory path where your original JSON files are stored.

2. **Run the Pipeline:**
   - Once `start_path` is configured, execute the `python3 -m admin` to run the script in the admin directory.
   - The script will automatically process the JSON files through the ETL pipeline.