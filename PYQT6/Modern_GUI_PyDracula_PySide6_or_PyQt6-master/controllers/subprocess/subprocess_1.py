import subprocess


def runcmd(command):
    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk',
                         timeout=1)
    if ret.returncode == 0:
        print('sucess:', ret)
    else:
        print('error:', ret)


runcmd(['dir', '-b'])
