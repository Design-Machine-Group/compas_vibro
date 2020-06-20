import matplotlib.pyplot as plt
from compas_vibro.vibro import from_W_to_dB
from compas_vibro.datastructures import VibroStructure

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


class VibroPlotter(object):

    def __init__(self, vibro_list, name_list, log_freq=False, log_pow=False, max_freq=None, min_freq=None):
        self.vibro_list = vibro_list
        self.log_freq = log_freq
        self.log_pow = log_pow
        self.colors = ['r', 'c', 'g', 'm', 'y', 'b', 'k', 'w']
        self.shapes = ['o', 's', 'p']
        self.name_list = name_list
        self.linewidth = 3
        self.markersize = 5
        self.max_freq = max_freq
        self.min_freq = min_freq

    def plot_vibrodata(self, tloss=True, radiated=False, incident=False, curves=False):

        if type(self.vibro_list) != list:
            self.vibro_list = [self.vibro_list]
            self.name_list = [self.name_list]

        for i, vibro in enumerate(self.vibro_list):
            if isinstance(vibro, VibroStructure):
                frequencies = vibro.frequencies
                freqs   = [frequencies[f] for f in frequencies]
                label = self.name_list[i]

                if tloss:
                    tramission_loss = vibro.transmission_loss
                    data = [tramission_loss[f] for f in tramission_loss]
                    label += ' TL'
                    shape = self.shapes[0]

                if radiated:
                    total_radiation_w = vibro.total_radiation_w
                    rads = [total_radiation_w[f] for f in total_radiation_w]
                    data = [from_W_to_dB(w) for w in rads]
                    label += ' W'
                    shape = self.shapes[1]

                if incident:
                    diffuse_incident_power = vibro.diffuse_incident_power
                    data = [from_W_to_dB(diffuse_incident_power[f]) for f in diffuse_incident_power]
                    label += ' I'
                    shape = self.shapes[2]

            elif type(vibro) == dict:
                label = self.name_list[i]
                freqs = vibro['freq']
                data = vibro['R']
                shape = self.shapes[0]

            color = self.colors[i]

            if not curves:
                color += shape

            if self.min_freq:
                delfreqs = [f for f in freqs if f < self.min_freq]
                freqs = [f for f in freqs if f >= self.min_freq]
                data = data[len(delfreqs):]

            if self.max_freq:
                freqs = [f for f in freqs if f <= self.max_freq]
                data = data[:len(freqs)]

            plt.plot(freqs, data, color, label=label, linewidth=self.linewidth, markersize=self.markersize)

        plt.xlabel('Frequencies (Hz)')
        plt.ylabel('Transmission Loss (dB)')
        plt.grid(which="both")
        plt.legend(loc=0)
        plt.show()

    def plot_radiation_curve(self, db=False):
        unit = 'W'
        frequencies = self.vibrostructure.frequencies
        total_radiation_w = self.vibrostructure.total_radiation_w
        freqs   = [frequencies[f] for f in frequencies]
        rads    = [total_radiation_w[f] for f in total_radiation_w]

        if db:
            rads = [from_W_to_dB(w) for w in rads]
            unit = 'dB'

        if self.log_freq:
            plt.semilogx(freqs, rads, 'ro')
        else:
            plt.plot(freqs, rads, 'ro')

        plt.xlabel('Frequencies (Hz)')
        plt.ylabel('Radiated sound power ({0})'.format(unit))
        plt.grid(which="both")
        plt.show()

    def plot_rad_vs_tl(self, log_freq=False):
        frequencies = self.vibrostructure.frequencies
        tramission_loss = self.vibrostructure.transmission_loss
        total_radiation_w = self.vibrostructure.total_radiation_w
        diffuse_incident_power = self.vibrostructure.diffuse_incident_power
        freqs   = [frequencies[f] for f in frequencies]
        tls     = [tramission_loss[f] for f in tramission_loss]
        rads    = [from_W_to_dB(total_radiation_w[f]) for f in total_radiation_w]
        incp    = [from_W_to_dB(diffuse_incident_power[f]) for f in diffuse_incident_power]

        if self.log_freq:
            plt.semilogx(freqs, tls, 'ro', label='TL')
            plt.semilogx(freqs, rads, 'bo', label='Radiation')
            plt.semilogx(freqs, incp, 'go', label='Incident')
        else:
            plt.plot(freqs, tls, 'ro', label='TL')
            plt.plot(freqs, rads, 'bo', label='Radiation')
            plt.plot(freqs, incp, 'go', label='Incident')

        plt.xlabel('Frequencies (Hz)')
        plt.ylabel('Radiated sound power / Transmission Loss(dB)')
        plt.grid(which="both")
        plt.legend()
        plt.show()

    def plot_rad_vs_inc(self, log_pow=False):
        frequencies = self.vibrostructure.frequencies
        total_radiation_w = self.vibrostructure.total_radiation_w
        diffuse_incident_power = self.vibrostructure.diffuse_incident_power
        freqs   = [frequencies[f] for f in frequencies]
        rads    = [total_radiation_w[f] for f in total_radiation_w]
        incp    = [diffuse_incident_power[f] for f in diffuse_incident_power]

        if self.log_pow:
            plt.semilogy(freqs, rads, 'bo', label='Radiation')
            plt.semilogy(freqs, incp, 'go', label='Incident')
        else:
            plt.plot(freqs, rads, 'bo', label='Radiation')
            plt.plot(freqs, incp, 'go', label='Incident')

        plt.xlabel('Frequencies (Hz)')
        plt.ylabel('Radiated sound power / Transmission Loss(dB)')
        plt.grid(which="both")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.datastructures import VibroStructure

    path = compas_vibro.TEMP
    name0 = 'mJ'
    filepath = os.path.join(path, name0 + '.json')
    vib0 = VibroStructure.from_json(filepath)

    path = compas_vibro.TEMP
    name1 = 'mK'
    filepath = os.path.join(path, name1 + '.json')
    vib1 = VibroStructure.from_json(filepath)

    path = compas_vibro.TEMP
    name2 = 'mL'
    filepath = os.path.join(path, name2 + '.json')
    vib2 = VibroStructure.from_json(filepath)

    path = compas_vibro.TEMP
    name3 = 'mM'
    filepath = os.path.join(path, name3 + '.json')
    vib3 = VibroStructure.from_json(filepath)

    path = compas_vibro.TEMP
    name4 = 'mN'
    filepath = os.path.join(path, name4 + '.json')
    vib4 = VibroStructure.from_json(filepath)

    path = compas_vibro.TEMP
    name5 = 'mO'
    filepath = os.path.join(path, name5 + '.json')
    vib5 = VibroStructure.from_json(filepath)


    # plotter = VibroPlotter([vib0, vib1], [name0, name1])
    plotter = VibroPlotter([vib0, vib1, vib2, vib3, vib4, vib5], [name0, name1, name2, name3, name4, name5])
    plotter.plot_vibrodata(tloss=True, radiated=False, incident=False)
