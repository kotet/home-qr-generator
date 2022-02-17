FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tzdata \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* \
    && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo 'Asia/Tokyo' >/etc/timezone

RUN apt-get update \
    && apt-get install -y \
        git sudo vim bash-completion rsync wget curl \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -m vscode \
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

RUN apt-get update \
    && apt-get install -y \
        build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev libgdbm-dev libbz2-dev liblzma-dev zlib1g-dev uuid-dev libffi-dev libdb-dev tk-dev \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*


RUN apt-get update \
    && apt-get install -y \
        fonts-noto-mono \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

USER vscode
ENV HOME /home/vscode

ENV PYTHON_VERSION 3.10.2
ENV PYTHON_ROOT $HOME/local/python-$PYTHON_VERSION
ENV PATH $PYTHON_ROOT/bin:$HOME/.poetry/bin:$PATH

RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv \
    && cd ~/.pyenv/plugins/python-build \
    && PREFIX=~/local ./install.sh \
    && ~/local/bin/python-build -v ${PYTHON_VERSION} ~/local/python-${PYTHON_VERSION}

ENV PATH "$PATH:/home/vscode/local/python-${PYTHON_VERSION}/bin"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
RUN poetry completions bash | sudo tee /etc/bash_completion.d/poetry.bash-completion
ENV PATH "$PATH:/home/vscode/.poetry/bin"

RUN poetry config virtualenvs.in-project true