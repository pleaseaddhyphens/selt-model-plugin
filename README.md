This is the guide how to insall that plugin
## Prerequisites

### 1. Install Python
Gaphor requires Python 3.11 or later. You can download the latest version of Python from the official site: [Python Downloads](https://www.python.org/downloads/).

- **Windows**: Download and run the installer, then select the option to add Python to your PATH.
- **macOS/Linux**: Install via package manager (recommended) or download from the site.

### 2. Install pip
Most Python installations come with `pip` (Python's package installer) pre-installed. You can check if pip is installed by running:

```bash
pip --version
```

If it's missing, refer to the [official pip installation guide](https://pip.pypa.io/en/stable/installation/) to install it.

---

## For Windows

1. **Download Gaphor**: Go to the [Gaphor download page](https://gaphor.org/download/) and download the Windows installer.
2. **Install Gaphor**: Run the downloaded installer and follow the on-screen instructions to install Gaphor.

3. **Install SeltModelPlugin**: After installing Gaphor, open a command prompt and run the following command to install the SeltModelPlugin:

   ```bash
   pip install --upgrade --target $env:USERPROFILE\.local\gaphor\plugins-2 git+https://github.com/pleaseaddhyphens/selt-model-plugin.git
   ```

4. **Launch Gaphor**: When you open Gaphor, it should automatically load the SeltModelPlugin if it was installed correctly. You’re ready to go!

---

## For macOS

1. **Download Gaphor**: Visit the [Gaphor download page](https://gaphor.org/download/) and download the macOS version of Gaphor.
2. **Install Gaphor**: Open the downloaded `.dmg` file and drag Gaphor into your Applications folder.

3. **Install SeltModelPlugin**: Open Terminal and run the following command to install the SeltModelPlugin:

   ```bash
   pip install --upgrade --target $HOME/.local/gaphor/plugins-2 git+https://github.com/pleaseaddhyphens/selt-model-plugin.git
   ```
4. **Troubleshooting** if pip don't recognize the pull from git, download zip file and run from the .zip file folder:
   ```bash
   pip install --upgrade --target $HOME/.local/gaphor/plugins-2 selt-model-plugin.zip
   ```

4. **Launch Gaphor**: Open Gaphor from your Applications folder. The SeltModelPlugin should load automatically if installed correctly.

---

## For Linux

1. **Download Gaphor from flatpack**:
	- If you don’t have it setup already, follow the instructions to [install Flatpak](https://flatpak.org/setup).

3. **Install SeltModelPlugin**: Run the following command in Terminal to install the SeltModelPlugin:

   ```bash
   pip install --upgrade --target $HOME/.local/gaphor/plugins-2 git+https://github.com/pleaseaddhyphens/selt-model-plugin.git
   ```
4. **Troubleshooting** if pip don't recognize the pull from git, download zip file and run from the .zip file folder:
   ```bash
   pip install --upgrade --target $HOME/.local/gaphor/plugins-2 selt-model-plugin.zip
   ```

5. **Launch Gaphor**: Start Gaphor from your applications menu or by typing `gaphor` in Terminal. The plugin should load automatically upon startup.

---

### Notes

- **Plugin Installation Directory**: Ensure that the directory specified for the plugin (`$HOME/.local/gaphor/plugin-2` for macOS/Linux or `%USERPROFILE%\.local\gaphor\plugin-2` for Windows) is correct. If the plugin fails to load, verify this directory exists.
---
## Contact Information
If you have any questions or run into issues, please reach out:
1. **Email**: [Valentin.Tikhonenko@skoltech.ru](mailto:Valentin.Tikhonenko@skoltech.ru)


