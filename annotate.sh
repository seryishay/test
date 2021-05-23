python3 junit_annotate.py --path "/tmp"
cat annotate.md
cat annotate.md | buildkite-agent annotate --context "junit" --style "info"