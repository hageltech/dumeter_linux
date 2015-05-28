
from distutils.core import setup
import re

VERSIONFILE='src/dumeter/__init__.py'
verstrline = open(VERSIONFILE, 'rt').read()
VSRE = r"^VERSION = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)


setup(name='dumeter-reporter',
    version=verstr,
    description='dumeter.net network bandwidth usage reporter',
    long_description='dumeter.net network bandwidth usage reporter',
    author='Haim Gelfenbeyn',
    author_email='support@hageltech.com',
    url='https://www.dumeter.net/',
    license='MPL-2.0',
    scripts=['src/dumeter-reporter'],
    package_dir={'dumeter': 'src/dumeter'},
    packages=['dumeter'],
    data_files=[
        ('/etc', ['dumeter-reporter.conf']),
        ('/var/lib/dumeter-reporter', [])],
    )

