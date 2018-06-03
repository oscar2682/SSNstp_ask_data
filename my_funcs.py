def ask_user_time(datetime):
    import os
    from sys import exit
    global datefile
    if not datetime:
       print("[WARNING] Date string is empty")
       exit()
    y  = datetime.split(",")[0].split("/")[0]
    if (int(y) <= 1979) or (int(y) >= 2100):
       print("[WARNING] Year format is wrong")
       exit()
    mo = datetime.split(",")[0].split("/")[1]
    if (int(mo) < 1) or (int(mo) >= 12):
       print("[WARNING] Month format is wrong")
       exit()
    d  = datetime.split(",")[0].split("/")[2]
    h  = "%02d" % int(datetime.split(",")[1].split(":")[0])
    if (int(h) < 0) or (int(h) > 23):
       print("[WARNING] Hour format is wrong")
       exit()
    mi = datetime.split(",")[1].split(":")[1]
    if (int(mi) < 0) or (int(mi) > 59.99):
       print("[WARNING] Minute format is wrong")
       exit()
    s  = datetime.split(",")[1].split(":")[2]
    if (int(s) < 0) or (int(s) > 59.99):
       print("[WARNING] Second format is wrong")
       exit()
#    print "%s/%s/%s,%s:%s:%s +5m\n" % (y,mo,d,h,mi,s)
    f = open('ssnstp.input','w')
    f.write('WIN IG PP HHZ %s/%s/%s,%s:%s:%s +5m\n' % (y,mo,d,h,mi,s))
    f.write('exit\n')
    f.close()
    os.system("SSNstp < ssnstp.input")
    os.system("rm -f ssnstp.input")
    datfile="%s%s%s%s%s%s.IG.PPIG.HHZ.sac" % (y,mo,d,h,mi,s)
    return datfile

def filter_one(filename,fmin=0.03, fmax=0.1):
    from obspy import read
    from numpy import absolute,log,linspace
    import matplotlib.pyplot as plt
    plt.style.use('bmh')
    st = read(filename)
    tr = st.copy()
    pre_filt = (0.005, 0.006, 30.0, 35.0)
    t1 = tr[0].stats.starttime
    seedresp = {'filename': "PPIG.RESP", 'date': t1, 'units': 'VEL'}
    tr[0].simulate(paz_remove=None, pre_filt=pre_filt, seedresp=seedresp)
    tr[0].filter("bandpass",freqmin=fmin, freqmax=fmax)
    tr.write(filename+".pz",format='SAC')
    amp=absolute(max(tr[0].data)) + absolute(min(tr[0].data))*1e4
    mag = log(amp)+6.08
    npts = tr[0].stats.sac.npts
    delta = tr[0].stats.sac.delta
    t = linspace(0,npts*delta+1,npts)
    plt.clf()
    plt.text(250,amp*0.75,"M${}_{k}$= %4.2f" % mag,
      bbox={'facecolor':'red', 'alpha':0.5, 'pad':10}, fontsize=15)
    plt.plot(t,tr[0].data*1e4)
    plt.title("PPIG-BHZ\nFiltro: 0.03-0.1 Hz\n%s"%t1)
    plt.xlabel("Tiempo, s")
    plt.ylabel("Amplitud, cm/s")
    plt.tight_layout()

