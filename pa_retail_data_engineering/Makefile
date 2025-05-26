PYTHON      := python3
START_PATH  ?= ./original_datasets
OUTPUT_PATH ?= ./datafiles

.PHONY: run load_all zip_datafiles
run:
	@echo ">> running data-pipeline"
	@echo ">> start-path:  $(strip $(START_PATH))"
	@echo ">> output-path: $(strip $(OUTPUT_PATH))"
	@$(PYTHON) -m admin \
		--start-path "$(strip $(START_PATH))" \
		--output-path "$(strip $(OUTPUT_PATH))"

load_all:
	@echo ">> ETL for all json files"
	@echo ">> start-path:  $(strip $(START_PATH))"
	@echo ">> output-path: $(strip $(OUTPUT_PATH))"
	@$(PYTHON) -m admin \
		--start-path ../pa_retail_data_engineering/original_datasets \
		--output-path "$(strip $(OUTPUT_PATH))" \
		--auto-load-all

zip_datafiles:
	zip -r cleaned_datafiles.zip datafiles
