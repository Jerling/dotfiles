#!/usr/bin/env python
#-*-coding:utf-8-*-

import os

from libqtile import layout,widget,bar,manager,hook
from libqtile.widget import base
from libqtile.manager import Screen,Drag
from libqtile.command import lazy
try:
    from libqtile.manager import Key,Group
except ImportError:
    from libqtile.config import Key,Group

sup='mod4'
alt='mod1'

#键位映射
keys=[
    #Layout
    Key([sup],'Down',lazy.layout.down()),
    Key([sup],'Up',lazy.layout.up()),
    Key([alt],'Tab',lazy.layout.next()),
    Key([alt,'shift'],'Tab',lazy.layout.previous()),
    Key([sup],'space',lazy.nextlayout()),
    Key([sup],'k',lazy.layout.increase_ratio()),
    Key([sup],'j',lazy.layout.decrease_ratio()),
    # 和emacs 冲突
    # Key([alt],'l',lazy.layout.increase_nmaster()),
    # Key([alt],'h',lazy.layout.decrease_nmaster()),

    #Window
    Key([sup],'w',lazy.window.kill()),
    Key([sup],'m',lazy.window.toggle_maximize()),

    #Group
    Key([sup],'Left',lazy.group.prevgroup()),
    Key([sup],'Right',lazy.group.nextgroup()),


    #Application launchers
    Key([sup],'Return',lazy.spawn('deepin-terminal')),
    Key([sup],'f',lazy.spawn('firefox')),
    Key([sup],'v',lazy.spawn('vmware')),
    Key([sup],'e',lazy.spawn('dde-file-manager')),
    Key([sup],'a',lazy.spawn('rofi -show window')),
    Key([sup],'z',lazy.spawn('rofi -show run')),

    #Audio
    Key([sup],'F8',lazy.spawn('amixer --quiet set Master mute')),
    Key([sup],'F9',lazy.spawn('amixer --quiet set Master unmute')),
    Key([alt],'minus',lazy.spawn('amixer --quiet set Master 2dB-')),
    Key([alt,'shift'],'equal',lazy.spawn('amixer --quiet set Master 2dB+')),

    #restart qtile
    Key([sup],'r',lazy.restart()),
    #shutdown
    Key([sup,'shift'],'q',lazy.spawn('shutdown -h now')),

    #interact with prompts:
    Key([sup],'s',lazy.spawncmd()),    
]

mouse=[
    Drag([sup],"Button1",lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([sup],"Button3",lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
]

#建立groups
group_names=[
    ("study",{'layout':'tile'}),
    ("work",{"layout":'tile'}),
    ("web",{"layout":"max"}),
    ("vbox",{"layout":"max"}),
    ('music',{'layout':'max'}),
    ('doc',{'layout':'max'}),
    ('chat',{'layout':'max'})
]

groups=[Group(name,**kwargs) for name,kwargs in group_names]

for i , (name,kwargs) in enumerate(group_names,1):
    keys.append(Key([sup],str(i),lazy.group[name].toscreen()))
    keys.append(Key([sup,'shift'],str(i),lazy.window.togroup(name)))

#建立layouts
layouts=[
    layout.Tile(border_focus='#196ff2',border_width=1),
    layout.Max()
]



font='NotoSans'
fontsize=16
foreground='#FFFFFF'
background='#000000'


def humanize_bytes(value):
    suff=['B','K','M','G','T']
    while value > 1024. and len(suff)>1:
        value/=1024.
        suff.pop(0)
    return "% 3s%s" %('%.3s'%value,suff[0])


#本来这个是用来显示CPU、Mem、Net的情况，后来不知为何无法显示
class Metrics(base._TextBox):
    
    defaults=[
        ('font','Arial','Metrics font'),
        ('fontsize',None,'Metircs pixel size'),
        ('pading',None,'Metrics padding'),
        ('background','00000','background color'),
        ('foreground','ffffff','foreground color')
        ]


    def __init__(self,**kwargs):
        base._TextBox.__init__(self,**kwargs)
        self.cpu_usage,self.cpu_total=self.get_cpu_stat()
        self.interfaces={}
        self.idle_ifaces={}

    def _configure(self,qtile,bar):
        base._TextBox._configure(self,qtile,bar)
        self.timeout_add(0,self._update)

    def get_cpu_stat(self):
        stat=[int(i) for i in open('/proc/stat').readline().split()[1:]]
        return sum(stat[:3]),sum(stat)

    def get_cpu_usage(self):
        new_cpu_usage,new_cput_total=self.get_cpu_stat()
        cput_usage=new_cpu_usage-self.cpu_usage
        cpu_total=new_cpu_total-self.cpu_total
        self.cpu_usage=new_cpu_usage
        self.cpu_tptal=new_cpu_total
        return 'Cpu: %d%%' % (float(cpu_usage)/float(cpu_total)*100.)

    def get_mem_usage(self):
        info={}
        for line in open('/proc/meminfo'):
            key,val=line.split(':')
            info[key]=int(val.spilt()[0])
        mem=info['MemTotal']
        mem-=info['MemFree']
        mem-=info['Buffers']
        mem-=info['Cached']
        return 'Mem: %d%%' % (float(mem)/float(info['MemTotal'])*100)

    def get_net_usage(self):
        interfaces=[]
        basedir='/sys/class/net'
        for iface in os.listdir(basedir):
            j=os.path.join
            ifacedir=j(basedir,iface)
            statdir=j(ifacedir,'statistics')
            idle=iface in self.idle_ifaces
            try:
                if int(open(j(ifacedir, 'carrier')).read()):
                    rx = int(open(j(statdir, 'rx_bytes')).read())
                    tx = int(open(j(statdir, 'tx_bytes')).read())
                    if iface not in self.interfaces:
                        self.interfaces[iface] = (rx, tx)
                    old_rx, old_tx = self.interfaces[iface]
                    self.interfaces[iface] = (rx, tx)
                    rx = rx - old_rx
                    tx = tx - old_tx
                    if rx or tx:
                        idle = False
                        self.idle_ifaces[iface] = 0
                        rx = humanize_bytes(rx)
                        tx = humanize_bytes(tx)
                        interfaces.append('%s: %s / %s' % (iface, rx, tx))
            except:
                pass
            if idle:
                interfaces.append('%s: %-11s' % (iface, ("%ds idle" % self.idle_ifaces[iface]))
                )
                self.idle_ifaces[iface] += 1
                if self.idle_ifaces[iface] > 30:
                    del self.idle_ifaces[iface]
        return " | ".join(interfaces)
    

    def _update(self):
        self.update()
        self.timeout_add(1, self.update)
        return False

    def update(self):
        stat = [self.get_cpu_usage(), self.get_mem_usage()]
        net = self.get_net_usage()
        if net:
            stat.append(net)
        self.text = " | ".join(stat)
        self.bar.draw()
        return True


screens=[
    Screen(
        bottom=bar.Bar(
            [
                widget.TextBox(text='◤ ',fontsize=40,foreground='#323335',padding=0),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.TextBox("default config", name="default"),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            24,
        ),
    ),
    Screen(bottom=bar.Bar([
        widget.TextBox(text='◤ ',fontsize=40,foreground='#323335',padding=0),
        widget.GroupBox(font=font,fontsize=fontsize,active=foreground,inactive="#808080",borderwidth=3),
        widget.Prompt(font=font,fontsize=fontsize),
        widget.CurrentLayout(font=font,foreground=foreground,fontsize=fontsize),
        widget.Sep(foreground=background,linewidth=3),
        widget.WindowName(font=font,fontsize=fontsize,foreground=foreground),
        widget.Notify(font=font,fontsize=fontsize),
        Metrics(font=font,fontsize=fontsize,foreground=foreground),
        widget.Volume(foreground="#70ff70"),
        widget.BatteryIcon(),
        widget.Systray(icon_size=18),
        widget.Clock(font=font,fontsize=fontsize,foreground=foreground,fmt='%Y-%m-%d %a %H:%M'),
    ],30))
]


@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True
