Brange = np.linspace(0,0.04,500)
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
        plt.plot(Brange,ls_zeeman(J2/2.,L,S,M2/2.,A,Brange),color="black",linewidth=1.8,linestyle="dashdot")
plt.xlabel(r"$B_{ext}$  (Tesla)",fontsize=20)
plt.ylabel(r"Zeeman Energy (GHz)",fontsize=20)
plt.title(r"${}^2P$    Zeeman Energy",fontsize=20)
plt.xlim(-0.007,0.052)
#plt.ylim(-5,5)
plt.text(-0.004,0.67,r"${}^2P_{3/2}$",fontsize=26)
plt.text(-0.004,-0.83,r"${}^2P_{1/2}$",fontsize=26)
plt.text(0.042,1.6,r"$M_J = +\frac{3}{2}$",fontsize=20)
plt.text(0.042,0.88,r"$M_J = +\frac{1}{2}$",fontsize=20)
plt.text(0.042,0.12,r"$M_J = -\frac{1}{2}$",fontsize=20)
plt.text(0.042,-0.62,r"$M_J = -\frac{3}{2}$",fontsize=20)
plt.text(0.042,-0.88,r"$M_J = +\frac{1}{2}$",fontsize=20)
plt.text(0.042,-1.28,r"$M_J = -\frac{1}{2}$",fontsize=20)
#plt.savefig("2p_zeeman_low.png",bbox_inches="tight")
plt.show()
    
