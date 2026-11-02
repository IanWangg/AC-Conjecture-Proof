"""Exact free-word/Tietze checks for the three remaining power9 branches."""
import argparse
import json
from pathlib import Path


def inverse(w):return w.swapcase()[::-1]


def reduce(w):
    out=[]
    for c in w:
        if out and out[-1]==c.swapcase():out.pop()
        else:out.append(c)
    return ''.join(out)


def substitute(w,images):
    table=dict(images);table.update({c.upper():inverse(v) for c,v in images.items()})
    return reduce(''.join(table[c] for c in w))


def power(w,n):return reduce((w if n>=0 else inverse(w))*abs(n))


def endomorphism(w,images,n=1,back=None):
    if n<0:
        assert back is not None
        return endomorphism(w,back,-n)
    for _ in range(n):w=substitute(w,images)
    return w


def magnus(w,alpha,back=None):
    """Read a word in fiber letters and t into fiber-word times t^height."""
    value='';height=0
    for c in w:
        if c in 'tT':height+=1 if c=='t' else -1
        else:value=reduce(value+endomorphism(c,alpha,height,back))
    return value,height


def checks():
    rD='XXXyxYXyy';rE='XXYxxYYxy';rF='XXyXYxYxy';braid='xyxYXY'
    phiD={'a':'b','b':'AbAb'}
    alphaE={'a':'b','b':'c','c':'Bacc'}
    backE={'a':'acBB','b':'a','c':'b'}
    alphaF={'a':'b','b':'aB'}
    backF={'a':'ba','b':'a'}
    for images,back in ((alphaE,backE),(alphaF,backF)):
        for c in images:
            assert substitute(substitute(c,images),back)==c
            assert substitute(substitute(c,back),images)==c

    # D: a=x(xY)^2, t=yX; the inverse free basis is x=a t²,y=t a t².
    d_images={'x':'att','y':'tatt'}
    d_back={'a':'xxYxY','t':'yX'}
    for c in 'xy':assert substitute(substitute(c,d_images),d_back)==c
    for c in 'at':assert substitute(substitute(c,d_back),d_images)==c
    a2='ttaTT';b='taT'
    relationD=reduce(inverse(a2)+'A'+b+'A'+b)
    conjugatorD='TTATTTT'
    literalD=substitute(rD,d_images)
    assert literalD==reduce(conjugatorD+relationD+inverse(conjugatorD))
    assert magnus(substitute(inverse(braid),d_images),phiD)==('baBabAbA',1)

    # E: a=xY²,t=y.  t^5 rE t^-5 is exactly a3^-1 a1^-1 a0 a2².
    e_images={'x':'att','y':'t'};e_back={'a':'xYY','t':'y'}
    for c in 'xy':assert substitute(substitute(c,e_images),e_back)==c
    for c in 'at':assert substitute(substitute(c,e_back),e_images)==c
    a1='taT';a2='ttaTT';a3='tttaTTT'
    relationE=reduce(inverse(a3)+inverse(a1)+'a'+a2+a2)
    assert reduce('ttttt'+substitute(rE,e_images)+'TTTTT')==relationE
    assert magnus(substitute(rE,e_images),alphaE,backE)==('',0)
    assert magnus(substitute(braid,e_images),alphaE,backE)==('aBac',1)

    # F: x=b,y=b t, with a=Yxy,b=x,t=Xy.  The t a t^-1=b
    # relation is already a free identity in the original x,y words.
    f_back={'a':'Yxy','b':'x','t':'Xy'}
    assert substitute('taTB',f_back)==''
    relationF=substitute('tbTbA',f_back)
    assert reduce(inverse(f_back['a'])+inverse(relationF)+f_back['a'])==rF
    f_images={'x':'b','y':'bt'}
    assert magnus(substitute(rF,f_images),alphaF,backF)==('',0)
    W,height=magnus(substitute(inverse(braid),f_images),alphaF,backF)
    assert (W,height)==('baBaBaBAbA',1)
    conjugator='BAbbbABB'
    assert reduce(conjugator+W+inverse(substitute(conjugator,alphaF)))=='BAbb'
    # Candidate b^k t is conjugate to a^k t by t, since alphaF(a)=b.
    assert substitute('a',alphaF)=='b'

    characters={'D':(2,3),'E':(2,1),'F':(0,1)}
    for name,r in (('D',rD),('E',rE),('F',rF)):
        u,v=characters[name]
        chi=lambda w:u*(w.count('x')-w.count('X'))+v*(w.count('y')-w.count('Y'))
        assert chi(r)==0
        assert chi(braid if name=='E' else inverse(braid))==1
    return dict(status='PASS',ordinary_AC_goal_solved=False,
                original_relators={'D':rD,'E':rE,'F':rF},
                D_free_basis=d_back,D_inverse_basis=d_images,
                D_relation_conjugator=conjugatorD,D_relation_in_a_t=relationD,
                D_endomorphism=phiD,D_braid_inverse_coefficient='baBabAbA',
                E_free_basis=e_back,E_inverse_basis=e_images,E_relation_in_a_t=relationE,
                E_alpha=alphaE,E_alpha_inverse=backE,E_braid_coefficient='aBac',
                F_generators_in_original_words=f_back,F_alpha=alphaF,F_alpha_inverse=backF,
                F_braid_inverse_coefficient=W,F_transfer_conjugator=conjugator,
                F_transferred_coefficient='BAbb',primitive_character_vectors=characters)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    result=checks()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
