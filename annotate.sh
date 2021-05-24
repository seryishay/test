python3 junit_annotate.py --path "/tmp"
#cat annotate.md
#cat annotate.md | buildkite-agent annotate --context "junit" --style "info"

cat annotate_fail.md | buildkite-agent annotate --style 'error' --context 'ctx-error'
cat annotate_passed.md |buildkite-agent annotate --style 'success' --context 'ctx-success'