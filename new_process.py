if __name__ == "__main__":
	launch_process(DUBIOUS_DATA_CSV, "process-dubious-", DUBIOUS_DATA_DIR)
	launch_process(TYPICAL_DATA_CSV, "process-typical-", TYPICAL_DATA_DIR)