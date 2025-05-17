Log-Monitoring Application

Usage: Usage: python3 log_processor.py <path_to_log_file> <path_to_report_file>

Solution: 

Due to the nature of a log file, we can draw some idea which help us optimize the time and space complexity of our problem:
    - The jobs being logged are most likely processes running on an operating systems (PID used in application description)
    - 2 processes running at the same time can not have the same PID
    - The first occurence of a PID in a log file will signify the start of a job, the second one, the end of a job

Therefore, iterating over every job and using a dictionary with PIDs as keys to track starts and ends of jobs is both time and space efficient.




Notes:
    - The solution was written unde the assumption that the logging did not miss any starts and ends of a job
    - The solution was written with as many edge cases / possible unprovided information in mind, without overcomplicating the task