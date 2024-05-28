import subprocess


def test_site_up():
    assert "Failed" not in str(subprocess.check_output("curl http://127.0.0.1:5000 --max-time 3", shell=True))


def test_connection():
    assert (int(str(subprocess.check_output("curl --include http://127.0.0.1:5000", shell=True)).split(" ")[1]) in
            range(200, 400))
