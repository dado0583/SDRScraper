

# Monitor: main entry point. Called once per day per type of files?

# Orchestrator: Calls the monitor each day for each type of file

# Provider: Sources the data from the source files

# Sources: lists the sources for the files

# Writer: Will write to S3, and let the orchestrator know what the lastest value is. 
  # Writer handles resumes. Write multiple files?

TODO: Resume functionality...