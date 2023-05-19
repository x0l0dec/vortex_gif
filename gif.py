import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from matplotlib import animation


mn = 10000
k = []; e = []; on = []; xn = []; ox = [[]]; oy = [[]]; xx = [[]]; xy = [[]];
xsize = 1.8e-4; ysize = 5e-4;
my_dpi = 96

f = open('acor.txt')
for line in f:
    k.append(int(line.split(' ')[0]))
    e.append(float(line.split(' ')[2]))

    line = f.readline()
    on.append(len(line.split('o')) - 1)
    xn.append(len(line.split('x')) - 1)
    ox.append([]); oy.append([]); xx.append([]); xy.append([]);
    j = 0
    while j < on[len(on) - 1] + xn[len(xn) - 1]:
        if (line.split(' ')[j][0] == 'o'):
            oy[k[len(k) - 1]].append(float(line.split(';')[j].split('(')[1]) * mn) # x
            ox[k[len(k) - 1]].append(float(line.split(')')[j].split(';')[1]) * mn) # y
        else:
            xy[k[len(k) - 1]].append(float(line.split(';')[j].split('(')[1]) * mn) # x
            xx[k[len(k) - 1]].append(float(line.split(')')[j].split(';')[1]) * mn) # y
        j = j + 1

py = []; px = [];
f = open('prim.txt')
for line in f:
    py.append(float(line.split(';')[0]) * mn)
    px.append(float(line.split(';')[1]) * mn)


fig, ax = plt.subplots()

#ax.set_title('')

def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)

def anime(i):
    print(i)
    ax.clear()
#    line = ax.scatter(x[int(i + k[len(k) - 1] / 2 - 100)],y[int(i + k[len(k) - 1] / 2 - 100)],s=1,color='#1e38eb')
#    ax.scatter(py,px,s=68,color='#505354')
#    ax.scatter(py,px,s=24,color='#ffffff')
    ax.scatter(oy[int(i)],ox[int(i)],s=2,color='#ec0c1c')
    ax.scatter(xy[int(i)],xx[int(i)],s=2,color='#1e38eb')
#    iii = 0
#    while iii < 60:
#        tx = []; ty = []
#        kkk = 0
#        while kkk <= int(i):
#            tx.append(ox[kkk])
#            ty.append(oy[kkk])
#            kkk = kkk + 1
#        ax.plot(tx,ty,color='#0020a0')
#        del tx, ty
#
#        tx = []; ty = []
#        kkk = 0
#        while kkk <= int(i):
#            tx.append(xx[kkk])
#            ty.append(xy[kkk])
#            kkk = kkk + 1
#        ax.plot(tx,ty,color='#a00020')
#        del tx, ty
#
#        iii = iii + 1
    set_size(4,4)
    ax.set_xlim((0,xsize * mn))
    ax.set_ylim((0,ysize * mn))
#    plt.xlabel('шаг = ' + str(k[int(i + k[len(k) - 1] / 2 - 100)]) + '; N = ' + str(n[int(i + k[len(k) - 1] / 2 - 100)]) + ';')
    ax.set_xlabel('шаг = ' + str(k[int(i)]) + '; No = ' + str(on[int(i)]) + '; Nx = ' + str(xn[int(i)]) + '; E = ' + str(e[int(i)]))
#    ax.grid(True)
    return line

print(k[len(k) - 1],' : ',on[len(on) - 1],' : ',xn[len(xn) - 1])

j = 200

ss = 'acor.gif'
ani = animation.FuncAnimation(fig,anime,frames=j,interval=5,repeat=True)
writergif=animation.PillowWriter(fps = 10)
writergif.setup(fig, "2D_Schrodinger_Equation.gif", dpi = 300) 
ani.save(ss,writer=writergif,dpi=my_dpi * 4)
plt.clf()

exit(0)


# speed 2
del k, e, on, xn, ox, oy, xx, xy
k = []; e = []; on = []
f = open('speed.txt')
for line in f:
    k.append(float(line.split(':')[0]) * mn)
    e.append(float(line.split(':')[1]) * mn)
    on.append(float(line.split(':')[2]) * mn)
f.close()


fig, ax = plt.subplots(figsize=(800/my_dpi, 500/my_dpi), dpi=my_dpi)

plt.scatter(k, e, s=1, color='#ec0c1c')
plt.xlabel('r, мкм', style='italic')
plt.ylabel('U, мкм/шаг', style='italic')
plt.savefig("speed.png", dpi=my_dpi * 4)
plt.clf()


fig, ax = plt.subplots(figsize=(800/my_dpi, 500/my_dpi), dpi=my_dpi)

plt.scatter(k, on, s=1, color='#b2b2b2')

z = np.polyfit(k, on, 1)
p = np.poly1d(z)
plt.plot(k, p(k), color='#ec0c1c')

plt.xlabel('r, мкм', style='italic')
plt.ylabel('$U_п$, мкм', style='italic')
plt.savefig("speed2.png", dpi=my_dpi * 4)
plt.clf()


step = 0.01
spd = []; nr = []
i1 = 0; i2 = step;
while i1 <= max(k):
    print(i1,i2)
    spd.append(0)
    nr.append(i1 + (i2 - i1) / 2)
    j = 0; jj = 0
    for i in k:
        if (i >= i1) and (i < i2):
            spd[-1] = spd[-1] + e[j]
            jj = jj + 1
        j = j + 1
    if (jj > 0):
        spd[-1] = spd[-1] / jj
    i1 = i2;
    i2 = i2 + step;

fig, ax = plt.subplots(figsize=(800/my_dpi, 500/my_dpi), dpi=my_dpi)

plt.scatter(nr, spd, s=1, color='#b2b2b2')

z = np.polyfit(nr, spd, 1)
p = np.poly1d(z)
plt.plot(nr, p(nr), color='#ec0c1c')

plt.xlabel('r, мкм', style='italic')
plt.ylabel('$U_ср$, мкм/шаг', style='italic')
plt.savefig("speed3.png", dpi=my_dpi * 4)
plt.clf()


del spd, nr
spd = []; nr = []
i1 = 0; i2 = step;
while i1 <= max(k):
    print(i1,i2)
    spd.append(0)
    nr.append(i1 + (i2 - i1) / 2)
    j = 0; jj = 0
    for i in k:
        if (i >= i1) and (i < i2):
            spd[-1] = spd[-1] + on[j]
            jj = jj + 1
        j = j + 1
    if (jj > 0):
        spd[-1] = spd[-1] / jj
    i1 = i2;
    i2 = i2 + step;

fig, ax = plt.subplots(figsize=(800/my_dpi, 500/my_dpi), dpi=my_dpi)

plt.scatter(nr, spd, s=1, color='#b2b2b2')

z = np.polyfit(nr, spd, 1)
p = np.poly1d(z)
plt.plot(nr, p(nr), color='#ec0c1c')

plt.xlabel('r, мкм', style='italic')
plt.ylabel('$U_{п-ср}$, мкм', style='italic')
plt.savefig("speed4.png", dpi=my_dpi * 4)
plt.clf()

exit(0)



# speed
def trans(m):
    n = [[]]
    m.pop(0)
    row = len(m)
    col = len(m[0])

 
    for i in range(col):
        n.append([])
        for j in range(row):
            n[i].append(float(m[j][i]))

    return n

del k, e, on, xn, ox, oy, xx, xy
x = [[]]; y = [[]]; t = [[]]; r = []
f = open('speed.txt')
for line in f:
    r.append(int(line.split(' ')[0]))

    line = f.readline()
    j = 0
    t.append([]); x.append([]); y.append([])
    while j < 60:
        t[r[len(r) - 1]].append(float(line.split(' ')[j].split('(')[0]) * mn)
        x[r[len(r) - 1]].append(float(line.split(';')[j].split('(')[1]) * mn)
        y[r[len(r) - 1]].append(float(line.split(')')[j].split(';')[1]) * mn)
        j = j + 1

tt = trans(t)
xx = trans(x)
yy = trans(y)

fig, ax = plt.subplots(figsize=(800/my_dpi, 500/my_dpi), dpi=my_dpi)

palette = sb.color_palette(n_colors = 3)
i = 0
j = 0
while j < 60:
    plt.plot(r, tt[j], color=palette[i])
    j = j + 20
    i = i + 1
plt.xlabel('k, шаг', style='italic')
plt.ylabel('U, мкм/шаг', style='italic')
plt.savefig("speed.png", dpi=my_dpi * 4)
plt.clf()
f.close()

fig, ax = plt.subplots(figsize=(800/my_dpi, 500/my_dpi), dpi=my_dpi)

palette = sb.color_palette(n_colors = 6)
i = 0
j = 0
while j < 60:
    plt.plot(r, xx[j], color=palette[i])
    j = j + 10
    i = i + 1
plt.xlabel('k, шаг', style='italic')
plt.ylabel('U, мкм/шаг', style='italic')
plt.savefig("speed_x.png", dpi=my_dpi * 4)
plt.clf()

fig, ax = plt.subplots(figsize=(800/my_dpi, 500/my_dpi), dpi=my_dpi)

palette = sb.color_palette(n_colors = 6)
i = 0
j = 0
while j < 60:
    plt.plot(r, yy[j], color=palette[i])
    j = j + 10
    i = i + 1
plt.xlabel('k, шаг', style='italic')
plt.ylabel('U, мкм/шаг', style='italic')
plt.savefig("speed_y.png", dpi=my_dpi * 4)
plt.clf()
