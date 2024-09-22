import subprocess

# Current packages in requirements.txt
current_packages = {
    "backgroundremover": "0.2.8",
    "blinker": "1.8.2",
    "certifi": "2024.8.30",
    "charset-normalizer": "3.3.2",
    "click": "8.1.7",
    "commandlines": "0.4.1",
    "decorator": "4.4.2",
    "ffmpeg-python": "0.2.0",
    "filelock": "3.16.1",
    "filetype": "1.2.0",
    "Flask": "3.0.3",
    "fsspec": "2024.9.0",
    "future": "1.0.0",
    "hsh": "1.1.0",
    "idna": "3.10",
    "imageio": "2.35.1",
    "imageio-ffmpeg": "0.5.1",
    "itsdangerous": "2.2.0",
    "Jinja2": "3.1.4",
    "lazy_loader": "0.4",
    "llvmlite": "0.43.0",
    "MarkupSafe": "2.1.5",
    "more-itertools": "10.5.0",
    "moviepy": "1.0.3",
    "mpmath": "1.3.0",
    "networkx": "3.3",
    "numba": "0.60.0",
    "numpy": "2.0.2",
    "packaging": "24.1",
    "Pillow": "9.5.0",
    "proglog": "0.1.10",
    "PyMatting": "1.1.12",
    "PySocks": "1.7.1",
    "requests": "2.32.3",
    "scikit-image": "0.24.0",
    "scipy": "1.14.1",
    "setuptools": "75.1.0",
    "six": "1.16.0",
    "sympy": "1.13.3",
    "tifffile": "2024.9.20",
    "torch": "2.2.2",
    "torchvision": "0.17.2",
    "tqdm": "4.66.5",
    "typing_extensions": "4.12.2",
    "urllib3": "2.2.3",
    "waitress": "3.0.0",
    "Werkzeug": "3.0.4"
}

# Packages to keep
keep_packages = {
    "Flask": "3.0.3",
    "Werkzeug": "3.0.4",
    "backgroundremover": "0.2.8",
    "numpy": "1.24.3",  # Add numpy here
    "torch": "2.2.2",
    "torchvision": "0.17.2",
    "Pillow": "9.5.0",
    "requests": "2.32.3",
    "tqdm": "4.66.5"
}

# Packages to uninstall
to_uninstall = set(current_packages.keys()) - set(keep_packages.keys())

# Uninstall packages
for package in to_uninstall:
    try:
        subprocess.check_call(["pip", "uninstall", "-y", package])
        print(f"Uninstalled {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to uninstall {package}")

# Before installing numpy, install setuptools
try:
    subprocess.check_call(["pip", "install", "--upgrade", "setuptools"])
    print("Installed setuptools")
except subprocess.CalledProcessError:
    print("Failed to install setuptools")

print("Uninstallation process completed.")
