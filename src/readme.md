## Convert Python Script to Executable
### Requirements
- [PyInstaller](https://www.pyinstaller.org/)

### Usage Instructions

1. **Install PyInstaller**
   If you haven't installed PyInstaller yet, you can do so using pip:
   ```bash
   pip install pyinstaller
   ```

2. **Open Command Prompt**
   Launch the Command Prompt (cmd) on your system.

3. **Navigate to Your Project Directory**
   Change the directory to your project's folder. Replace `your/current/path` with the actual path to your project:
   ```bash
   cd your/current/path
   ```

4. **Generate the Executable**
   Use PyInstaller to create the executable from the provided `.spec` file:
   ```bash
   pyinstaller OpenImagery.spec
   ```

5. **Locate the Executable**
   After the process completes, your executable file will be located in the `dist` folder within your project directory.

6. **Run and Enjoy**
   Navigate to the `dist` folder and run your new executable file to enjoy your standalone application!


With these steps, you can easily convert your Python script into a standalone executable that can be run on any compatible system without needing to install Python or other dependencies.
