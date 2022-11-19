LoL match history analysis
==============================

A project to analyze league of legends match data.

Requirements to run
------------
- [Riot developer API key](https://developer.riotgames.com/)
- Python installation or docker

Development
------------

Copy the file .env.default to .env and replace setting values with your own (API-key, region, data save-path etc.). Download data from riot-api using doit as described below. You can then start a notebook server with ```jupyter lab``` and explore the data.

Use ```doit``` to run tasks like make_dataset, linting and tests:

``` bash
doit help make_dataset
doit make_dataset -s "summoner 1" -s summoner2
doit lint
doit pytest
```

Using docker
------------
To build a docker image, start a container (as your current user/group), mount current directory and connect to the container:

``` bash
docker build -t riot -f Dockerfile .
docker run -d --rm -it --user $(id -u):$(id -g) --volume $(pwd):/workspace --name riot riot
docker exec -it riot /bin/bash
```

Using python
------------
If you want to use python environments instead, use the commands below. That creates a virtual python environment in your current folder, activates it and installs dependencies with pip

``` bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Project Organization
------------

    ├── LICENSE
    ├── dodo.py            <- Makefile-like multiplatform CLI
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources (ex. script config files)
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- Documentation
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── lol_match_history  <- Source code for use in this project.
    │   ├── __init__.py    <- Makes riot a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │                     predictions
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    |
    ├── Dockerfile         <- Dockerfile with settings to run scripts in Docker container
    ├── dvc.yaml           <- DVC pipeline; see dvc.org
    ├── params.yaml        <- Parameter values (things like hyperparameters) used by DVC pipeline
    ├── setup.cfg          <- config file with settings for running pylint, flake8 and bandit
    └── pytest.ini         <- config file with settings for running pytest

------------
<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience.</small>
