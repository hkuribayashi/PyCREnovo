from enum import Enum


class Network(Enum):

    DEFAULT = (1000000.0, 20.0, 46.0, 32.0, -174.0, 35.0, 0.0, 5.0, 5.0, 1.0, 12.0, 14.0, 1.0, 80.0, -30.0, 600, 4, 1,
               1000, 0.2, 50, 20, 1, 1, 1.5, 0.7)

    def __init__(self, simulation_area, bandwidth, mbs_power, sbs_power, noise_power, mbs_height, sbs_height, mbs_gain,
                 sbs_gain, ue_height, number_subcarriers, number_ofdm_symbols, subframe_duration, max_bias, min_bias,
                 image_resolution, ue_arrival_rate, ue_service_rate, total_time_steps, priority_ue_proportion,
                 max_ue_per_mbs, max_ue_per_sbs, max_bs_per_ue, ordinary_ues_weight, priority_ues_weight,
                 outage_threshold):

        if simulation_area < 0 or simulation_area is None:
            raise RuntimeError('Incorrect value for parameter simulation_area: {}'.format(simulation_area))
        else:
            self._simulation_area = simulation_area

        if mbs_power < 0 or mbs_power is None:
            raise RuntimeError('Incorrect value for parameter mbs_power: {}'.format(mbs_power))
        else:
            self._mbs_power = mbs_power

        if sbs_power < 0 or sbs_power is None:
            raise RuntimeError('Incorrect value for parameter sbs_power: {}'.format(sbs_power))
        else:
            self._sbs_power = sbs_power

        if bandwidth < 0 or bandwidth is None:
            raise RuntimeError('Incorrect value for parameter bandwidth: {}'.format(bandwidth))
        else:
            self._bandwidth = bandwidth

        if noise_power > 0 or noise_power is None:
            raise RuntimeError('Incorrect value for parameter noise_power: {}'.format(noise_power))
        else:
            self._noise_power = noise_power

        if mbs_height < 0 or mbs_height is None:
            raise RuntimeError('Incorrect value for parameter mbs_height: {}'.format(mbs_height))
        else:
            self._mbs_height = mbs_height

        if sbs_height < 0 or sbs_height is None:
            raise RuntimeError('Incorrect value for parameter sbs_height: {}'.format(sbs_height))
        else:
            self._sbs_height = sbs_height

        if ue_height < 0 or ue_height is None:
            raise RuntimeError('Incorrect value for parameter ue_height: {}'.format(ue_height))
        else:
            self._ue_height = ue_height

        if mbs_gain < 0 or mbs_gain is None:
            raise RuntimeError('Incorrect value for parameter mbs_gain: {}'.format(mbs_gain))
        else:
            self._mbs_gain = mbs_gain

        if sbs_gain < 0 or sbs_gain is None:
            raise RuntimeError('Incorrect value for parameter sbs_gain: {}'.format(sbs_gain))
        else:
            self._sbs_gain = sbs_gain

        if number_subcarriers < 0 or number_subcarriers is None:
            raise RuntimeError('Incorrect value for parameter number_subcarriers: {}'.format(number_subcarriers))
        else:
            self._number_subcarriers = number_subcarriers

        if number_ofdm_symbols < 0 or number_ofdm_symbols is None:
            raise RuntimeError('Incorrect value for parameter number_ofdm_symbols: {}'.format(number_ofdm_symbols))
        else:
            self._number_ofdm_symbols = number_ofdm_symbols

        if subframe_duration < 0 or subframe_duration is None:
            raise RuntimeError(
                'Incorrect value for parameter subframe_duration: {}'.format(subframe_duration))
        else:
            self._subframe_duration = subframe_duration

        if max_bias is None:
            raise RuntimeError('Incorrect value for parameter max_bias: {}'.format(max_bias))
        else:
            self._max_bias = max_bias

        if min_bias is None:
            raise RuntimeError('Incorrect value for parameter min_bias: {}'.format(min_bias))
        else:
            self._min_bias = min_bias

        if image_resolution is None:
            raise RuntimeError('Incorrect value for parameter image_resolution: {}'.format(image_resolution))
        else:
            self._image_resolution = image_resolution

        if ue_arrival_rate < 0 or ue_arrival_rate is None:
            raise RuntimeError('Incorrect value for ue_arrival_rate parameter: {}'.format(ue_arrival_rate))
        else:
            self._ue_arrival_rate = ue_arrival_rate

        if ue_service_rate < 0 or ue_service_rate is None:
            raise RuntimeError('Incorrect value for ue_service_rate parameter: {}'.format(ue_service_rate))
        else:
            self._ue_service_rate = ue_service_rate

        if total_time_steps < 0 or total_time_steps is None:
            raise RuntimeError('Incorrect value for total_time_steps parameter: {}'.format(total_time_steps))
        else:
            self._total_time_steps = total_time_steps

        if priority_ue_proportion < 0 or priority_ue_proportion > 1:
            raise RuntimeError(
                'Incorrect value for priority_ue_proportion parameter: {}'.format(priority_ue_proportion))
        else:
            self._priority_ue_proportion = priority_ue_proportion

        if max_ue_per_mbs < 0 or max_ue_per_mbs is None:
            raise RuntimeError('Incorrect value for parameter max_ue_per_mbs: {}'.format(max_ue_per_mbs))
        else:
            self._max_ue_per_mbs = max_ue_per_mbs

        if max_ue_per_sbs < 0 or max_ue_per_sbs is None:
            raise RuntimeError('Incorrect value for parameter max_ue_per_sbs: {}'.format(max_ue_per_sbs))
        else:
            self._max_ue_per_sbs = max_ue_per_sbs

        if max_bs_per_ue < 0 or max_bs_per_ue is None:
            raise RuntimeError('Incorrect value for parameter max_bs_per_ue: {}'.format(max_bs_per_ue))
        else:
            self._max_bs_per_ue = max_bs_per_ue

        if ordinary_ues_weight < 0 or ordinary_ues_weight is None:
            raise RuntimeError('Incorrect value for parameter ordinary_ues_weight: {}'.format(ordinary_ues_weight))
        else:
            self._ordinary_ues_weight = ordinary_ues_weight

        if priority_ues_weight < 0 or priority_ues_weight is None:
            raise RuntimeError('Incorrect value for parameter priority_ues_weight: {}'.format(priority_ues_weight))
        else:
            self._priority_ues_weight = priority_ues_weight

        if outage_threshold < 0 or outage_threshold > 1:
            raise RuntimeError('Incorrect value for parameter outage_threshold: {}'.format(outage_threshold))
        else:
            self._outage_threshold = outage_threshold

    @property
    def simulation_area(self):
        return self._simulation_area

    @property
    def mbs_power(self):
        return self._mbs_power

    @property
    def sbs_power(self):
        return self._sbs_power

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def sbs_height(self):
        return self._sbs_height

    @property
    def sbs_gain(self):
        return self._sbs_gain

    @property
    def mbs_height(self):
        return self._mbs_height

    @property
    def mbs_gain(self):
        return self._mbs_gain

    @property
    def ue_height(self):
        return self._ue_height

    @property
    def number_subcarriers(self):
        return self._number_subcarriers

    @property
    def number_ofdm_symbols(self):
        return self._number_ofdm_symbols

    @property
    def subframe_duration(self):
        return self._subframe_duration

    @property
    def max_bias(self):
        return self._max_bias

    @property
    def min_bias(self):
        return self._min_bias

    @property
    def image_resolution(self):
        return self._image_resolution

    @property
    def ue_arrival_rate(self):
        return self._ue_arrival_rate

    @property
    def ue_service_rate(self):
        return self._ue_service_rate

    @property
    def total_time_steps(self):
        return self._total_time_steps

    @property
    def priority_ue_proportion(self):
        return self._priority_ue_proportion

    @property
    def max_ue_per_mbs(self):
        return self._max_ue_per_mbs

    @property
    def max_ue_per_sbs(self):
        return self._max_ue_per_sbs

    @property
    def max_bs_per_ue(self):
        return self._max_bs_per_ue

    @property
    def ordinary_ues_weight(self):
        return self._ordinary_ues_weight

    @property
    def priority_ues_weight(self):
        return self._priority_ues_weight

    @property
    def outage_threshold(self):
        return self._outage_threshold
