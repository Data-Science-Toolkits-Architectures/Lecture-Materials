# Setting up your machine

Everything you build in this course runs on your own laptop. So the laptop has to work before we start.

Work through this before **Thursday 10 September**. It ends with one command that checks the machine. If something fails, you send us what it prints, and we have a week to sort it out. If your machine is not ready on 17 September, you lose that session.

Set aside about an hour. Most of it is waiting for downloads, so start somewhere with a decent connection.

## What your machine needs

- Windows 11, macOS, or Linux.
- 8 GB of memory.
- 15 GB of free disk space. You will need about 10 GB of it by the end of October.
- The right to install software. Check this first if your laptop belongs to an employer.

Tell us now if any of those is a problem. Each one has a way round it, and all of them are easier to arrange in September than in October.

## What you install

Six things, and nothing else for the rest of the semester.

1. A **[GitHub](https://github.com)** account, where your team's code lives.
2. **[Git](https://git-scm.com)**, which tracks every change to that code.
3. **[uv](https://docs.astral.sh/uv/)**, which fetches Python and every package the project needs. You never install Python yourself.
4. **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**, which runs the parts of the system that are not Python. You do not use it until the second session. We check it now because it is the one that goes wrong.
5. **[PyCharm](https://www.jetbrains.com/pycharm/)**, the editor we teach in. Keep [Visual Studio Code](https://code.visualstudio.com) if you already use it, but our screenshots and our help will be PyCharm.
6. **[Warp](https://www.warp.dev)**, the terminal we all use. When you show us a problem it will look like something we recognise. You can also send us a command and its answer in one piece.

Everything else the project needs is written down inside the project, and uv and Docker fetch it when the time comes. That is deliberate. It is what stops your laptop drifting out of step with everyone else's.

## Start with GitHub

Approval takes days, so do this before anything else.

1. Create an account at [github.com](https://github.com/signup). Use your university address, which makes the next step faster.
2. Apply for the [GitHub Student Developer Pack](https://education.github.com/pack).
3. Turn on [GitHub Copilot Free](https://github.com/settings/copilot) in your account settings.

The pack carries two things we use, [Copilot](https://github.com/features/copilot) and the full edition of PyCharm. They are separate benefits, so a problem with one does not touch the other.

GitHub suspended new sign-ups for the paid Copilot plan in April 2026 and we expect it to reopen. If it has not by the time you apply, use Copilot Free. Every account has it and it is enough for this course.

Now do the section for your own system, then carry on from [PyCharm and Warp](#pycharm-and-warp).

## macOS

Check which chip your Mac has before you start. Apple menu, then About This Mac. It says Apple silicon or Intel, and you need that for Docker.

**Command line tools.** Open Terminal, in Applications and then Utilities, and run this.

```
xcode-select --install
```

Accept the window that appears and wait. This is how Git gets onto a Mac. The `git` command already exists, but nothing sits behind it until these tools are installed. It is a large download, though far smaller than the whole of [Xcode](https://developer.apple.com/xcode/). If it says the tools are already there, carry on.

**uv.** Same window.

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close Terminal and open it again. That is how the new command becomes available.

**Docker Desktop.** Download it from [docker.com](https://www.docker.com/products/docker-desktop/), picking the build for your chip. Drag Docker to Applications, start it, accept the terms, and wait until it says it is running. Leave it running.

## Windows

**Check that your processor can run containers.** Do this before you download anything. It is the one thing you cannot fix by installing software.

Press Ctrl, Shift and Escape together to open Task Manager. Choose Performance, then CPU. On the right, **Virtualisation** must say **Enabled**.

If it says Disabled, you can usually switch it on in your laptop's firmware settings. You reach those by pressing a key such as F2 or Del while the machine starts. If the line is missing, or the laptop is managed and will not let you change it, stop and tell us. Do not spend an evening on it.

**Git and uv.** Open the Start menu, type `terminal`, and open Windows Terminal. These use [winget](https://learn.microsoft.com/windows/package-manager/winget/), which Windows 11 already has.

```
winget install --id Git.Git -e
winget install --id astral-sh.uv -e
```

Close the window and open a new one.

**Docker Desktop.** Download it from [docker.com](https://www.docker.com/products/docker-desktop/) and run the installer. It asks to add [WSL2](https://learn.microsoft.com/windows/wsl/). Accept, and restart when it asks. Then start Docker Desktop and wait until it says it is running. Leave it running.

## Linux

These steps assume Ubuntu 22.04 or later, or Debian. Other distributions work and every page linked here covers them, but those two are the ones we can help with quickly.

**Check that your processor can run containers.** [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/) runs containers inside a virtual machine, so it needs KVM.

```
ls -l /dev/kvm
```

A line of output means you are fine. If the file does not exist, switch on virtualisation in your laptop's firmware settings and check again. You reach those by pressing a key such as F2 or Del while the machine starts.

**Git and uv.**

```
sudo apt update
sudo apt install -y git curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close the terminal and open a new one.

**Docker Desktop.** Follow [Docker's instructions for your distribution](https://docs.docker.com/desktop/setup/install/linux/), in the order they give them. They have you add Docker's package repository before installing the downloaded package, and the install fails if you skip it. Start Docker Desktop from your applications menu and leave it running.

## PyCharm and Warp

The same on all three systems.

Download **PyCharm** from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/download/), or use the [Toolbox App](https://www.jetbrains.com/toolbox-app/) and let it manage the install. Start it once. If your Student Pack has come through, sign in with GitHub to unlock the full edition. If it has not, the free edition is enough and you can sign in later.

Download **Warp** from [warp.dev](https://www.warp.dev/download) and install it. You do not need an account. From here on, wherever these instructions say to open a terminal, open Warp.

## Where your work lives

This is the most common cause of problems we cannot diagnose from a distance, and it looks like nothing.

Keep everything for this course in a folder called `dev`, directly inside your user folder. Not Documents. Not Desktop. **Not inside OneDrive, iCloud Drive, Dropbox or anything else that syncs to the cloud.**

Those services copy files while they are still being written. Python environments and containers write thousands of small files, and the two fight each other in ways that produce errors nobody can read. Windows quietly puts Documents inside OneDrive. macOS does the same with Desktop and Documents.

The path must have no spaces and no accented characters either. Windows names your user folder after you. If your name carries a space or an accent, moving folders will not fix it. Tell us instead.

```
mkdir ~/dev
cd ~/dev
```

Those two commands are the same on all three systems.

## Check your machine

Still in that folder, run these in turn.

```
git clone https://github.com/Data-Science-Toolkits-Architectures/Lecture-Materials.git
cd Lecture-Materials
uv run doctor.py
```

The first fetches the course repository, the second moves into it, and the third checks your machine and prints a result for every item.

It checks the machine, not your project. Once it passes you are set up for the whole course and you never run it again.

If Git asks who you are, set that and run the check again.

```
git config --global user.name "Your Name"
git config --global user.email "you@stud.unilu.ch"
```

## When it passes

Send us nothing. You are done until 17 September.

One line may come back marked WARN rather than PASS. That is not a failure and it does not stop you starting. It means your machine is tighter than the course assumes, usually on memory. We would still like to know, so send us that one line.

## When something fails

Every failure prints what is missing and the command that fixes it. Read that line first. Most failures are a terminal that was already open before you installed something, and opening a fresh one is the whole fix.

If it fails again, copy the block of text between the two lines of dashes. All of it, not a screenshot of part of it. Email it to both of us with the subject **DSTA setup** and your full name in the message. The addresses are in the syllabus. Tell us what you already tried.

Two are worth knowing about in advance.

**Docker will not start on Windows.** Almost always the virtualisation setting. Check it again.

**Docker will not start at all.** Tell us early. Sorting this out with you in September is easy. Finding out in October is not.
