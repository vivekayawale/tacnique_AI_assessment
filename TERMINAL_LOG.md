# Terminal Log

Commands were run from the project root in WSL (Ubuntu, Python 3.14.4). The host Windows
Python launcher was unavailable, so pytest was installed into a temporary directory without
changing the project dependencies.

## Test setup

```text
$ cd /tmp && apt-get download python3-pip-whl
Get:1 http://archive.ubuntu.com/ubuntu resolute/universe amd64 python3-pip-whl all 25.1.1+dfsg-1ubuntu2 [1430 kB]
Fetched 1430 kB in 3s (467 kB/s)

$ dpkg-deb -x /tmp/python3-pip-whl_25.1.1+dfsg-1ubuntu2_all.deb /tmp/haven-pip-bootstrap

$ cd /mnt/c/Users/Vivek/tacnique/haven-infra-assessment
$ PYTHONPATH=/tmp/haven-pip-bootstrap/usr/share/python-wheels/pip-25.1.1-py3-none-any.whl python3 -m pip --version
pip 25.1.1 from /tmp/haven-pip-bootstrap/usr/share/python-wheels/pip-25.1.1-py3-none-any.whl/pip (python 3.14)

$ PYTHONPATH=/tmp/haven-pip-bootstrap/usr/share/python-wheels/pip-25.1.1-py3-none-any.whl python3 -m pip install --target /tmp/haven-infra-assessment-pydeps -r requirements.txt
Collecting pytest>=8.0 (from -r requirements.txt (line 1))
Successfully installed iniconfig-2.3.1 packaging-26.3 pluggy-1.7.0 pygments-2.21.0 pytest-9.2.0
```

## B2 access-control tests

```text
$ PYTHONPATH=/tmp/haven-infra-assessment-pydeps python3 -m pytest -q tests/test_access_control.py
...                                                                      [100%]
3 passed in 0.27s
```

## B2 cost-tag tests

```text
$ PYTHONPATH=/tmp/haven-infra-assessment-pydeps python3 -m pytest -q tests/test_cost_tag_check.py
....                                                                     [100%]
4 passed in 0.26s
```

## Cost-tag check repeated against the unchanged plan

Run 1:

```text
$ PYTHONPATH=/tmp/haven-infra-assessment-pydeps python3 scripts/cost_tag_check.py fixtures/plan.json
Missing landlord_account_id tag: aws_s3_bucket.listing_media
Missing landlord_account_id tag: aws_lambda_function.mls_feed_sync
CHECK_EXIT=1
```

Run 2:

```text
$ PYTHONPATH=/tmp/haven-infra-assessment-pydeps python3 scripts/cost_tag_check.py fixtures/plan.json
Missing landlord_account_id tag: aws_s3_bucket.listing_media
Missing landlord_account_id tag: aws_lambda_function.mls_feed_sync
CHECK_EXIT=1
```

Both runs reported the same resource addresses in the same order and returned the same exit
code. Exit code `1` is expected because the fixture includes resources missing the required
tag.
