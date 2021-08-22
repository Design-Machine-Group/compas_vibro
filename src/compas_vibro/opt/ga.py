import random
import json
import pickle

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2021, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


class GA(object):
    def __init__(self,
                 func,
                 num_var,
                 num_gen=100,
                 num_pop=50,
                 len_bin=8,
                 boundaries=[0., 1.],
                 num_elite= 10,
                 mut_p=.01,
                 min_fit=None):

        # inputs - - -
        self.num_gen = num_gen
        self.num_pop = num_pop
        self.num_var = num_var
        self.num_elite =  num_elite
        self.mut_p = mut_p
        self.fit_func = func
        self.min_fit = min_fit
        self.per_gen_out = False
        self.filepath = 'ga_opt.obj'

        if type(len_bin) == int:
            self.len_bin = [len_bin] * self.num_var
        else:
            self.len_bin = len_bin
        if len(boundaries) == 2:
            self.boundaries = [[0., 1.]] * self.num_var
        else:
            self.boundaries = boundaries

        # data - - -
        self.pop = {}
        self.fitnesses = {}
        self.sort = []
        self.gen = 0
        self.pool = []
        self.num_bits = sum(self.len_bin)
        self.num_rpop = self.num_pop - self.num_elite
        self.best_ind = {}
        self.best_fit = {}
        self.best_pop = {}
        self.fit_min_max_avg = {}

    def optimize(self):
        self.pop = {i:{} for i in range(self.num_gen)}
        self.random_pop()
        for gen in range(self.num_gen):
            self.scale_pop()
            self.compute_fitness()
            self.sort_pop()
            if self.per_gen_out:
                # self.write_json()
                self.to_obj()
            print('Generation {} - Best fit {} - Best Ind {}'.format(gen,
                                                                     self.best_fit[self.gen],
                                                                     self.best_ind[self.gen]))
            if self.min_fit != None and self.best_fit[gen] <= self.min_fit:
                break
            elif gen < self.num_gen - 1:
                self.elite_pop()
                self.tournament()
                self.crossover()
                self.mutation()
                self.gen += 1
        # self.write_json()
        self.to_obj()

    def random_pop(self):
        for i in range(self.num_pop):
            genes = []
            for j in range(self.num_var):
                genes.extend([int(round(random.random(), 0)) for _ in range(self.len_bin[j])])
            self.pop[self.gen][i] = {'bin': genes}

    def scale_pop(self):
        for kpop in self.pop[self.gen]:
            self.pop[self.gen][kpop].update({'scaled':[]})
            s = 0
            for i in range(self.num_var):
                n = self.len_bin[i] + s
                low, high = self.boundaries[i]
                gene = self.pop[self.gen][kpop]['bin'][s:n]
                maxbin = float((2 ** self.len_bin[i]) - 1)
                decoded = self.decode_gene(gene)
                scaled = low + (high - low) * decoded / maxbin
                # print(s, n, scaled, decoded, gene)
                self.pop[self.gen][kpop]['scaled'].append(scaled)
                s = n
            # print('')

    def decode_gene(self, gene):
        value = 0
        for u, g in enumerate(gene):
            if g == 1:
                value = value + 2**u
        return value

    def compute_fitness(self):
        # fit = self.fit_func(self.pop[self.gen][kpop]['scaled'])
        # self.pop[self.gen][kpop]['fitness'] = fit
        for kpop in self.pop[self.gen]:
            # print(self.pop[self.gen][kpop]['bin'])
            # print(self.pop[self.gen][kpop]['scaled'])
            # print('')
            bin_key = ''.join(map(str, self.pop[self.gen][kpop]['bin']))
            if bin_key in self.fitnesses:
                self.pop[self.gen][kpop]['fitness'] = self.fitnesses[bin_key]
                # print('found it', kpop)
            else:
                # print('not here')
                fit = self.fit_func(self.pop[self.gen][kpop]['scaled'])
                self.pop[self.gen][kpop]['fitness'] = fit
                self.fitnesses[bin_key] = fit

    def elite_pop(self):
        for i, epop in enumerate(self.sort[:self.num_elite]):
            self.pop[self.gen + 1][i] = self.pop[self.gen][epop]

    def sort_pop(self):
        fit_pop = [(kpop,self.pop[self.gen][kpop]['fitness']) for kpop in self.pop[self.gen]]
        sort = sorted(fit_pop, key = lambda x: x[1])

        fit_pop = [self.pop[self.gen][kpop]['fitness'] for kpop in self.pop[self.gen]]
        self.best_ind[self.gen] = sort[0][0]
        self.best_fit[self.gen] = sort[0][1]
        self.best_pop[self.gen] = self.pop[self.gen][self.best_ind[self.gen]]
        self.fit_min_max_avg[self.gen] = {'min':min(fit_pop),
                                          'max': max(fit_pop),
                                          'avg': sum(fit_pop) / float(len(fit_pop))}
        self.sort = [s[0] for s in sort]

    def tournament(self):
        indices = range(self.num_pop)
        a = random.sample(indices, self.num_rpop)
        b = random.sample(indices, self.num_rpop)
        self.pool = []
        for i in range(len(a)):
            f1 = self.pop[self.gen][a[i]]['fitness']
            f2 = self.pop[self.gen][b[i]]['fitness']
            if f1 < f2:
                self.pool.append(a[i])
            else:
                self.pool.append(b[i])

    def crossover(self):
        a = self.pool[:int(len(self.pool) / 2)]
        b = self.pool[int(len(self.pool) / 2):]
        for i in range(len(a)):
            bin1 = self.pop[self.gen][a[i]]['bin']
            bin2 = self.pop[self.gen][b[i]]['bin']
            cp = random.randint(1, len(bin1))
            bin3 = bin1[:cp] + bin2[cp:]
            bin4 = bin2[:cp] + bin1[cp:]
            self.pop[self.gen + 1][self.num_elite + i] = {'bin': bin3}
            self.pop[self.gen + 1][self.num_pop - i - 1] = {'bin': bin4}

    def mutation(self):
        #TODO: this mutation in expensive, implement one based on jumps (Goldberg 1989)
        for kpop in range(self.num_elite, self.num_pop):
            self.pop[self.gen + 1]
            self.pop[self.gen + 1][kpop]
            self.pop[self.gen + 1][kpop]['bin']
            for i, gene in enumerate(self.pop[self.gen + 1][kpop]['bin']):
                if random.random() < self.mut_p:
                    if gene == 0:
                        self.pop[self.gen + 1][kpop]['bin'][i] = 1
                    else:
                        self.pop[self.gen + 1][kpop]['bin'][i] = 0

    def write_json(self):
        with open(self.filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'pop'           :{},
                'num_gen'       : self.num_gen,
                'num_pop'       : self.num_pop,
                'num_var'       : self.num_var,
                'len_bin'       : self.len_bin,
                'boundaries'    : self.boundaries,
                'fit_func'      : self.fit_func.__name__,
                'fitnesses'     : self.fitnesses,
        }
        return data

    def to_obj(self):
        self.fit_func = self.fit_func.__name__
        self.fitnesses = None
        self.pop = {}
        with open(self.filepath, 'wb') as f:
            pickle.dump(self, f, protocol=2)
        print('***** GA saved to: {0} *****\n'.format(self.filepath))

    @staticmethod
    def from_obj(filepath):
        with open(filepath, 'rb') as f:
            ga_ = pickle.load(f)
        print('***** Structure loaded from: {0} *****'.format(filepath))
        return ga_

    def plot_generations(self):
        import matplotlib.pyplot as plt

        minf = []
        maxf = []
        avgf = []
        gen = []
        for kgen in self.fit_min_max_avg:
            minf.append(self.fit_min_max_avg[kgen]['min'])
            maxf.append(self.fit_min_max_avg[kgen]['max'])
            avgf.append(self.fit_min_max_avg[kgen]['avg'])
            gen.append(kgen)

        plt.plot(gen, minf, color='black', linewidth=.8, label='Min. fitness')
        plt.plot(gen, avgf, color='red', linewidth=.8, label='Avg. fitness')
        plt.plot(gen, maxf, color='black', linewidth=.4, label='Max. fitness')
        plt.grid(linestyle=':')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Optimization progress')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    for i in range(50): print('')

    def func(x):
        return sum(x)

    ga = GA(func, 40, min_fit=0.)
    ga.optimize()
    ga.plot_generations()
