export ANNOTATE_FAILED_FILENAME=annotate_fail.md
export ANNOTATE_PASSED_FILENAME=annotate_passed.md
export ARTIFACTS_DIR=.
EXIT_CODE=0
python3 .buildkite/junit_annotate.py || EXIT_CODE="@?"
< $ANNOTATE_FAILED_FILENAME buildkite-agent annotate --style 'error' --context 'ctx-error'
< $ANNOTATE_PASSED_FILENAME buildkite-agent annotate --style 'success' --context 'ctx-success'
exit EXIT_CODE