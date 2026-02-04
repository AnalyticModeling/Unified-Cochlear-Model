from GEFs_core.Filter import *
from GEFs_core.FilterBank import *
from GEFs_core.Signal import *
from Cochlea import *
import matplotlib.pyplot as plt
import helpers

### for auditory physicists

def fig3_2019():
  c = Cochlea(Ap=[0.05], bp=[1], Bu=[1.3])
  betas, reals, imags, magns, phases = c.plot_wavenumber(betas=np.geomspace(0.7, 1.2, 10000), show=False)
  fig, (ax1, ax2) = plt.subplots(2, 1)

  ax1.semilogx(betas, reals, ls='--')
  ax1.xaxis.set_major_locator(locator=matplotlib.ticker.LogLocator(subs=(0.7, 1, 1.2)))
  ax1.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
  ax1.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
  ax1.set_ylabel(r'Re{k} (mm$^{-1}$)')
  ax1.axhline(y=0, color='k', ls=':')
  ax1.axvline(x=1, color='k', ls=':')

  ax2.semilogx(betas, imags, ls='--')
  ax2.xaxis.set_major_locator(locator=matplotlib.ticker.LogLocator(subs=(0.7, 1, 1.2)))
  ax2.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
  ax2.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
  ax2.set_ylabel(r'Im{k} (mm$^{-1}$)')
  ax2.axhline(y=0, color='k', ls=':')
  ax2.axvline(x=1, color='k', ls=':')
  ax2.set_xlabel('β')

  fig.suptitle('Wavenumber (k) of model')
  plt.show()

def fig6_2019():
  c = Cochlea.five_param(type='V', aAp=0.3768, bAp=-0.1366, bp=1, aBu=3.714, bBu=0.03123, cfs=[0.2, 0.5, 2, 5, 15])

  fils = c.bode_plot(freqs=np.geomspace(0.1, 30, 100000), show=False)

  fig, (ax1, ax2) = plt.subplots(2, 1)
  fig.suptitle('Q and N of velocities of a cochlea')

  for i in range(5):
    fil = fils[i]
    chars = c.filters[i].get_computed_chars()
    # print(chars)
    xaxis, magn, phase, uid = fil
    ax1.semilogx(xaxis, magn, label=f'Q={round(chars["Qerb"], 2)}') # magn in db
    # ax2.semilogx(xaxis, phase, label=f'N={round(chars["Nbeta"], 2)}') # phase in cycles
    ax2.semilogx(xaxis, phase, label=f'N={round(chars["Nbeta"], 2)}') # phase in cycles
  ax1.xaxis.set_major_locator(locator=matplotlib.ticker.LogLocator(subs=(1, 2, 5)))
  ax1.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
  ax1.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
  ax1.set_ylabel('Magnitude (dB)')
  ax1.legend()

  ax2.set_ylabel('Phase (cycles)')
  ax2.set_xlabel('Frequency (kHz)')
  ax2.legend()

  plt.show()

def fig8_2019():
  c = Cochlea.five_param(type='V', aAp=0.3768, bAp=-0.1366, bp=[1, 1, 1, 1, 1], aBu=3.714, bBu=0.03123, xs=[i for i in range(5)])
  pairs = [(1.5, 200), (8, 400), (1.5, 700), (0.3, 400)]
  def tones(t):
    ans = 0
    for i in range(4):
      fi, ti = pairs[i]
      ans += np.exp(-((t-ti)/50)**2) * np.sin(2*np.pi*fi*t)
    return ans
  sig = Signal(mode='t', data=[tones(t/100) for t in range(100000)], fs=100)
  c.signal_response_heatmap(sig, len_xs=50)

def fig2_2022():
  fig, axs = plt.subplots(2, 2, constrained_layout=True)

  c1 = Cochlea(Ap=[0.11], bp=[1], Bu=[7], CF0=1)
  betas1, reals1, imags1, magns1, phases1 = c1.plot_wavenumber(betas=np.geomspace(0.5, 2, 10000), show=False)
  c2 = Cochlea(Ap=[0.055], bp=[1], Bu=[7], CF0=10)
  betas2, reals2, imags2, magns2, phases2 = c2.plot_wavenumber(betas=np.geomspace(0.5, 2, 10000), show=False)
  axs[0][0].semilogx(betas1, reals1, label='Human Apex')
  axs[0][0].semilogx(betas2, reals2, ls='--', label='Human Base')
  axs[0][0].xaxis.set_major_locator(locator=matplotlib.ticker.LogLocator(subs=(0.5, 1, 2)))
  axs[0][0].xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
  axs[0][0].xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
  axs[0][0].set_ylabel(r'Re{k} (mm$^{-1}$)')
  axs[0][0].axhline(y=0, color='k', ls=':')
  axs[0][0].axvline(x=1, color='k', ls=':')
  axs[0][0].legend()

  axs[0][1].semilogx(betas1, imags1)
  axs[0][1].semilogx(betas2, imags2, ls='--')
  axs[0][1].xaxis.set_major_locator(locator=matplotlib.ticker.LogLocator(subs=(0.5, 1, 2)))
  axs[0][1].xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
  axs[0][1].xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
  axs[0][1].set_ylabel(r'Im{k} (mm$^{-1}$)')
  axs[0][1].axhline(y=0, color='k', ls=':')
  axs[0][1].axvline(x=1, color='k', ls=':')

  c1 = Cochlea(Ap=[0.11], bp=[1], Bu=[7], CF0=1)
  betas1, reals1, imags1, magns1, phases1 = c1.plot_impedance(betas=np.geomspace(0.5, 2, 10000), show=False)
  c2 = Cochlea(Ap=[0.055], bp=[1], Bu=[7], CF0=10)
  betas2, reals2, imags2, magns2, phases2 = c2.plot_impedance(betas=np.geomspace(0.5, 2, 10000), show=False)
  axs[1][0].semilogx(betas1, reals1)
  axs[1][0].semilogx(betas2, reals2, ls='--')
  axs[1][0].xaxis.set_major_locator(locator=matplotlib.ticker.LogLocator(subs=(0.5, 1, 2)))
  axs[1][0].xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
  axs[1][0].xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
  axs[1][0].set_ylabel(r'Re{Z}/(2$\pi\rho$l)')
  axs[1][0].axhline(y=0, color='k', ls=':')
  axs[1][0].axvline(x=1, color='k', ls=':')
  axs[1][0].set_xlabel(r'$\beta$')

  axs[1][1].semilogx(betas1, imags1)
  axs[1][1].semilogx(betas2, imags2, ls='--')
  axs[1][1].xaxis.set_major_locator(locator=matplotlib.ticker.LogLocator(subs=(0.5, 1, 2)))
  axs[1][1].xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
  axs[1][1].xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
  axs[1][1].set_ylabel(r'Im{Z}/(2$\pi\rho$l)')
  axs[1][1].axhline(y=0, color='k', ls=':')
  axs[1][1].axvline(x=1, color='k', ls=':')
  axs[1][1].set_xlabel(r'$\beta$')

  fig.suptitle('Estimated wavenumbers and impedances in human cochlea')
  plt.show()

if __name__ == "__main__":
    fig3_2019()
    fig6_2019()
    fig8_2019()
    fig2_2022()

  # example for all four plots for cochlea