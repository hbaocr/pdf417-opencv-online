
import glob
import os
import subprocess
from joblib import Parallel, delayed

import os
import sys
file_dir1 = os.path.dirname(__file__)
sys.path.append(file_dir1)

jar_filename = "javase-3.4.2-SNAPSHOT-jar-with-dependencies.jar"
jar_path = ""


class BarCodeReader():
    command = "java -jar"
    lib_path = ""

    def __init__(self):
        self.lib_path = jar_filename

    def decode(self, filename_pattern):
        filenames = glob.glob(os.path.abspath(filename_pattern))
        if len(filenames) == 0:
            print("File not found!")
            results = None

        elif len(filenames) == 1:
            results = self._decode(filenames[0].replace('\\', '/'))

        else:
            results = Parallel(n_jobs=-1)(
                delayed(self._decode)(filename.replace('\\', '/'))
                for filename in filenames)

        return results

    def _decode(self, filename):
        cmd = ' '.join([self.command, self.lib_path,
                        'file:///' + filename, '--multi','--possible_formats PDF_417','--try_harder'])
        (stdout, _) = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE,
                                       universal_newlines=True,
                                       shell=True).communicate()
        lines = stdout.splitlines()
        separator_idx = [
            i for i in range(len(lines)) if lines[i][:4] == 'file'
        ] + [len(lines)]

        result = [
            self._parse_single(lines[separator_idx[i]:separator_idx[i + 1]])
            for i in range(len(separator_idx) - 1)
        ]
        return result

    @staticmethod
    def _parse_single(lines):
        """parse stdout and return structured result

            raw stdout looks like this:
            file://02.png (format: CODABAR, type: TEXT):
            Raw result:
            0000
            Parsed result:
            0000
            Found 2 result points.
            Point 0: (50.0,202.0)
            Point 1: (655.0,202.0)
        """
        result = {}
        result['filename'] = lines[0].split(' ', 1)[0]

        if len(lines) > 1:
            lines[0] = lines[0].split(' ', 1)[1]
            for ch in '():,':
                lines[0] = lines[0].replace(ch, '')
            _, result['format'], _, result['type'] = lines[0].split(' ')

            raw_index = find_line_index(lines, "Raw result:")
            parsed_index = find_line_index(lines, "Parsed result:")
            points_index = find_line_index(lines, "Found")

            if not raw_index or not parsed_index or not points_index:
                print("Parse Error!")
                return lines
            result['raw'] = lines[raw_index + 1:parsed_index]
            result['raw'] = '\n'.join(result['raw'])
            result['parsed'] = lines[parsed_index + 1:points_index]
            result['parsed'] = '\n'.join(result['parsed'])
            # result['points'] = [ast.literal_eval(line[12:]) for line in lines[points_index+1:-1]]
        return result


def find_line_index(lines, content):
    for i, line in enumerate(lines):
        if line[:len(content)] == content:
            return i

    return None
