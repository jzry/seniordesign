# Configuring Python

Before running the Python code for this project
you must set up a virtual python environment,
install all dependencies, and install the custom
packages in this folder.

It is assumed that you have already installed Python
on your system.

If you already have a virtual environment setup,
you can skip that section.

## Configuring Python Virtual Environment

Open a terminal and navigate to the project's root directory `seniordesign`.

Create a new virtual environment with the command:

`python -m venv python_env`

To start using the virtual environment,
you must first source it in your terminal:

- **Linux and MacOS**
    - `source python_env/bin/activate`
- **Windows**
    - In cmd.exe: `python_env\Scripts\activate.bat`
    - In Powershell: `python_env\Scripts\Activate.ps1`

If you succeed, you will see the text `(python_env)` appear at the beginning
of the prompt line in your terminal.

> [!IMPORTANT]
> You may have to source the virtual environment every time each time you
> start your terminal. Make sure `(python_env)` appears in your terminal
> before running python or pip!

## Installing Packages

Install the main dependencies with the following command in a terminal:

`pip install opencv-python numpy matplotlib`

[Install PyTorch](https://pytorch.org/get-started/locally/) using the
command from their website. From the options on the linked page,
select the following:
- Stable 2.5.x
- (Your operating system)
- Pip
- Python
- CPU

> [!NOTE]
> You can install a [CUDA version](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)
> of PyTorch if you want to use your GPU. For this project,
> the CPU version is fine.

### Install Custom Packages

Navigate in your terminal to the directory `seniordesign/Python`

Run the following command to make an editable install of the `OCR` and `preprocessing`
packages:

`pip install -e OCR_Package -e Preprocessing_Package`

> [!NOTE]
> An editable install will allow you to edit the code in these packages without
> having to reinstall them every time you make a change.

If you need to unistall either of these packages:

`pip uninstall OCR` or

`pip uninstall preprocessing`

