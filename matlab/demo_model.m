initialRun

function res = cochlea_init()
    c = Cochlea(Ap=0.3768*exp(-0.1*(0:3)), bp=[0.5, 1, 1.5, 2], Bu=3.714*exp(0.03*(0:3)));
    res = c.bode_plot();
end

function res = cochlea_at_location()
    c = Cochlea(Ap=0.3768*exp(-0.1*(0:3)), bp=[0.5, 1, 1.5, 2], Bu=3.714*exp(0.03*(0:3)));
    fil = c.filter_at_location(0);
    res = fil.bode_plot();
end

function res = cochlea_wavenumber()
    c = Cochlea(Ap=0.3768*exp(-0.1*(0:3)), bp=[0.5, 1, 1.5, 2], Bu=3.714*exp(0.03*(0:3)));
    res = c.plot_wavenumber();
end

function res = cochlea_impedance()
    c = Cochlea(Ap=0.3768*exp(-0.1*(0:3)), bp=[0.5, 1, 1.5, 2], Bu=3.714*exp(0.03*(0:3)));
    res = c.plot_impedance();
end

function res = cochlea_heatmap()
    c = Cochlea(type='V', aAp=0.3768, bAp=-0.1366, bp=[1, 1, 1, 1, 1], aBu=3.714, bBu=0.03123, xs=[0, 1, 2, 3, 4]);
    function innerres = tones(t)
        innerres = 0;
        fis = [1.5, 8, 1.5, 3];
        tis = [200, 400, 700, 400];
        for idx = 1:4
            innerres = innerres + (exp(-((t-tis(idx))/50).^2) .* sin(2*pi*fis(idx)*t));
        end
    end
    sample_rate = 1;
    % endtime = 1000*sample_rate;
    endtime = 100;
    timestamps = 0:(endtime-1);
    sig = Signal(mode='t', data=timestamps./sample_rate, fs=sample_rate);
    res = c.signal_response_heatmap(sig);
    % res{0}
end

%
% def cochlea_heatmap():
%   c = Cochlea.five_param(type='V', aAp=0.3768, bAp=-0.1366, bp=[1, 1, 1, 1, 1], aBu=3.714, bBu=0.03123, xs=[i for i in range(5)])
%   pairs = [(1.5, 200), (8, 400), (1.5, 700), (0.3, 400)]
%   def tones(t):
%     ans = 0
%     for i in range(4):
%       fi, ti = pairs[i]
%       ans += np.exp(-((t-ti)/50)**2) * np.sin(2*np.pi*fi*t)
%     return ans
%   sig = Signal(mode='t', data=[tones(t/100) for t in range(100000)], fs=100)
%   c.signal_response_heatmap(sig)

  cochlea_init()
% cochlea_at_location()
% cochlea_wavenumber()
% cochlea_impedance()
% cochlea_heatmap()