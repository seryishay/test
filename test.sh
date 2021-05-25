pip3 install pytest
python3 -m pytest --all -v --junitxml="/tmp/junit-result.xml"

export ANNOTATE_FAILED_FILENAME=annotate_fail.md
export ANNOTATE_PASSED_FILENAME=annotate_passed.md
export ARTIFACTS_DIR=.
EXIT_CODE=0
python3 junit_annotate.py || EXIT_CODE="@?"
< $ANNOTATE_FAILED_FILENAME buildkite-agent annotate --style 'error' --context 'ctx-error'
< $ANNOTATE_PASSED_FILENAME buildkite-agent annotate --style 'success' --context 'ctx-success'
exit EXIT_CODE