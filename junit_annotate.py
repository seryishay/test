import xml.etree.ElementTree as ET
import os
import fnmatch


def parse_junit(path):
    print(f'Parsing Junit XML: {path}')
    report = []

    try:
        tree = ET.parse(path)
        testcases = tree.iter('testcase')

        for testcase in testcases:
            classname = testcase.get('classname')
            name = testcase.get('name')
            time = testcase.get('time')
            file = testcase.get('file')
            line = testcase.get('line')
            error = testcase.find('error')
            failure = testcase.find('failure')
            skipped = testcase.find('skipped')

            if skipped is not None:
                result = 'SKIPPED'
                text = skipped.text
                message = skipped.attrib.get('message')
            elif error is not None:
                result = 'ERRORED'
                text = error.text
                message = error.attrib.get('message')
            elif failure is not None:
                result = 'FAILED'
                text = failure.text
                message = failure.attrib.get('message')
            else:
                result = 'PASSED'
                message = None
                text = None

            report.append({
                'name': name,
                'classname': classname,
                'time': time,
                'file': file,
                'line': line,
                'result': result,
                'message': message,
                'text': text
            })
    except Exception as e:
        print(e)
    return report


def batch_parse_junit(path):
    xml_files = []
    results = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, '*.xml'):
                xml_files.append(os.path.join(root, name))
    for file_path in xml_files:
        results += parse_junit(file_path)
    return results


def generate_html(path, artifact_base_url, failed_filename, passed_filename):
    parsed_xml = batch_parse_junit(path)

    def testcase_to_html(testcase):
        html = f'<details><summary><code>{testcase.get("name")} in {testcase.get("classname")}</code></summary>\n'
        if testcase.get("result") is not None:
            html += f'\t<p>Result: {testcase.get("result")}</p>\n'
        if testcase.get("time") is not None:
            html += f'\t<p>Runtime: {float(testcase.get("time")):0.2f}</p>\n'
        if testcase.get("message") is not None:
            html += f'\t<p>Message: {testcase.get("message")}</p>\n\n'
        if testcase.get("text") is not None:
            html += f'<pre><code>{testcase.get("text")}</code></pre>\n\n'
        html += '</details>\n'
        return html

    failed = [test for test in parsed_xml if test.get('result') != 'PASSED']
    passed = [test for test in parsed_xml if test.get('result') == 'PASSED']
    failed_file = f'{len(failed)}/{len(parsed_xml)} Failed\n\n'
    passed_file = f'{len(passed)}/{len(parsed_xml)} Passed\n\n'

    for testcase in failed:
        failed_file += testcase_to_html(testcase)

    with open(failed_filename, 'w') as f:
        f.write(failed_file)

    for testcase in passed:
        passed_file += testcase_to_html(testcase)

    with open(passed_filename, 'w') as f:
        f.write(passed_file)

    print(failed_file, passed_file)
    return len(failed) == 0


if __name__ == '__main__':

    path = os.environ.get('ARTIFACTS_DIR', './artifacts')
    buildkite_job_id = os.environ.get('BUILDKITE_JOB_ID')
    artifact_base_url = f'https://buildkite-managedartifactsbucket.s3.amazonaws.com/{buildkite_job_id}/artifacts/'
    failed_filename = os.environ.get('ANNOTATE_FAILED_FILENAME', 'annotate_fail.md')
    passed_filename = os.environ.get('ANNOTATE_PASSED_FILENAME', 'annotate_passed.md')
    print(path, artifact_base_url, failed_filename, passed_filename)

    exit_result = generate_html(path, artifact_base_url, failed_filename, passed_filename)
    exit(0 if exit_result else 1)
