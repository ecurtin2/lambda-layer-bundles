"""

Given a conda --list file, get the dependencies for one library
containing packages from the conda list. In effect, this is extracting 
the subset of the set of anaconda packages needed to run one of the libraries.

This should allow you to create one 'master' list of libraries, and the layers
can be extracted from it using this function. The libraries should then
all work when combined. 

This file is optional to use - it requires conda.

"""


from contextlib import redirect_stdout
from itertools import dropwhile
import io
import sys

from conda import cli

with open('anaconda_list.txt') as f:
    lines = [line.split() for line in f.readlines()[3:]]

    
class Info:
    def __init__(self, version, build, channel='default'):
        self.version = version
        self.build = build
        self.channel = channel
    def __repr__(self):
        return f'{type(self).__name__}(version={self.version}, build={self.build}, channel={self.channel})'
    
libraries = {package: Info(*rest) for package, *rest in lines}


def conda_run(*args):
    out = io.StringIO()
    with redirect_stdout(out):
        cli.main("", *args)
    return out.getvalue()


def conda_search(library, version, build, channel='default'):
    return conda_run('search', f'{library}={version}={build}', '-c', channel, '--info')


def requirements(library):
    info = libraries[library]
    search = conda_search(library, info.version, info.build, info.channel)
    lines = iter(search.split('\n'))
    for line in lines:
        if 'dependencies' in line:
            break

    LAMBDA_INCLUDED = {'python', 'boto3'}
    
    # Lovely to have but in general these are too large for lambda
    # layers. Perhaps a numpy-MKL layer is worth doing?
    BLACKLIST = {'mkl', 'icc_rt', 'blas', 'vc'}  

    deps = {line.split()[1] for line in lines if line} - LAMBDA_INCLUDED - BLACKLIST

    dependencies = []
    for dependency in sorted(deps):
        info = libraries.get(dependency)
        dependencies.append(f'{dependency}=={info.version}')
        
    lib = [f'{library}=={info.version}']
    return '\n'.join(lib + dependencies)

if __name__ == '__main__':
    try:
        lib = sys.argv[1]
        print(requirements(lib))
    except:
        print('Oh no! This script takes exactly one command line arg. '
        'It must be the name of a package within anaconda_list.txt'
        )

