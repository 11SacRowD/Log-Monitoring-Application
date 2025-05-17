import sys

# Job duration thresholds in seconds
WARNING_THRESHOLD_S = 300
ERROR_THRESHOLD_S = 600

# Due to the log file format, we'll assume we're working with timestamps using the 24 hour time format
# We will also assume that the logging period for generating one singular log file is less than 24 hours, as log entries lack a date field
def get_job_duration(start_timestamp, end_timestamp):
    start_h, start_m, start_s = [int(timestamp_component) for timestamp_component in start_timestamp.split(':')]
    end_h, end_m, end_s = [int(timestamp_component) for timestamp_component in end_timestamp.split(':')]
    
    # Simple logic for calculating the duration of a job in seconds
    m_carrier = 0
    h_carrier = 0
    
    if end_s < start_s:
        s_duration = 60 - start_s + end_s
        m_carrier = 1
    else:
        s_duration = end_s - start_s
            
    end_m = end_m - m_carrier
    if end_m < start_m:
        m_duration = 60 - start_m + end_m
        h_carrier = 1
    else:
        m_duration = end_m - start_m
        
    end_h = end_h - h_carrier
    if end_h < start_h:
        h_duration = 24 - start_h + end_h
    else:
        h_duration = end_h - start_h
    
    return s_duration + m_duration * 60 + h_duration * 3600
    
    
    
def generate_raport(logfile):
    job_dict = {}
    report_array = []
    
    last_job_timestamp = None
    
    for log_entry in logfile.readlines():
        job_params = log_entry.split(',')
        job_timestamp, job_description, job_status, job_PID = job_params
        
        # Allows us to know the last timestamp in the log file
        last_job_timestamp = job_timestamp
        job_PID = int(job_PID[:-1])

        # A job PID's first appearance in the log file signifies the start of a job
        if job_PID not in job_dict:
            # Treat the case where a job's first related log entry reports an END status
            if job_status == 'END':
                report_array.append(f"{job_description} with ID {job_PID} did not start during logging period.")
                continue
            
            # Store values in job dictionary as a separate dictionary contiaining relevant log entry information
            # Job status is not relevant (except previous edge case) due to the nature of the log files (see README)
            job_dict[job_PID] = {
                'job_description': job_description,
                'job_timestamp': job_timestamp,
            }    
        else:
            # If the job is already in the dictionary, it means it has already started
            job_duration = get_job_duration(job_dict[job_PID]['job_timestamp'], job_timestamp)
            # We will report only one type of error per job (ERROR implies WARNING)
            if job_duration >= ERROR_THRESHOLD_S:
                report_array.append(f"ERROR: {job_dict[job_PID]['job_description']} with ID {job_PID} "
                                    f"took longer than {ERROR_THRESHOLD_S // 60} minutes.")
            elif job_duration >= WARNING_THRESHOLD_S:
                report_array.append(f"WARNING: {job_dict[job_PID]['job_description']} with ID {job_PID} "
                                    f"took longer than {WARNING_THRESHOLD_S // 60} minutes.")
            
            # The second occurance of an existing PID in the dictionary means the job with that PID has ended
            # We remove the job from the dictionary in case a new job might start with the same PID
            del job_dict[job_PID]
                
    # Treat the case where jobs have started inside the logfile but did not end
    # Based on the last timestamp in the log file, we can determine if a started job will give an ERROR
    #
    # We will report a custom WARNING in the other case, as the difference between the last recorded timestamp and the job's start timestamp
    # might be longer than 10 minutes, not just 5. 
    #
    # We will print a custom message for jobs started less than 5 minutes before the last timestamp
    for job_PID, job_info in job_dict.items():
        job_duration = get_job_duration(job_info['job_timestamp'], last_job_timestamp)
        if job_duration >= ERROR_THRESHOLD_S:
            report_array.append(f"ERROR: {job_dict[job_PID]['job_description']} with ID {job_PID} "
                                f"took longer than {ERROR_THRESHOLD_S // 60} minutes.")
        elif job_duration >= WARNING_THRESHOLD_S:
            report_array.append(f"WARNING: {job_dict[job_PID]['job_description']} with ID {job_PID} "
                                f"took longer than {WARNING_THRESHOLD_S // 60} minutes. Cannot determine if job took longer than 10 minutes, job END not in log!")
        else:
            report_array.append(f"{job_info['job_description']} with ID {job_PID} never ended during logging period.")
        
    return report_array


def main():
    nr_args = len(sys.argv)
    if nr_args != 3:
        print("Usage: python3 log_processor.py <path_to_log_file> <path_to_report_file>") 
        sys.exit(1)
    
    log_file = open(sys.argv[1], 'r')
    report_file = open(sys.argv[2], 'w')
    
    report_array = generate_raport(log_file)
    report_file.write('\n'.join(report_array))
    
    report_file.close()
    log_file.close()
        
        
if __name__=="__main__":
    main()