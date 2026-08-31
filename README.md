# Data Science Toolkits & Architectures Course - Materials
This repository contains the materials (Jupyter Notebooks and sample project code) for the Data Science Toolkits & Architectures course at the University of Lucerne.

### Before the first lecture
`SETUP.md` in this repository tells you what to install and in what order. Work through it before the first lecture.

It ends with one command, which you run here:

```bash
uv run doctor.py
```

The command checks your machine and prints a result for every item. You send us the result only if something fails. You run the same command at every stage of the course, and it checks more as the project grows.

### Repository Structure
The repository is organized as follows:
- `notebooks`: Jupyter notebooks for each lecture, with code examples and optional exercises.
- `src`: sample code for the course project. More parts arrive through the semester.
- `data`: the dataset the project trains on.

Folder and file names carry no spaces and no capital letters. A space in a path breaks commands that are not carefully quoted, and it breaks them differently on Windows and on macOS. Keep to the same convention in your own repository.

### Accessing the Materials
The materials for each lecture will be made available at __the latest before the lecture starts__. Please make sure to pull the latest changes from the repository before each lecture or check the repository for updates.

To release the materials progressively throughout the course, the materials for each lecture are provided in a __separate branch__. You can switch to the branch corresponding to the current lecture to access its materials.

For example, to access the materials for the first lecture, switch to the `lecture-1` branch:

```bash
git switch lecture-1
```

### Working with the Repository
We recommend cloning the repository to your local machine and working with the materials there. You can use Git to pull the latest changes before each lecture and easily switch between branches.

However, we recommend that you `do not work directly in this course repository`. Instead, copy the materials you need into your own project repository and do your work there.

__Alternatively__, you can work directly with the materials on GitHub by copying or downloading the files for each lecture.