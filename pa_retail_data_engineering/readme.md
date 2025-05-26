# Data Engineering Pipeline

This pipeline performs an Extract, Transform, and Load (ETL) process on structured JSON files to produce normalized CSV outputs.

## 1. Configure the Pipeline

Open the `Makefile` and set the following variables:

* `START_PATH`: Path to the root directory containing your original JSON files.
* `OUTPUT_PATH`: Path where the generated CSV files will be saved.

Example:

```makefile
START_PATH  ?= ./original_datasets
OUTPUT_PATH ?= ./data_output
```

## 2. Run the Pipeline

### For a single JSON file (interactive mode)

Use this mode to manually extract, transform, and load a specific file:

```bash
make run
```

You will be prompted to navigate through directories, select a file, and run each ETL stage interactively.

### For all JSON files (batch mode)

Use this command to automatically process all `.json` files across all subdirectories under `START_PATH`:

```bash
make load_all
```
