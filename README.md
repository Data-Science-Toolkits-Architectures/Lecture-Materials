# Data Science Toolkits & Architectures: course materials

This repository holds the materials for the Data Science Toolkits & Architectures course at the University of Lucerne. That means the notebook for each lecture and the sample code for the course project.

## Before the first lecture

Work through [SETUP.md](SETUP.md). It tells you what to install and in what order, and it is the only thing you have to do before we start.

It ends with one command, which you run inside this folder.

```bash
uv run doctor.py
```

The command checks your machine and prints a result for every item. You send us the result only if something fails.

## How the materials are released

The material for each lecture lives on its own branch, and a branch appears at the latest before its lecture starts. Pull before every lecture, then switch to the branch for the lecture you are in.

```bash
git fetch
git switch lecture-1
```

## What a lecture branch holds

One folder per lecture under `src`, so `src/lecture_02` for the second lecture. Inside it are the notebook for that lecture, its code examples and its optional exercises. Later branches also carry the data the project trains on.

Nothing here has a space in its name, and folders are lower case with underscores. A space breaks any command that does not quote the path, and it breaks differently on each of the three systems. Use the same convention in your own repository.

## Work in your own repository, not in this one

Clone this repository and pull it before each lecture. Do not do your own work inside it. Copy what you need into your own project repository and work there. This repository moves under you every time we push the next lecture, and anything you leave here will collide with that.
