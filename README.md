## Prerequisites

- Python 3.10 or later
- `make`

## Getting Started

1. Clone the repository:

   ```sh
   git clone https://github.com/mazedm80/py-htmx.git
   cd project
   ```

2. Create a virtual environment and install the required tools:

    ```sh
    make install
    ```

3. Run the service locally

    ```sh
    make run
    ```

## Available Targets

- `checkstyle`: Checks the code style of the project using black and isort. The target fails if the code style is not compliant.
- `clear`: Removes all build files and folders.
- `codestyle`: Applies the code style to the project using black and isort.
- `help`: Displays the help message for the Makefile.
- `install`: Creates a virtual environment and installs the package with all dependencies using Poetry.
- `run`: Executes the service locally.
- `test`: Runs pytest against the package.

There are also some aliases defined, such as `i` for `install`, `r` for `run`, `t` for `test`, `cl` for `clear`, and `cs` for `codestyle`.

## Dependencies

The following dependencies are required to use this Makefile:

- python 3.10 or higher
- poetry 1.6.0 or higher
- black 23.9.0 or higher
- isort 5.12.0 or higher

They will be installed in a virtual environment with `make install`

The following dependencies are required to use this service:

- fastapi = 0.103.1 or higher
- uvicorn = 0.23.2 or higher
