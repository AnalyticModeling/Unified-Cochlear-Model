import pytest
import numpy as np
from GEFs_core.Filter import Filter
from GEFs_core.Signal import Signal
from python.Cochlea import Cochlea

#======================
# Cochleas Fixture
#======================
# (can be extended to include more cochleas)
@pytest.fixture
def sample_cochleas():
    """Fixture to create four Cochlea objects: custom (xs), custom (cfs), five_param, and species."""
    custom_cochlea_xs = Cochlea(CF0=30, l_factor=5, length=25, xs=[0, 10, 20], Ap=[0.1, 0.2, 0.3], bp=1, Bu=[2, 3, 4])
    custom_cochlea_cfs = Cochlea(CF0=30, l_factor=5, length=25, cfs=[10, 5, 2], Ap=[0.1, 0.2, 0.3], bp=1, Bu=[2, 3, 4])
    five_param_cochlea = Cochlea.five_param(aAp=0.5, bAp=-0.1, bp=[1, 1, 1, 1], aBu=4, bBu=0.05)
    species_cochlea = Cochlea(species='human')
    return {
        'custom_xs': custom_cochlea_xs,
        'custom_cfs': custom_cochlea_cfs,
        'five_param': five_param_cochlea,
        'species': species_cochlea,
    }

#======================
# Signal Fixture
#======================
# (can be extended to include more signals)
@pytest.fixture
def sample_signal():
    """Fixture to create a sample Signal object."""
    fs = 1000
    t = np.linspace(0, 1, fs, endpoint=False)
    data = np.sin(2 * np.pi * 10 * t)
    return Signal(data=data, fs=fs)

#======================
# Core Tests
#======================

# Test 1 - passed
def test_cochlea_length_and_filters(sample_cochleas):
    """Test cochlea_length and number of filters for each Cochlea type."""
    for name, cochlea in sample_cochleas.items():
        if name in ['custom_xs', 'custom_cfs']:
            assert cochlea.cochlea_length == 25
            assert len(cochlea.filters) == 3
        elif name == 'five_param':
            assert len(cochlea.filters) == 4
        elif name == 'species':
            assert cochlea.cochlea_length == 35
        else:
            raise ValueError(f"Unexpected Cochlea type: {name}")

# Test 2 - failed ( leaks a lot of system info need exception handling)
def test_empty_cochlea():
    """Test making empty cochlea object."""
    cochlea = Cochlea()

# Test 3 - passed
def test_cochlea_initialization_cfs_and_xs_error():
    """Test Cochlea initialization with both cfs and xs."""
    with pytest.raises(Exception, match='Please provide exactly one of either a list of all locations along cochlea \(xs\) or a list of all characteristic frequencies \(cfs\)'):
        Cochlea(cfs=[10, 5], xs=[1, 2])

# Test 4 - passed
def test_five_param_init():
    """Test Cochlea initialization with five_param, including parameter calculation."""
    aAp = 0.1
    bAp = -0.01
    bp = 1
    aBu = 3
    bBu = 0.01
    length = 20  # example length
    cfs = [10, 5, 2]  # example cfs
    xs = [-np.log(cf / 20) * 3.8 for cf in cfs]  # calculate xs for given cfs

    cochlea_five_cfs = Cochlea.five_param(aAp=aAp, bAp=bAp, bp=bp, aBu=aBu, bBu=bBu, length=length, cfs=cfs)

    assert isinstance(cochlea_five_cfs, Cochlea)
    assert callable(cochlea_five_cfs.Ap_fun)
    assert callable(cochlea_five_cfs.Bu_fun)
    assert len(cochlea_five_cfs.filters) == len(cfs)

    # Check if Ap and Bu parameters are calculated correctly
    for i, cf in enumerate(cfs):
        expected_Ap = aAp * np.exp(bAp * cf)
        expected_Bu = aBu * np.exp(bBu * cf)

        assert np.isclose(cochlea_five_cfs.filters[i].get_params()['Ap'], expected_Ap, atol=1e-6)
        assert np.isclose(cochlea_five_cfs.filters[i].get_params()['Bu'], expected_Bu, atol=1e-6)

    # test with xs input.
    cochlea_five_xs = Cochlea.five_param(aAp=aAp, bAp=bAp, bp=bp, aBu=aBu, bBu=bBu, length=length, xs=xs)

    assert isinstance(cochlea_five_xs, Cochlea)
    assert callable(cochlea_five_xs.Ap_fun)
    assert callable(cochlea_five_xs.Bu_fun)
    assert len(cochlea_five_xs.filters) == len(xs)

    # Check if Ap and Bu parameters are calculated correctly
    for i, x in enumerate(xs):
        cf = 20 * np.exp(-x / 3.8)  # calculate cf from x
        expected_Ap = aAp * np.exp(bAp * cf)
        expected_Bu = aBu * np.exp(bBu * cf)

        assert np.isclose(cochlea_five_xs.filters[i].get_params()['Ap'], expected_Ap, atol=1e-6)
        assert np.isclose(cochlea_five_xs.filters[i].get_params()['Bu'], expected_Bu, atol=1e-6)

# Test 5 - passed
def test_given_species_invalid():
    """Test _given_species method with invalid species."""
    with pytest.raises(Exception, match='"invalid_species" is an unsupported species'):
        cochlea = Cochlea('invalid_species')

# Test 6 - failed ( only species cochlea cause error with filter_at_location function)
def test_filter_at_location(sample_cochleas):
    """Test filter_at_location method for each Cochlea type."""
    for name, cochlea in sample_cochleas.items():
        if name in ['custom_xs', 'custom_cfs','five_param']: # passed
            filter_at_5 = cochlea.filter_at_location(5)
            assert isinstance(filter_at_5, Filter)
            assert np.isclose(filter_at_5.cf, cochlea.cf(5), atol=1e-5)
        elif name == 'species': # cause error
            filter_at_5 = cochlea.filter_at_location(5)
            assert isinstance(filter_at_5, Filter)
            assert np.isclose(filter_at_5.cf, cochlea.cf(5), atol=1e-5)

# Test 7 - passed
def test_cochlea_process_signal_output_type(sample_cochleas, sample_signal):
    """Test if output signals are of type Signal for each Cochlea type."""
    for name, cochlea in sample_cochleas.items():
        output_signals = cochlea.process_signal(sample_signal)
        for signal in output_signals.outsignals:
            assert isinstance(signal, Signal)
            assert len(signal) == len(sample_signal)

# Test 8 - passed
def test_plot_wavenumber(sample_cochleas):
    """ test that the `plot_wavenumber` method returns five NumPy arrays [betas, reals, imags, magns, phases] for each cochlea model """

    for name, cochlea in sample_cochleas.items():
        betas, reals, imags, magns, phases = cochlea.plot_wavenumber(show=False)
        assert isinstance(betas, np.ndarray)
        assert isinstance(reals, np.ndarray)
        assert isinstance(imags, np.ndarray)
        assert isinstance(magns, np.ndarray)
        assert isinstance(phases, np.ndarray)
        results = cochlea.plot_wavenumber(show=False)
        assert len(results) == 5  # [betas, reals, imags, magns, phases]

# Test 9 - passed
def test_plot_impedance(sample_cochleas):
    """ test that the `plot_impedance` method returns five NumPy arrays [betas, reals, imags, magns, phases] for each cochlea model """

    for name, cochlea in sample_cochleas.items():
        betas, reals, imags, magns, phases = cochlea.plot_impedance(show=False)
        assert isinstance(betas, np.ndarray)
        assert isinstance(reals, np.ndarray)
        assert isinstance(imags, np.ndarray)
        assert isinstance(magns, np.ndarray)
        assert isinstance(phases, np.ndarray)
        results = cochlea.plot_impedance(show=False)
        assert len(results) == 5  # [betas, reals, imags, magns, phases]

# Test 10 - 3 passed, 1 failed ( only species cochlea cause error because it needs the value of x_coord )
def test_signal_response_heatmap_output_type(sample_cochleas, sample_signal):
    """Test if signal_response_heatmap returns a list of NumPy arrays."""
    for name, cochlea in sample_cochleas.items():
        if name in ['custom_xs', 'custom_cfs', 'five_param']:
            sigs = cochlea.signal_response_heatmap(sample_signal, len_xs=10, show=False)
            assert isinstance(sigs, list)
            assert len(sigs) == 10  # len_xs
            for sig in sigs:
                assert len(sig) == len(sample_signal)

        elif name == 'species': # failed, it raise an error because it need the value of x_coord
            sigs = cochlea.signal_response_heatmap(sample_signal, len_xs=10, show=False)
            assert isinstance(sigs, list)
            for sig in sigs:
                assert len(sig) == len(sample_signal)


# Test 11 - 3 passed, 1 failed ( only species cochlea cause error because it need the value of x_coord )
def test_signal_response_heatmap_output_shape(sample_cochleas, sample_signal):
    """Test if signal_response_heatmap returns a list of correct shape."""
    for name, cochlea in sample_cochleas.items():
        if name in ['custom_xs', 'custom_cfs','five_param']: # passed
            sigs = cochlea.signal_response_heatmap(sample_signal, len_xs=10)
            assert isinstance(sigs, list)
            assert len(sigs) == 10  # len_xs
            for sig in sigs:
                assert len(sig) == len(sample_signal)

        elif name == 'species': # failed, it raise an error because it need the value of x_coord
            sigs = cochlea.signal_response_heatmap(sample_signal, len_xs=10)
            assert isinstance(sigs, list)
            assert len(sigs) == 10  # len_xs
            for sig in sigs:
                assert len(sig) == len(sample_signal)