# project-image-captioning

Some experiments with automated captioning of project images

## Machine Setup

```bash
sudo apt update
sudo apt upgrade
```

Possibly reboot if there is a kernel update

```bash
sudo apt install python3-pip
sudo apt install python-is-python3
sudo pip install pipenv

git config --global user.name "First Last"
git config --global user.email "user@example.com"

git clone https://github.com/MILL-LX/project-image-captioning.git

cd project-image-captioning
pipenv install
pipenv shell

python generate_captions.py --clear-output
```
