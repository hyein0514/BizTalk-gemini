import os
import subprocess
import time
import signal
import psutil

def check_flask_servers(script_name="app.py"):
    """Check if any Flask servers are running and return their PIDs."""
    running_servers = []

    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmdline = proc.info["cmdline"]
            if (
                cmdline
                and "python" in proc.info["name"].lower()
                and any(script_name in arg for arg in cmdline if arg)
            ):
                pid = proc.info["pid"]
                running_servers.append(pid)
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            pass

    return running_servers


def kill_flask_servers(script_name="app.py"):
    """
    Kill all Python processes running the specified script (Flask servers)
    Uses psutil to find and kill processes more reliably than just using command line
    """
    killed_pids = []

    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmdline = proc.info["cmdline"]
            if (
                cmdline
                and "python" in proc.info["name"].lower()
                and any(script_name in arg for arg in cmdline if arg)
            ):
                pid = proc.info["pid"]
                print(f"Found Flask server process {pid} running {script_name}, killing...")

                # Windows requires SIGTERM
                os.kill(pid, signal.SIGTERM)
                killed_pids.append(pid)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            pass

    if killed_pids:
        print(
            f"Killed Flask server processes with PIDs: {', '.join(map(str, killed_pids))}"
        )
    else:
        print(f"No Flask server processes running {script_name} found.")

    # Give processes time to die
    time.sleep(1)

    # Verify all are dead
    for pid in killed_pids:
        if psutil.pid_exists(pid):
            print(f"Warning: Process {pid} still exists after kill signal.")
        else:
            print(f"Confirmed process {pid} was terminated.")

    return killed_pids

def start_flask_server_windows(script_name="app.py", port=5000):
    """Start a Flask server using Windows 'start' command which is more reliable for Windows environments."""
    print(
        f"Starting Flask server ({script_name}) on port {port} using Windows 'start' command..."
    )

    # Get the virtual environment Python executable
    venv_path = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_path):
        print(f"Error: Could not find Python executable at {venv_path}")
        return None

    try:
        # Use Windows 'start' command to launch in a new window
        # This is more reliable on Windows for Flask apps
        log_file_path = os.path.join("C:\\Users\\user\\.gemini\\tmp\\5b58604e831195a75dde15e837b0493c7e0ba2d67ade925e6448171984900b16", f"flask_{script_name}.log")
        with open(log_file_path, "w") as log_file:
            process = subprocess.Popen(
                [venv_path, script_name],
                cwd="backend",
                stdout=log_file,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        print(f"Flask server ({script_name}) started in background. Output logged to {log_file_path}")
        return process.pid

    except Exception as e:
        print(f"Error starting Flask server: {str(e)}")
        return None
