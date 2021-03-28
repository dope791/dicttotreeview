pytest test_dtv.py --junitxml=results.xml -o junit_suite_name="general tests"
pytest test_time.py --junitxml=time_results.xml -o junit_suite_name="runtime test"
