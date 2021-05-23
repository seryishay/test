import xml.etree.ElementTree as ET
import os
import fnmatch
import argparse

def parse_junit(path='junit-result.xml'):
    print(f'Parsing Junit XML: {path}')
    report = []

    try:
        tree = ET.parse(path)
        testcases = tree.iterfind('testcase')

        for testcase in testcases:
            classname = testcase.get('classname')
            name = testcase.get('name')
            time = testcase.get('time')
            file = testcase.get('file')
            line = testcase.get('line')
            error_string = testcase.find('error')
            failure_string = testcase.find('failure')
            skipped_string = testcase.find('skipped')

            if skipped_string is not None:
                result = 'SKIPPED'
                message = skipped_string.text
            elif error_string is not None:
                result = 'ERRORED'
                message = error_string.text
            elif failure_string is not None:
                result = 'FAILED'
                message = failure_string.text
            else:
                result = 'PASSED'
                message = None

            report.append({
                'name': name,
                'classname': classname,
                'time': time,
                'file': file,
                'line': line,
                'result': result,
                'message': message
            })
    except Exception as e:
        print(e)
    print(report)
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


def generate_html(path, output='annotate.md'):
    parsed_xml = batch_parse_junit(path)
    html = ''

    def testcase_to_html(testcase):
        html = f'<details><summary><code>{testcase.get("name")} in {testcase.get("classname")} {testcase.get("result")}</code></summary>\n'
        if testcase.get("message") is not None:
            html += f'\t<p>{testcase.get("message")}</p>\n'
        html += '</details>\n'
        return html

    for testcase in parsed_xml:
        html += testcase_to_html(testcase)

    with open(output, 'w') as f:
        f.write(html)

    return html


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='', help='path to artifacts folder')
    args = parser.parse_args()
    if args.path is None:
        raise Exception('path must be supplied')
    print(f'path={args.path}')
    print(generate_html(args.path))
