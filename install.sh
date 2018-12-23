#!/bin/bash
#auto restore workspace
#by author Jerling 2018

SOFTWARE="git zsh vim tmux rofi cmake make tig shellcheck"

function install_am()
{
    `$INSTALL gcc adobe-source-code-pro-fonts bat tldr $SOFTWARE`
}

function install_dud()
{
    `$INSTALL -y build-essential $SOFTWARE`
}

function install_rcf()
{
    `$INSTALL -y gcc gcc-c++ $SOFTWARE`
}

function install_gen()
{
    `$INSTALL dev-vcs/git app-shells/zsh app-editors/vim app-misc/tmux dev-util/cmake dev-vcs/tig dev-util/shellcheck app-editors/emacs`
}

echo "What is your OS?"
select os in "Arch/Manjaro" "Debain/Ubuntu/Deepin" "RedHat/Centos/Fedaro" "Gentoo" "Over"
do
    echo $os
    case $os in
        "Arch/Manjaro")
            INSTALL="sudo pacman -S"
            install_am && yaourt -S global;;
        "Debain/Ubuntu/Deepin")
            INSTALL="sudo apt install -y"
            install_dud;;
        "RedHat/Centos/Fedaro")
            INSTALL="sudo yum install -y"
            install_rcf;;
        "Gentoo")
            INSTALL="sudo emerge"
            install_gen;;
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
    case $EMACS in
        "Y")
            "$INSTALL emacs"
            if [ ! -d ~/data/elpa ]
            then
                mkdir ~/data/elpa
            fi
            rsync -avzP rsync://mirrors.tuna.tsinghua.edu.cn/elpa/melpa ~/data/elpa && rsync -avzP rsync://mirrors.tuna.tsinghua.edu.cn/elpa/gnu ~/data/elpa && rsync -avzP 
rsync://mirrors.tuna.tsinghua.edu.cn/elpa/org ~/data/elpa
            git clone -b develop https://github.com/syl20bnr/spacemacs ~/.emacs.d
            git clone https://gitee.com/Jerling/spacemacs-private.git ~/.spacemacs.d
            emacs &
            ;;
        "N")
            break;;
        *)
            break;;
    esac
    break
done

if [ ! -d  ~/dotfiles ]
then
    git clone https://github.com/Jerling/dotfiles.git ~/dotfiles
fi

# install space-vim
git clone https://github.com/liuchengxu/space-vim/ .space-vim && bash .space-vim/install.sh
rm -f ~/.spacevim
ln -s -f ~/dotfiles/config/spacevim ~/.spacevim && vim
cp -f ~/dotfiles/config/snippets ~/.vim/plugged/org-snippets/snippets
ln -s -f ~/dotfiles/config/tmux/.tmux.conf ~
cp ~/dotfiles/config/tmux/.tmux.conf.local ~

# wm config
echo "Select Your Window Manager?"
select wm in "i3" "qtile" "none"
do
    case $wm in
        "i3")
            mv ~/.i3/config ~/.i3/config.bak
            ln -s -f ~/dotfiles/config/i3/config ~/.i3/config
   	   		 ln -s -f ~/dotfiles/config/i3/i3blocks.conf ~/.i3blocks.conf
            cp -s -f ~/dotfiles/config/urxvrt/Xresources .Xresources
            ;;
        "qtile")
            cp ~/dotfiles/config/qtile ~/.config/
            ;;
        *)
            break;;
    esac
    break
done

# install oh-my-zsh
cd ~ && sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

echo "Done!"
