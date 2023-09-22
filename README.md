## Prerequisites

- Python 3.8 or later
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

- python 3.6 or higher
- poetry 1.4.0 or higher
- black 23.1.0 or higher
- isort 5.12.0 or higher
- pytest 7.2.2 or higher

They will be installed in a virtual environment with `make install`

The following dependencies are required to use this service:

- fastapi = 0.95.0 or higher
- uvicorn = 0.21.1 or higher

## Contributing
1. Create a new branch for your feature or bugfix.
2. Write your code and tests.
3. Commit your changes and push them to your branch.
4. Submit a pull request.