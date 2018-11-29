### .bash_profile

```bash
# general path
export PATH=/bin:/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:$PATH

# color
export CLICOLOR=1
export LSCOLORS='ExGxFxdaCxDaDahbadacec'
export PS1="\[\033[38;5;11m\]\u@\[$(tput sgr0)\]\[\033[38;5;13m\]\h\[$(tput sgr0)\]\[\033[38;5;10m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]> \[$(tput sgr0)\]"

# history search
export HISTSIZE=1000000
export HISTFILESIZE=1000000000
if [[ $- == *i* ]]
then
    bind '"\e[A": history-search-backward'
    bind '"\e[B": history-search-forward'
fi

# Alias definitions
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
```

### .bash_aliases

```bash
alias ll='ls -l -h'
alias la='ls -l -a -h'
alias jn='jupyter-notebook'
alias ..='cd ..'
alias myalias='cat .bash_aliases'
alias sc='source ~/.bash_profile'
# alias sc='source ~/.bashrc'
```

### .inputrc
```bash
# tab complete
set completion-ignore-case on
set show-all-if-ambiguous on
TAB: menu-complete
```

