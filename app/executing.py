import subprocess

def runcmd(powershell_cmd):
    try:
        result = subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return result.stderr.strip()
    except Exception as e:
        return str(e)

