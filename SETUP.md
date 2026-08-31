# Setting up your machine

The system you build in this course runs on your own laptop. That is why the laptop has to be ready before we start, and this document gets it there.

Work through it before **Thursday 10 September**. At the end you run one command and send us what it prints. We use that to find broken machines while there is still time to fix them. A machine that is not ready on 17 September costs you the first session.

Set aside about an hour. Most of that is waiting for downloads, so start it somewhere with a good connection.

## What your machine needs

- Windows 11 or macOS. Both are supported and the instructions differ only where they must.
- 8 GB of memory. The course is designed to fit in that.
- 15 GB of free disk space. You need about 10 GB by the end of October. The rest is margin.
- The right to install software. If your laptop is managed by an employer, check this before you start.

Tell us now if any of those is a problem. There is a way round each of them, and all of them are easier to arrange in August than in October.

## What you install

Six things, and then nothing else for the rest of the semester.

1. **A GitHub account.** Where your team's code lives.
2. **Git.** The tool that tracks every change to that code.
3. **uv.** It fetches Python and every package the project needs. You do not install Python yourself.
4. **Docker Desktop.** It runs the parts of the system that are not Python. You do not use it until the second session, but we check it now so that a problem surfaces early.
5. **PyCharm.** The editor we teach in. If you already work in Visual Studio Code you may keep it, but our screenshots and our help will be PyCharm.
6. **Warp.** The terminal we all use. A problem you show us then looks like something we know. You can also send us a whole command and its answer in one piece.

That list is the whole set. Everything else the project uses is described in files inside the project itself, and uv and Docker fetch it when you need it. This is deliberate. It means your laptop cannot drift out of step with everyone else's.

## GitHub, first, because it takes time to approve

1. Create an account at [github.com](https://github.com). Use your university address. It makes the next step faster.
2. Apply for the [GitHub Student Developer Pack](https://education.github.com/pack). Approval can take several days, so do this first. The pack gives you the full edition of PyCharm at no cost, along with other tools we use later.
3. Turn on GitHub Copilot Free in your account settings. Every account has it.

The pack carries two things we use. GitHub Copilot, and the full edition of PyCharm. They are separate benefits, so a problem with one does not affect the other.

GitHub suspended new sign-ups for the paid Copilot plan in April 2026. We expect it to reopen. If it has not by the time you apply, turn on Copilot Free instead. Every account carries it and it is enough for this course.

## macOS

Find out which chip your Mac has first. Open the Apple menu, then About This Mac. It says either Apple silicon or Intel. You need this for step three.

**1. Command line tools.** Open Terminal, from Applications and then Utilities. Type this and press return.

```
xcode-select --install
```

A window appears. Accept it and wait. This installs Git along with other things macOS needs. It is a large download. If it tells you the tools are already installed, that is fine, carry on.

**2. uv.** In the same Terminal window.

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close Terminal and open it again when this finishes. That is how the new command becomes available.

**3. Docker Desktop.** Download it from [docker.com](https://www.docker.com/products/docker-desktop/), choosing the version for your chip. Open the file and drag Docker to Applications. Start it, accept the terms, and wait until it reports that it is running. Leave it running.

**4. PyCharm.** Download it from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/download/). Install it and start it once. If your Student Pack has been approved, sign in with your GitHub account to unlock the full edition. If it has not been approved yet, the free edition is enough for now and you can sign in later.

**5. Warp.** Download it from [warp.dev](https://www.warp.dev/download). Open the file and drag Warp to Applications. Start it. You do not need an account. From here on, when these instructions say to open a terminal, open Warp.

## Windows

**1. Check that your processor can run containers.** Do this before you download anything, because it is the one thing you cannot fix by installing software.

Open Task Manager by pressing Ctrl, Shift and Escape together. Choose Performance, then CPU. Look for **Virtualisation** on the right. It must say **Enabled**.

If it says Disabled, you can usually turn it on in your laptop's firmware settings. You reach those by pressing a key such as F2 or Del while the machine starts. If it is missing entirely, or your laptop is managed and will not let you change it, stop here and tell us. Do not spend an evening on it.

**2. PowerShell 7.** Windows comes with an older version that behaves differently. Open the Start menu, type `terminal`, and open Windows Terminal. Then run this.

```
winget install --id Microsoft.PowerShell -e
```

Close the window. From now on, whenever these instructions say to open a terminal, open **PowerShell 7** and not Windows PowerShell. They have similar names and they are not the same thing.

**3. Git and uv.** In a PowerShell 7 window.

```
winget install --id Git.Git -e
winget install --id astral-sh.uv -e
```

Close the window and open a new one when this finishes.

**4. Docker Desktop.** Download it from [docker.com](https://www.docker.com/products/docker-desktop/) and run the installer. It asks to install a component called WSL2. Accept it. Restart your laptop when it asks. Then start Docker Desktop and wait until it reports that it is running. Leave it running.

**5. Give WSL2 a fixed size.** Docker runs inside a small Linux machine, and left alone it takes as much memory as it likes. We set it once, so that every machine in the course behaves the same way and Windows keeps enough for itself.

Create a file called `.wslconfig` in your user folder, which is the one named after you inside `C:\Users`. Put exactly this in it.

```
[wsl2]
memory=4GB
processors=2
swap=2GB
```

If your laptop has 16 GB of memory or more, write `memory=8GB` instead.

The file must be named `.wslconfig` with the dot and with no `.txt` on the end. Notepad adds `.txt` unless you choose All Files in the save dialogue. After saving it, quit Docker Desktop and start it again.

**6. PyCharm.** Download it from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/download/). Install it and start it once. If your Student Pack has been approved, sign in with your GitHub account to unlock the full edition. If it has not been approved yet, the free edition is enough for now.

**7. Warp.** Download it from [warp.dev](https://www.warp.dev/download) and run the installer. Start it and choose PowerShell 7 as its shell when it asks. You do not need an account. From here on, when these instructions say to open a terminal, open Warp.

## Where your work lives

This matters more than it looks, and it is the most common cause of problems we cannot diagnose from a distance.

Keep everything for this course in a folder called `dev`, directly inside your user folder. Not in Documents. Not in Desktop. **Not anywhere inside OneDrive or iCloud Drive.**

Those services copy files to the cloud while they are being written. Python environments and containers write thousands of small files, and the two fight each other in ways that produce error messages nobody can read. Windows often puts Documents inside OneDrive without telling you, and macOS does the same with Desktop and Documents.

The path must also have no spaces in it and no accented characters. Windows names your user folder after you, so if your own name contains a space or an accent, that folder cannot be fixed by moving anything. Tell us instead. Windows names your user folder after you. If yours contains an umlaut, tell us. Some tools handle that badly and we would rather know now.

Open a terminal and run these two commands. They are the same on both systems.

```
mkdir ~/dev
cd ~/dev
```

## Check your machine

Still in that folder, run these three commands in turn.

```
git clone https://github.com/Data-Science-Toolkits-Architectures/Lecture-Materials.git
cd Lecture-Materials
uv run doctor.py
```

The first fetches the course repository. The second moves into it. The third checks your machine and prints a result for every item.

You will run `uv run doctor.py` again at every stage of the course. It is the same command each time and it checks more as the project grows.

If Git asks who you are, run these two commands with your own details and then run the check again.

```
git config --global user.name "Your Name"
git config --global user.email "you@stud.unilu.ch"
```

## If everything passed

You are done. Send us nothing. Your machine is ready and there is nothing else to do before 17 September.

## If something failed

Every failure prints what is missing and the command that fixes it. Read that line first. Most failures are a terminal that was open before something was installed. Closing it and opening a new one is the whole fix.

If the failure repeats, the check ends with a block of text between two lines of dashes. Copy all of it. Send it by email to both of us, with the subject line **DSTA setup** and your full name in the message. The addresses are in the syllabus.

Send the whole block and not a screenshot of part of it. The block holds the details we need. Say what you already tried.

Two failures are worth knowing about in advance.

**Docker will not start on Windows.** Almost always this is the virtualisation setting from step one. Check it again.

**Docker will not start at all, on either system.** Tell us. GitHub Codespaces gives you the whole environment in a browser and your Student Pack covers it. We would rather set that up in September than discover the need for it in October.
