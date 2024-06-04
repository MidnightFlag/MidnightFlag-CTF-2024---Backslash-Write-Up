# Weger's Attack
from sage.all import *

from Crypto.Util.number import long_to_bytes

def compute_gamma(n, r):
    def recursive_loop(n, r, start=0, deepth=0, max_deepth=0):
        if deepth == max_deepth:
            return n / (n^(deepth/r))
        else:
            S = 0
            for i in range(start, r):
                S += recursive_loop(n, r, i+1, deepth+1, max_deepth)
            return S

    gamma = 0
    for i in range(r):
        gamma += (-1)**i * recursive_loop(n, r, max_deepth=i+1)

    return int(gamma) + (-1)**r


def attack(n, e, r):
    print('[+] Computing T')

    T = compute_gamma(n, r)    
    m = int(n - T)
    a = continued_fraction(Integer(e) / Integer(m))
    print('[+] Searching over convergents')
    for i in a.convergents():
        k = i.numerator()
        d = i.denominator()
        if pow(pow(2,e,n),d,n) == 2:
            print('[+] D & phi found !')
            phi = (e*d - 1)/k
            return d, phi, k
    return None, None, None


e=167684882076591361795739750449616296794055336034223296698178706012784501236537143842143876795558488353549531449162397077410771366086673950242138091641993694893241442755504937236228933248478688708163461058490234672523872521038287556954933994882249548214980659608627912009244424730349088577197831395141127585571432086148266586434951179210752833991660016216772278964461709725687849340905464528124764943176249094254653089756078247879979448094046389013356316284314630852041004671511945614690437658589733751199872991061972223522928924048569085860990641806953184183910201319899738942102380624065178381548596595496127028269
n=182978936939260533597192686270253290628534600772854660185466156332243697913756296294583241371304814481078380108450349645191056343679402519517187252897343437712074952724817176468832139095114880686571565165976176744559116654712696570029067022912004861577563694536429052143070501621522803082795939115452297963015534345203912712377973388247125325978165186719827907679608938628084214413693565870053324722538541097621185263193905004485037279370440188956471384192857779904572658394526505476389035293956395324958412403765663938391638294770520304430506699665632229149568805422832023250626982835977575474903710502120532428993
c=163398483907647791039598655705756317031752936018050624450236473504060162084607777116369069421931848265202331732669813345400979732404734476598531344856938766945037703468866753817741896444842889531223798090025143704481916059435190555147529598358490460116483849569080114810635453876931390144214796278106188655537670903781358012716110563059668500938134923781767673216019132510277164344196650888824570942830154506129922673761760829820009335375157863803877854985954687842554686523025455772695619429066976536098919798115179883589238421088157604474180227250103880846243062789859065021982724412620248023084879176809457099659

d, phi, k = attack(
    n = n, 
    e = e,
    r = 5
)

if d:
	m = pow(c, d, n)
	print(long_to_bytes(m))

"""
[+] Computing T
[+] Searching over convergents
[+] D & phi found !
b'ESNA{Cryptanalysis_of_Multi-Prime_RSA_with_Small_Prime_Difference_by_Bahig_Bhery_Nassr}'
"""