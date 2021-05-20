import argparse
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pytest-args', nargs='*', help='Extra args to pass to pytest, with a -- prefix.')
    parser.add_argument('--pytest-single-args', nargs='*', help='Extra single args to pass to pytest, with a - prefix.')

    try:
        args = parser.parse_args()
    except AttributeError:
        print(parser.usage())
        sys.exit(1)

    extra_pytest_args = ' '.join([f'--{arg}' for arg in args.pytest_args]) if args.pytest_args else ''
    extra_pytest_single_args = \
        ' '.join([f'-{arg}' for arg in args.pytest_single_args]) \
            if args.pytest_single_args \
            else ''
    all_extra_pytest_args = f'{extra_pytest_args} {extra_pytest_single_args}'

    print(f'Extra pytest arguments: {extra_pytest_args}')
    print(f'Extra pytest single arguments: {extra_pytest_single_args}')