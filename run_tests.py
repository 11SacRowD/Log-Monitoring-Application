import os
import sys

def run_test(path_to_logfile):
    

    if not os.path.exists("reports"):
        os.makedirs("reports")

    report_file = os.path.join("reports", os.path.basename(path_to_logfile) + ".report")
    os.system(f"python3 log_processor.py {path_to_logfile} {report_file}")    
    
    with open(report_file, 'r') as report:
        report_content = report.read()
        
    num_errors = report_content.count("ERROR")
    num_warnings = report_content.count("WARNING")
    
    # We have built our *.expected_data file to contain the number of errors and warnings
    expected_output_file = path_to_logfile + ".expected_data"
    with open(expected_output_file, 'r') as expected_output:
        expected_values = expected_output.read().split()
        expected_num_errors = int(expected_values[0])
        expected_num_warnings = int(expected_values[1])
        
    if num_errors == expected_num_errors and num_warnings == expected_num_warnings:
        print(f"Test {path_to_logfile} passed \u2714!")
    else:
        print(f"Test {path_to_logfile} failed \u2717! expected {expected_num_errors} errors and "
              f"{expected_num_warnings} warnings, but got {num_errors} errors and {num_warnings} warnings.")


def run_all_tests():

    if not os.path.exists("logstash"):
        print("Logstash directory does not exist. Please generate some test log files.")
        return
    
    log_files = [os.path.join("logstash", f) for f in os.listdir("logstash") if f.endswith(".log")]
    
    if not log_files:
        print("No log files found in the current directory. Please generate some test log files.")
        return
    
    for log_file in log_files:
        run_test(log_file)
    
    # Line can be uncommented to remove reports after automated testing   
    # os.system("rm -rf reports")        
        
def main():
    run_all_tests()
    
if __name__ == "__main__":
    main()
    
    
    # Run the log processor script, compare the output with the expected output
    # and print the result
    
    