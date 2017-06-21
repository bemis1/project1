"""
    Takes CSV file as input. Assume line ',' sep:
    uuid,name,email,address,city,state,zip

    Data processed will contain Adds/Updates/Removals.

    Consider edge cases:
    1. Duplicate uuid
    2. Duplicate email

    Assume uuid is a 36 max len string containing hex/dashes.

    TODO: string length validation, email validation, address validation

"""
from optparse import OptionParser
import logic.accounts


COLUMNS = ['uuid', 'name', 'email', 'address', 'city', 'state', 'zip']


def strip(string):
    return string.strip()


def parse_line(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield dict(zip(COLUMNS, map(strip, line.split(','))))


def process_data(filename):
    errors = []
    for row in parse_line(filename):
        try:
            logic.accounts.upsert_account(row, filename)
        except:
            import traceback
            print (traceback.print_exc())
            errors.append(row)
    return errors


def main(filein, fileout):
    errors = process_data(filein)
    if errors:
        with open(fileout, 'w') as f:
            for e in errors:
                f.write(','.join(e[k] for k in COLUMNS) + '\n')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file",
                      help="Full file path of csv", metavar="FILE")
    parser.add_option("-e", "--error_file",
                      help="Full file path of errors", metavar="FILE",
                      default="")
    (options, args) = parser.parse_args()
    error_file = options.error_file or ("{}_error.out".format(options.file))
    main(options.file, error_file)
