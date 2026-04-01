#!/usr/bin/env python3
import math
G=6.6743e-11;M=5.972e24;R=6371e3

c=lambda r:math.sqrt(G*M/r)

e=lambda r,a:math.sqrt(G*M*(2/r-1/a))

h=lambda r1,r2:({'dv1':e(r1,(r1+r2)/2)-c(r1),'dv2':c(r2)-e(r2,(r1+r2)/2),
                 'dv_total':None,'t':None})

def h(r1,r2):
    a=(r1+r2)/2; dv1=e(r1,a)-c(r1); dv2=c(r2)-e(r2,a);
    return {'dv1':dv1,'dv2':dv2,'dv_total':dv1+dv2,'t':math.pi*math.sqrt(a**3/(G*M))}

def rk4(s,dt):
    def acc(x,y): r=math.hypot(x,y); f=-G*M/r**3; return f*x,f*y
    def f(u):a0,a1=acc(u[0],u[1]); return [u[2],u[3],a0,a1]
    k1=f(s);k2=f([s[i]+.5*dt*k1[i] for i in range(4)]);k3=f([s[i]+.5*dt*k2[i] for i in range(4)]);k4=f([s[i]+dt*k3[i] for i in range(4)]);
    return [s[i]+dt*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6 for i in range(4)]

def sim(r1,r2,dt=10):
    p=h(r1,r2); s=[r1,0,0,c(r1)+p['dv1']]; t=0
    while t<p['t']: s=rk4(s,dt); t+=dt
    r=math.hypot(s[0],s[1]); v_geo=c(r2); rad=[s[0]/r,s[1]/r]; tan=[-rad[1],rad[0]]
    cur=s[2]*tan[0]+s[3]*tan[1]; dv2=v_geo-cur; s[2]+=dv2*tan[0]; s[3]+=dv2*tan[1]
    return {**p,'r_final':r,'v_final':math.hypot(s[2],s[3]),'dv2_applied':dv2}

def t(m,d,i=450): g0=9.80665; mf=m*math.exp(-d/(i*g0)); return mf,m-mf

if __name__=='__main__':
    r1=R+500e3; r2=R+35786e3; p=h(r1,r2); mf,f=t(2000,p['dv_total']); s=sim(r1,r2)
    print(f"ΔV1={p['dv1']:.1f} ΔV2={p['dv2']:.1f} tot={p['dv_total']:.1f} m/s, t={p['t']/3600:.1f}h, f={f:.1f}kg, r={s['r_final']/1000:.1f}km, v={s['v_final']/1000:.3f}km/s")

