#!/bin/bash
#auto restore workspace
#by author Jerling 2018

SOFTWARE="git zsh vim tmux rofi cmake global"

function install_am()
{
    `INSTALL -S gcc g++ adobe-source-code-pro-fonts $SOFTWARE`
}

function install_dud()
{
    `INSTALL -y build-essential $SOFTWARE`
}

function install_rcf()
{
    `INSTALL -y gcc gcc-c++ $SOFTWARE`
}

echo "What is your OS?"
select os in "Arch/Manjaro" "Debain/Ubuntu/Deepin" "RedHat/Centos/Fedaro" "Over"
do
    echo $os
    case $os in
        "Arch/Manjaro")
            INSTALL="sudo pacman -S"
            install_am;;
        "Debain/Ubuntu/Deepin")
            INSTALL="sudo apt install -y"
            install_dud;;
        "RedHat/Centos/Fedaro")
            INSTALL="sudo yum install -y"
            install_rcf;;
        "Over")
            break;;
        *)
            echo "Not Support!"
            exit
    esac
    break
done

# install spacemacs
echo "Install spacemacs ?"
select EMACS in "Y" "N"
do
    if $EMACS == "Y"
      `INSTALL emacs`
      git clone -b develop https://github.com/syl20bnr/spacemacs ~/.emacs.d
      git clone https://gitee.com/Jerling/spacemacs-private.git ~/.spacemacs.d
      emacs &
    fi
    break
done

if [ ! -d  ~/dotfiles ]
then
  git https://github.com/Jerling/dotfiles.git ~/dotfiles
fi

# install space-vim
bash <(curl -fsSL https://raw.githubusercontent.com/liuchengxu/space-vim/master/install.sh)
rm -rf ~/.spacevim
ln -s -f ~/dotfile/config/spacevim ~/.spacevim
ln -s -f  ~/dotfiles/config/org.snippets ~/.vim/plugged/org-snippets/snippets
ln -s -f ~/dotfiles/config/tmux/.tmux.conf ~
cp ~/dotfiles/config/tmux/.tmux.conf.local ~

# wm config
echo "Select Your Window Manager?"
select wm in "i3" "qtile" "none"
do
    case $wm in
        "i3")
            rm ~/.i3/config
            cp config/i3/config ~/.i3/config
            ;;
        "qtile")
            cp config/qtile ~/.config/
            ;;
        *)
            break;;
    esac
    break
done

# install oh-my-zsh
cd ~ && sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

echo "Done!"
