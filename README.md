# svncl

Generate changelog from svn log.

## Rational

This tool is inspired by [svn2cl][svn2cl] whose output GNU style changelog is huge and easy to lost key informations, so this tool aims to generate a [conventional changelog][conventional-changlog] style changlog file.

[svn2cl]: https://arthurdejong.org/svn2cl/
[conventional-changlog]: https://github.com/conventional-changelog/conventional-changelog

## Requirements

- **your repo should follow the [conventional commit][conventional]**
- python 3.8+

[conventional]: https://www.conventionalcommits.org/en/v1.0.0/

## Installation

```bash
# install dependent package
pip3 install -r requirement.txt
# clone the repo
export $SVNCL /path/to/svncl
git clone https://github.com/qian-gu/svncl $SVNCL
```

## Usage

```bash
python $SVNCL/svncl.py -h
```

```text
usage: svncl.py [-h] [--path PATH] [--xml XML] [--input INPUT] [--output OUTPUT]

Generate changelog from svn log.

optional arguments:
  -h, --help       show this help message and exit
  --path PATH      svn repository directory path
  --xml XML        input xml format logfile
  --input INPUT    input changelog logfile
  --output OUTPUT  output changelog filename
```

## Examples

Generate changelog for repo projectX which is located in `~/svn_repos/projectX`.

```bash
# method 1: under any path, e.g., home, specify via --path option
cd ~
python $SVNCL/svncl.py --path ~/svn_repo/projectX
# method 2: run command under the repo directory, omit --path argument
cd ~/svn/repo/projectX
python $SVNCL/svncl.py
# specify xml logfile
python $SVNCL/svncl.py --xml svnlog.xml
# read input changelogfile
python $SVNCL/svncl.py --input changelog.md
```

example output:

```text
# Changelog

All noteable changes to this project whill be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guideline.

## (2022-09-30)

* feat(foo)!: support feature foo (r8)
* fix: remove error output of world.c (r7)
* fix: remove hello error output (r6)
* feat: add world feature (r5)
* feat: add hello feature (r3)
* fix: add title in readme.md (r2)
* feat: initial (r1)

```

## TODO

* [ ] support reading changlog file