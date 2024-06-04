Forensic - SignMyRar5
=======================

Enoncé
---------

- A compléter 

Résolution
---------------

1. On récupère l'archive du fichier et on l'ouvre avec le mot de passe
2. On récupère le dump mémoire et on commencer à l'analyser avec volatility

D'abord on récupère le profile de l'image :

.. code-block:: console

    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp imageinfo 

Il s'agit d'un profil Windows XP : 

.. code-block:: console

    Volatility Foundation Volatility Framework 2.6
    INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/kubow/Tools/volatility_2.6_lin64_standalone/Forensic - SignMyRar5.dmp)
                      PAE type : PAE
                           DTB : 0xaf8000L
                          KDBG : 0x8054d2e0L
          Number of Processors : 2
        Image Type (Service Pack) : 3
                    KPCR for CPU 0 : 0xffdff000L
                    KPCR for CPU 1 : 0xbab38000L
                KUSER_SHARED_DATA : 0xffdf0000L
            Image date and time : 2024-04-21 19:05:41 UTC+0000
        Image local date and time : 2024-04-21 21:05:41 +0200


On part à la recherche de l'archive rar dans le dump : 

.. code-block:: console

    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp profile=WinXPSP2x86 filescan | grep "rar"

Mais la recherche sur "rar" ne donne rien : 

.. code-block:: console

    Volatility Foundation Volatility Framework 2.6
    0x0000000009503408      2      1 RW-rw- \Device\HarddiskVolume1\Documents and Settings\Administrateur\Local Settings\Temporary Internet Files\Content.IE5\index.dat
    0x0000000009a8df60      1      1 RW-rw- \Device\HarddiskVolume1\Documents and Settings\Administrateur\Local Settings\Temporary Internet Files\Content.IE5\index.dat
    0x0000000009ac1570      2      1 RW-rw- \Device\HarddiskVolume1\Documents and Settings\LocalService\Local Settings\Temporary Internet Files\Content.IE5\index.dat

On va chercher d'autre fichiers utiles : 

.. code-block:: console

    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp profile=WinXPSP2x86 filescan | grep "txt"

Ah la ça devient intéressant ! 

.. code-block:: console

    Volatility Foundation Volatility Framework 2.6
    0x00000000095336d0      1      0 R--rwd \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\manifest.txt
    0x0000000009536ca0      4      2 -W-rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware VGAuth\logfile.txt.0
    0x000000000954bd08      1      0 R--rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\Unity Filters\win7gadgets.txt
    0x000000000954bf90      1      0 R--rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\Unity Filters\vmwarefilters.txt
    0x00000000095568b8      1      0 R--r-- \Device\HarddiskVolume1\System Volume Information\_restore{0E4A1252-3B4D-4419-8C36-EE82040C97D3}\drivetable.txt
    0x000000000955c220      1      0 R--rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\Unity Filters\microsoftoffice.txt
    0x00000000095a7ba0      1      0 R--rw- \Device\HarddiskVolume1\Program Files\VMware\VMware Tools\vmacthlp.txt
    0x00000000095ae218      1      0 R--rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\Unity Filters\adobeflashcs3.txt
    0x0000000009abe310      1      0 RW-r-- \Device\HarddiskVolume1\Documents and Settings\Administrateur\Bureau\README.txt
    0x0000000009ac9228      1      0 R--rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\Unity Filters\vistasidebar.txt
    0x0000000009aeec38      1      0 R--rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\Unity Filters\visualstudio2005.txt
    0x0000000009af4218      1      0 R--rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\Unity Filters\adobephotoshopcs3.txt
    0x0000000009b13f28      1      0 R--rw- \Device\HarddiskVolume1\Documents and Settings\All Users\Application Data\VMware\VMware Tools\Unity Filters\googledesktop.txt
    0x0000000009cb8388      1      0 R--rwd \Device\HarddiskVolume1\Documents and Settings\Administrateur\Mes documents\RarFile.txt


Les deux fichiers qui vont nous intéresser ici : 

- \Device\HarddiskVolume1\Documents and Settings\Administrateur\Bureau\README.txt
- \Device\HarddiskVolume1\Documents and Settings\Administrateur\Mes documents\RarFile.txt


On va refaire tout de même la recherche sur "Rar" plutôt que "rar" pour être sur : 

.. code-block:: console

    Volatility Foundation Volatility Framework 2.6
    0x0000000009b46f90      1      0 RW-rw- \Device\HarddiskVolume1\Documents and Settings\Administrateur\Recent\RarFile.lnk
    0x0000000009cb8388      1      0 R--rwd \Device\HarddiskVolume1\Documents and Settings\Administrateur\Mes documents\RarFile.txt

Et on trouve un fichier de plus, un lnk probablement du txt. 

On va télécharger tous ces fichiers et voir ce qu'ils contiennent : 

.. code-block:: console

    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp profile=WinXPSP2x86 dumpfiles -Q 0x0000000009abe310 -D test # README
    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp profile=WinXPSP2x86 dumpfiles -Q 0x0000000009cb8388 -D test # RarFile.txt
    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp profile=WinXPSP2x86 dumpfiles -Q 0x0000000009b46f90 -D test # RarFile.lnk


On regarde leur contenu : 

.. code-block:: console

    $ strings test/RarFile.txt 
    Malheureusement ils ont supprim
    s l'archive, j'arrive pas 
    la retrouver...

    $ strings test/readme.txt 
    J'ai r
    la derni
    re archive qui contient les patchs de s
    curit
    , tu trouveras un fichier rar contenant le patch de s
    curit
    . Voici le mot de passe : dhZIDHndzj45


On a le mot de passe de l'archive : dhZIDHndzj45

Mais toujours pas d'archive !

On va tenter la MFT, qui pourraient contenir plus de données avec un peu de chance


.. code-block:: console

    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp profile=WinXPSP2x86 mftparser | grep -A 15 -B 15 "Rar"


Malheureusement pas plus d'informations : 

.. code-block:: console

    Volatility Foundation Volatility Framework 2.6
    ***************************************************************************
    MFT entry found at offset 0x1f1e4400
    Attribute: In Use & File
    Record Number: 11057
    Link count: 1


    $STANDARD_INFORMATION
    Creation                       Modified                       MFT Altered                    Access Date                    Type
    ------------------------------ ------------------------------ ------------------------------ ------------------------------ ----
    2024-04-21 19:04:52 UTC+0000 2024-04-21 19:05:09 UTC+0000   2024-04-21 19:05:09 UTC+0000   2024-04-21 19:05:09 UTC+0000   Archive

    $FILE_NAME
    Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
    ------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
    2024-04-21 19:04:52 UTC+0000 2024-04-21 19:04:52 UTC+0000   2024-04-21 19:04:52 UTC+0000   2024-04-21 19:04:52 UTC+0000   Documents and Settings\ADMINI~1\MESDOC~1\RarFile.txt

    $OBJECT_ID
    Object ID: 92b42cd7-1100-ef11-aa7c-000c29501a69
    Birth Volume ID: 80000000-6800-0000-0000-180000000100
    Birth Object ID: 4b000000-1800-0000-4d61-6c6865757265
    Birth Domain ID: 7573656d-656e-7420-696c-73206f6e7420

    $DATA
    0000000000: 4d 61 6c 68 65 75 72 65 75 73 65 6d 65 6e 74 20   Malheureusement.
    0000000010: 69 6c 73 20 6f 6e 74 20 73 75 70 70 72 69 6d e9   ils.ont.supprim.
    0000000020: 73 20 6c 27 61 72 63 68 69 76 65 2c 20 6a 27 61   s.l'archive,.j'a
    0000000030: 72 72 69 76 65 20 70 61 73 20 e0 20 6c 61 20 72   rrive.pas...la.r
    0000000040: 65 74 72 6f 75 76 65 72 2e 2e 2e                  etrouver...

    ***************************************************************************
    ***************************************************************************
    MFT entry found at offset 0x1f1e4800
    Attribute: In Use & File
    Record Number: 11058
    Link count: 1


    $STANDARD_INFORMATION
    Creation                       Modified                       MFT Altered                    Access Date                    Type
    ------------------------------ ------------------------------ ------------------------------ ------------------------------ ----
    2024-04-21 19:05:00 UTC+0000 2024-04-21 19:05:00 UTC+0000   2024-04-21 19:05:00 UTC+0000   2024-04-21 19:05:00 UTC+0000   Archive

    $FILE_NAME
    Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
    ------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
    2024-04-21 19:05:00 UTC+0000 2024-04-21 19:05:00 UTC+0000   2024-04-21 19:05:00 UTC+0000   2024-04-21 19:05:00 UTC+0000   Documents and Settings\ADMINI~1\Recent\RarFile.lnk

    $DATA
    0000000000: 4c 00 00 00 01 14 02 00 00 00 00 00 c0 00 00 00   L...............
    0000000010: 00 00 00 46 9b 00 00 00 20 00 00 00 9a 0f 52 ca   ...F..........R.
    0000000020: 1e 94 da 01 9a 0f 52 ca 1e 94 da 01 9a 0f 52 ca   ......R.......R.
    0000000030: 1e 94 da 01 00 00 00 00 00 00 00 00 01 00 00 00   ................
    0000000040: 00 00 00 00 00 00 00 00 00 00 00 00 5e 00 14 00   ............^...
    0000000050: 1f 48 ba 8f 0d 45 25 ad d0 11 98 a8 08 00 36 1b   .H...E%.......6.
    0000000060: 11 03 48 00 32 00 00 00 00 00 95 58 9b 98 20 00   ..H.2......X....
    0000000070: 52 61 72 46 69 6c 65 2e 74 78 74 00 2e 00 03 00   RarFile.txt.....
    0000000080: 04 00 ef be 95 58 9b 98 95 58 9b 98 14 00 00 00   .....X...X......
    0000000090: 52 00 61 00 72 00 46 00 69 00 6c 00 65 00 2e 00   R.a.r.F.i.l.e...
    00000000a0: 74 00 78 00 74 00 00 00 1a 00 00 00 71 00 00 00   t.x.t.......q...
    00000000b0: 1c 00 00 00 01 00 00 00 1c 00 00 00 2d 00 00 00   ............-...
    00000000c0: 00 00 00 00 70 00 00 00 11 00 00 00 03 00 00 00   ....p...........
    00000000d0: f9 5a d9 10 10 00 00 00 00 43 3a 5c 44 6f 63 75   .Z.......C:\Docu
    00000000e0: 6d 65 6e 74 73 20 61 6e 64 20 53 65 74 74 69 6e   ments.and.Settin
    00000000f0: 67 73 5c 41 64 6d 69 6e 69 73 74 72 61 74 65 75   gs\Administrateu
    0000000100: 72 5c 4d 65 73 20 64 6f 63 75 6d 65 6e 74 73 5c   r\Mes.documents\
    0000000110: 52 61 72 46 69 6c 65 2e 74 78 74 00 00 1c 00 2e   RarFile.txt.....
    0000000120: 00 2e 00 5c 00 4d 00 65 00 73 00 20 00 64 00 6f   ...\.M.e.s...d.o
    0000000130: 00 63 00 75 00 6d 00 65 00 6e 00 74 00 73 00 5c   .c.u.m.e.n.t.s.\
    0000000140: 00 52 00 61 00 72 00 46 00 69 00 6c 00 65 00 2e   .R.a.r.F.i.l.e..
    0000000150: 00 74 00 78 00 74 00 36 00 43 00 3a 00 5c 00 44   .t.x.t.6.C.:.\.D
    0000000160: 00 6f 00 63 00 75 00 6d 00 65 00 6e 00 74 00 73   .o.c.u.m.e.n.t.s
    0000000170: 00 20 00 61 00 6e 00 64 00 20 00 53 00 65 00 74   ...a.n.d...S.e.t
    0000000180: 00 74 00 69 00 6e 00 67 00 73 00 5c 00 41 00 64   .t.i.n.g.s.\.A.d
    0000000190: 00 6d 00 69 00 6e 00 69 00 73 00 74 00 72 00 61   .m.i.n.i.s.t.r.a
    00000001a0: 00 74 00 65 00 75 00 72 00 5c 00 4d 00 65 00 73   .t.e.u.r.\.M.e.s
    00000001b0: 00 20 00 64 00 6f 00 63 00 75 00 6d 00 65 00 6e   ...d.o.c.u.m.e.n
    00000001c0: 00 74 00 73 00 10 00 00 00 05 00 00 a0 05 00 00   .t.s............
    00000001d0: 00 14 00 00 00 60 00 00 00 03 00 00 a0 58 00 00   .....`.......X..
    00000001e0: 00 00 00 00 00 6d 63 74 66 2d 62 34 31 39 62 36   .....mctf-b419b6
    00000001f0: 37 65 35 63 00 1e a9 39 02 5d 3c 51 4b be b6 7c   7e5c...9.]<QK..|
    0000000200: f7 aa 93 03 09 92 b4 2c d7 11 00 ef 11 aa 7c 00   .......,......|.


On va donc s'intéresser à la corbeille, attention il faut chercher "RECYCLE"

.. code-block:: console

    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp profile=WinXPSP2x86 filescan | grep "RECYCLE"

Il y a 3 fichiers qui sont présent : 

.. code-block:: console

    Volatility Foundation Volatility Framework 2.6
    0x00000000094f7998      1      0 R--rwd \Device\HarddiskVolume1\RECYCLER\S-1-5-21-1202660629-448539723-725345543-500\desktop.ini
    0x0000000009a7dad0      1      0 R--rw- \Device\HarddiskVolume1\RECYCLER\S-1-5-21-1202660629-448539723-7253455
    0x0000000009cb3df8      1      0 RW---- \Device\HarddiskVolume1\RECYCLER\S-1-5-21-1202660629-448539723-725345543-500\INFO2


On va télécharger les trois, et le deuxième donne un résultat intéressant lorsqu'on fait un strings dessus : 

.. code-block:: console

    ./volatility_2.6_lin64_standalone -f Forensic\ -\ SignMyRar5.dmp profile=WinXPSP2x86 dumpfiles -Q 0x0000000009a7dad0 -D test 


    $ strings test/file.None.0x89886c98.dat 
    flag0
    93Ob!
    l2$[
    {RB}
    flag0
    93Ob!
    l2$[


Cependant, lorsqu'on le renomme en archive.rar, il s'ouvre mais rien n'apparaît, pas de prompt de mot de passe, pas de fichier.

Après avoir demandé conseil j'ai examiné le fichier en hexadecimal : 

.. code-block:: console

    $ xxd archive.rar
    00000000: ffff ffff 1a07 0100 6b85 ba73 0d01 0509  ........k..s....
    00000010: 0808 0103 8080 0098 8100 9158 ae06 5102  ...........X..Q.
    00000020: 033c b000 04a0 0020 0983 84f5 8005 0004  .<..... ........
    00000030: 666c 6167 3001 0003 0fde d33c b71b f99a  flag0......<....
    00000040: 18d0 e739 334f 6221 c017 0f03 6e96 a16a  ...93Ob!....n..j
    00000050: 087d 93a3 796d d9a5 1551 acf0 6c32 245b  .}..ym...Q..l2$[
    00000060: f410 acbc 2a0a 0302 eb83 4b40 0294 da01  ....*.....K@....
    00000070: c4b2 a111 b7dd 503b 6cca 56de 61c4 2288  ......P;l.V.a.".
    00000080: 884c e1d5 ecba 7e07 f191 189f 0140 71a8  .L....~......@q.
    00000090: 9f67 0232 44e4 84a2 835d 53b7 94d9 2f55  .g.2D....]S.../U
    000000a0: 2ff2 73d3 1203 0703 f001 00f0 0100 8000  /.s.............
    000000b0: 0002 5252 0207 037b 5242 7dd1 d87d 1378  ..RR...{RB}..}.x
    000000c0: 6cda 61f0 0000 0050 0000 0001 0100 0000  l.a....P........
    000000d0: 0000 0000 00a0 0000 00a0 0000 0000 0000  ................
    000000e0: 00a0 0000 0000 0000 00f0 0000 0000 0000  ................
    000000f0: 0001 0001 0000 00e6 76cd d668 782c 88b3  ........v..hx,..
    00000100: 0f05 44dd 859a 6eff ffff ff1a 0701 006b  ..D...n........k
    00000110: 85ba 730d 0105 0908 0801 0380 8000 9881  ..s.............
    00000120: 0091 58ae 0651 0203 3cb0 0004 a000 2009  ..X..Q..<..... .
    00000130: 8384 f580 0500 0466 6c61 6730 0100 030f  .......flag0....
    00000140: ded3 3cb7 1bf9 9a18 d0e7 3933 4f62 21c0  ..<.......93Ob!.
    00000150: 170f 036e 96a1 6a08 7d93 a379 6dd9 a515  ...n..j.}..ym...
    00000160: 51ac f06c 3224 5bf4 10ac bc2a 0a03 02eb  Q..l2$[....*....
    00000170: 834b 4002 94da 01c4 b2a1 11b7 dd50 3b6c  .K@..........P;l
    00000180: ca56 de61 c422 8888 4ce1 d5ec ba7e 07f1  .V.a."..L....~..
    00000190: 9118 9f01 4071 a89f 6702 3244 e484 a283  ....@q..g.2D....
    000001a0: 5d53 b794 d92f 551d 7756 5103 0504 0000  ]S.../U.wVQ.....


Ce site m'a permis de découvrir que la signature du RAR était corrompue : https://ctf-wiki.mahaloz.re/misc/archive/rar/ 

Normalement, un fichier RAR doit commencer par 52 61 72 21 1A 07 00 

Or on peut voir que nous avons : ffff ffff 1a07 0

On va donc ouvrir le rar avec hexedit et on saisit 52 61 72 21 pour remplacer les ff ff ff ff 

On ferme et on sauvegarde, on rouvre l'archive et la bingo ! On a un fichier flag et le prompt du mot de passe 

On utilise le mot de passe et on obtient le flag : MCTF{H3ll0_H4ck3r_Y0u-F1nd_D4t4} 