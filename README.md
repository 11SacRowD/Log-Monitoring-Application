Log-Monitoring Application

log_processor.py - Script that produces the desired report based on a given logfile
Usage: python3 log_processor.py <path_to_input_log_file> <path_to_output_report_file>

Solution: 

Due to the nature of a log file, we can draw some idea which help us optimize the time and space complexity of our problem:
    - The jobs being logged are most likely processes running on an operating systems (PID used in application description)
    - 2 processes running at the same time can not have the same PID
    - The first occurence of a PID in a log file will signify the start of a job, the second one, the end of a job

Therefore, iterating over every job and using a dictionary with PIDs as keys to track starts and ends of jobs is both time and space efficient.

Testing

test_generator.py - Script that generates a logfile which can be processed with the log processor script. Logfile will be automatically created inside ./logstash/<name_of_log> in scope of running automated tests.

Also generates file containing number of expected Errors and Warnings in scope of automated testing and validation of log processor script.

Usage: python3 test_generator.py <num_of_jobs> <timeframe_for_job_starts_in_seconds> <name_of_logfile>

run_tests.py - Uses both log_processor and the tests generated with test_generator in order to validate correct processing of all logs generated inside logstash

5 tests have already been provided, generated with test_generator

Usage: python3 run_tests.py


Notes:
    - The solution was written unde the assumption that the logging did not miss any starts and ends of a job
    - The solution was written with as many edge cases / possible unprovided information in mind, without overcomplicating the task
    - Test generation tried to emulate the log given as an example to the best of my abilities,
    without going into extensive detail (May suffer from jobs generated with the same START timestamp / END timestamp)