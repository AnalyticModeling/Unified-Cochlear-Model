from Cochlea import *
from GEFs_core.Signal import Signal

def cochlea_init():
  c = Cochlea(Ap=[0.3768*np.exp(-0.1*i) for i in range(4)], bp=[0.5, 1, 1.5, 2], Bu=[3.714*np.exp(0.03*i) for i in range(4)])
  c.bode_plot(freqs=np.geomspace(0.1, 30, 100000))

def cochlea_at_location():
  c = Cochlea(Ap=[0.3768*np.exp(-0.1*i) for i in range(4)], bp=[0.5, 1, 1.5, 2], Bu=[3.714*np.exp(0.03*i) for i in range(4)])
  fil = c.filter_at_location(0)
  fil.bode_plot()

def cochlea_wavenumber():
  c = Cochlea(Ap=[0.3768*np.exp(-0.1*i) for i in range(4)], bp=[0.5, 1, 1.5, 2], Bu=[3.714*np.exp(0.03*i) for i in range(4)])
  c.plot_wavenumber()

def cochlea_impedance():
  c = Cochlea(Ap=[0.3768*np.exp(-0.1*i) for i in range(4)], bp=[0.5, 1, 1.5, 2], Bu=[3.714*np.exp(0.03*i) for i in range(4)])
  c.plot_impedance()

def cochlea_heatmap():
  c = Cochlea.five_param(type='V', aAp=0.3768, bAp=-0.1366, bp=[1, 1, 1, 1, 1], aBu=3.714, bBu=0.03123, xs=[i for i in range(5)])
  pairs = [(1.5, 200), (8, 400), (1.5, 700), (0.3, 400)]
  def tones(t):
    ans = 0
    for i in range(4):
      fi, ti = pairs[i]
      ans += np.exp(-((t-ti)/50)**2) * np.sin(2*np.pi*fi*t)
    return ans
  # sig = Signal(mode='t', data=[tones(t/100) for t in range(100000)], fs=100)
  # sig = Signal(mode='t', data=[tones(t/10) for t in range(10000)], fs=10)
  sig = Signal(mode='t', data=[tones(t) for t in range(100)], fs=1)
  ans = c.signal_response_heatmap(sig)
  print(ans[0][:100])
  print(len(ans))

if __name__ == "__main__":
   cochlea_init()
   cochlea_at_location()
   cochlea_wavenumber()
   cochlea_impedance()
   cochlea_heatmap()