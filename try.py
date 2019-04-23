Brange = np.linspace(0,0.4,500)
S=0.5
L=1.0
A=1
nevals = irnd((2*S+1)*(2*L+1))
yy = np.zeros((len(Brange),nevals))
plt.figure(figsize=(12,8))
for i in range(len(Brange)):
    temp = get_sorted(L,S,A,Brange[i])
    for ev in range(nevals):
        yy[i,ev] = temp[ev]
for ev in range(nevals):
    plt.plot(Brange,yy[:,ev],linewidth=3)
for J2 in range(irnd(abs(2.*(L-S))),irnd(2.*(L+S)+1),2):
    plt.hlines(zfs(J2/2.,L,S,A),-max(Brange)/20,max(Brange)/20,linestyle="dotted",linewidth=2)
    for M2 in range(-J2,J2+1,2):
        plt.plot(Brange,ls_zeeman(J2/2.,L,S,M2/2.,A,Brange),color="black",linewidth=0.8,linestyle="dashdot")
plt.xlabel(r"$B_{ext}$  (Tesla)",fontsize=20)
plt.ylabel(r"Zeeman Energy (GHz)",fontsize=20)
plt.title(r"${}^2P$    Zeeman Energy",fontsize=20)
plt.xlim(-0.07,0.58)
#plt.ylim(-5,5)
plt.text(-0.06,0.87,r"${}^2P_{3/2}$",fontsize=24)
plt.text(-0.06,-1.83,r"${}^2P_{1/2}$",fontsize=24)
plt.text(0.405,11.5,r"$M_L = +1\;M_S=+\frac{1}{2}$",fontsize=20)
plt.text(0.405,5.5,r"$M_L = \;\;\; 0\;\;M_S=+\frac{1}{2}$",fontsize=20)
plt.text(0.405,-0.05,r"$M_L =  -1\;M_S=+\frac{1}{2}$",fontsize=20)
plt.text(0.405,-1.55,r"$M_L =  +1\;M_S=-\frac{1}{2}$",fontsize=20)
plt.text(0.405,-6.2,r"$M_L = \;\;\; 0\;\;M_S=-\frac{1}{2}$",fontsize=20)
plt.text(0.405,-11.1,r"$M_L = -1\;M_S=-\frac{1}{2}$",fontsize=20)
#plt.savefig("2p_zeeman_high.png",bbox_inches="tight")
plt.show()
    
