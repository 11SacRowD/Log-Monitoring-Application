import random
import string
import itertools
import sys
import os
# Job types
SCHEDULED_TASK = "scheduled task"
BACKGROUND_JOB = "background job"

LOWERCASE_ALPHABET = string.ascii_lowercase

def generate_job_PIDS(num_jobs):
    return random.sample(range(10000, 100000), num_jobs)

def generate_job_descriptions(num_jobs):
    
    # Used to generate a psuedo-random distribution of job types
    scheduled_task_fraction = round(random.uniform(0.3, 0.7), 2)
    
    num_scheduled_tasks = int(num_jobs * scheduled_task_fraction)
    num_background_tasks = num_jobs - num_scheduled_tasks
    
    task_numbers = random.sample(range(100, 1000), num_scheduled_tasks)
    job_codes = random.sample(list(itertools.combinations(LOWERCASE_ALPHABET, 3)), num_background_tasks)
    
    # Generate job descriptions, shuffling them to better emulate a log
    job_description_array = []
    for i in range(num_scheduled_tasks):
        job_description_array.append(f"{SCHEDULED_TASK} {task_numbers[i]}")
    for i in range(num_background_tasks):
        job_description_array.append(f"{BACKGROUND_JOB} {''.join(job_codes[i])}")    
    random.shuffle(job_description_array)
    return job_description_array

def increment_timestamp(timestamp, seconds):
    h, m, s = [int(timestamp_component) for timestamp_component in timestamp.split(':')]
    
    s += seconds
    m += s // 60
    h += m // 60
    
    return f"{h % 24:02}:{m % 60:02}:{s % 60:02}"

def generate_job_start_timestamps(num_jobs, time_frame):
    # We will generate timestamps in an input-given time frame measured in seconds,
    # with a random starting time. 
    starting_hour = random.randint(0, 23)
    starting_minute = random.randint(0, 59)
    starting_second = random.randint(0, 59)
    
    starting_time = f"{starting_hour:02}:{starting_minute:02}:{starting_second:02}"
    # Generate timestamps in the given time frame
    time_offsets = random.sample(range(0, time_frame), num_jobs)
    
    job_start_timestamps = []
    for time_offset in time_offsets:
        job_start_timestamps.append(increment_timestamp(starting_time, time_offset))
    
    return job_start_timestamps

def generate_job_end_timestamps(job_start_timestamps):
    # We have picked a random fraction of jobs to be errors and warnings
    warning_jobs_fraction = round(random.uniform(0.2, 0.3), 2)
    error_jobs_fraction = round(random.uniform(0.2, 0.3), 2)
    
    job_end_timestamps = []
    num_job_errors = 0
    num_job_warnings = 0
    
    for i in range(len(job_start_timestamps)):
        # Generate a random job duration, chosen so we can calculate how many of each type
        # of jobs we want to generate (errors and warnings)
        job_duration = random.randint(1, 300)
        
        # Use the previously defined fractions to distribute job durations based on the 
        # warnings and errors we want to generate
        if i < len(job_start_timestamps) * warning_jobs_fraction:
            job_duration += 300
            num_job_warnings += 1
        elif i < len(job_start_timestamps) * (warning_jobs_fraction + error_jobs_fraction):
            job_duration += 600
            num_job_errors += 1
        
        # This approach will also help us assign matching PIDs to job starts and ends,
        # by maintaining the same order of job start timestamps
        job_end_timestamps.append(increment_timestamp(job_start_timestamps[i], job_duration))
        
    # We have also stored the number of errors and warnings in the log file
    # which will be used for both manual and automatic testing
    return job_end_timestamps, num_job_errors, num_job_warnings

def generate_jobs(num_jobs, time_frame):
    
    job_PIDS = generate_job_PIDS(num_jobs)
    job_descriptions = generate_job_descriptions(num_jobs)
    job_start_timestamps = generate_job_start_timestamps(num_jobs, time_frame)
    job_end_timestamps, num_job_errors, num_job_warnings = generate_job_end_timestamps(job_start_timestamps)
    
    
    logfile_entries = []
    for i in range(num_jobs):
        logfile_entries.append(f"{job_start_timestamps[i]},{job_descriptions[i]},"
                               f"START,{job_PIDS[i]}\n")
        logfile_entries.append(f"{job_end_timestamps[i]},{job_descriptions[i]},"
                               f"END,{job_PIDS[i]}\n")
        
    # Sort the log file entries by timestamp
    logfile_entries.sort(key=lambda x: x.split(',')[0])
    
    return logfile_entries, num_job_errors, num_job_warnings


def main():
    nr_args = len(sys.argv)
    if nr_args != 4:
        print("Usage: python test_generator.py <number_of_jobs> <time_frame> <name_of_logfile>")
        sys.exit(1)
        
    num_jobs = int(sys.argv[1])
    time_frame = int(sys.argv[2])
    path_to_logfile = sys.argv[3]
    
    logfile_entries, num_job_errors, num_job_warnings = generate_jobs(num_jobs, time_frame)
    print(f"Generated {num_jobs} jobs with {num_job_errors} expected errors and {num_job_warnings} expected warnings.")
    
    # Name consistency and directory pre-requisite required for automatic testing
    if not os.path.exists("logstash"):
        os.makedirs("logstash")
    if not path_to_logfile.startswith("logstash/"):
        path_to_logfile = "logstash/" + path_to_logfile
    if not path_to_logfile.endswith(".log"):
        path_to_logfile += ".log"
        
    path_to_expected_report_data_file = path_to_logfile + ".expected_data"
    
    logfile = open(path_to_logfile, "w")
    expected_report_data_file = open(path_to_expected_report_data_file, "w")
    
    logfile.writelines(logfile_entries)
    expected_report_data_file.write(f"{num_job_errors} {num_job_warnings}")
    
    logfile.close()
    expected_report_data_file.close()

if __name__ == "__main__":
    main()

    
    
    