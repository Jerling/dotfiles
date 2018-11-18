#!/bin/bash
#auto restore workspace
#by author Jerling 2018

Software="git zsh vim emacs rofi cmake global"

function install_am()
{
    sudo pacman -S gcc g++ adobe-source-code-pro-fonts $Software
}

function install_dud()
{
    sudo apt-get install -y build-essential $Software
}

function install_rcf()
{
    sudo yum install -y gcc gcc-c++ $Software
}

echo "What is your OS?"
select os in "Arch/Manjaro" "Debain/Ubuntu/Deepin" "RedHat/Centos/Fedaro" "Over"
do
    case $os in
        "Arch/Manjaro")
            install_am;;
        "Debain/Ubuntu.Debain")
            install_dud;;
        "RedHat/Centos/Fedaro")
            install_rcf;;
        "Over")
            break;
        *)
            echo "Not Support!"
            exit
    esac
    break
done

# install spacemacs
git clone -b develop https://github.com/syl20bnr/spacemacs ~/.emacs.d
git clone https://gitee.com/Jerling/spacemacs-private.git ~/.spacemacs.d
emacs &

if [ -d "./config/vimplus"]
then
    cd ./config/vimplus && sh ./install.sh
    cd -

# wm config
rm ~/.Xresources
rm ~/.i3/config
cp config/urxvrt/Xresources ~/.Xresources
cp config/i3/config ~/.i3/config

# install oh-my-zsh
cd ~ && sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

echo "Done!"
