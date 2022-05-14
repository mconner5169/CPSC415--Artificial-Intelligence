
import math
import sys
import numpy as np
import random

NUM_SIMS = 2000

class Condition():
    def __init__(self, terms):
        self.terms = terms

    def matches(self, term_vals):
        return all([ term in term_vals for term in self.terms ])


class RandomVariable():
    def __init__(self, name):
        self.name = name
        self._conditions = {}  # key=Condition, val=dict of vals/probs
    
    def add_condition(self, condition, probs):
        self._conditions[condition] = self.parse_probs(probs, condition)

    def parse_probs(self, probs, condition):
        parsed = { vp.split('=')[0]:float(vp.split('=')[1])
            for vp in probs.strip().split(' ') }
        return parsed

    def get_all_values(self):
        return self._conditions[list(self._conditions.keys())[0]]

    def get_prob_wrt_outcome(self, term_vals):
        for c, val_probs in self._conditions.items():
            if c.matches(term_vals):
                this_rvs_val = [
                    x for x in term_vals if x in self.get_all_values() ][0]
                return val_probs[this_rvs_val]
        assert False

    def get_prob_vector_for(self, term_vals):
        for c, val_probs in self._conditions.items():
            if c.matches(term_vals):
                return val_probs
        return None


class BBN():
    def __init__(self, name):
        self.name = name
        self.rvs = {}
        self.val_names_to_rvs = {}

    @classmethod 
    def from_filename(cls, filename):
        bbn = BBN(filename.split('.')[0])
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                stuff, probs = line.split(': ')
                var_name = stuff.split("|")[0]
                if "|" in stuff:
                    terms = stuff.split("|")[1].split("^")
                else:
                    terms = set()
                if var_name not in bbn.rvs:
                    bbn.rvs[var_name] = RandomVariable(var_name)
                condition = Condition(terms)
                bbn.rvs[var_name].add_condition(condition, probs)
        for rv in bbn.rvs.values():
            for val in rv.get_all_values():
                bbn.val_names_to_rvs[val] = rv
        return bbn
                    
    def compute_prob(self, query, exact=True):
        term_vals = set(query.split("|")[0].split("^"))
        terms = { self.val_names_to_rvs[tv] for tv in term_vals }
        if "|" in query:
            cond_vals = set(query.split("|")[1].split("^"))
        else:
            cond_vals = set()
        conditionals = { self.val_names_to_rvs[cv] for cv in cond_vals }
        method = getattr(self, 'compute_{}_prob'.format(
            'exact' if exact else 'approx'))
        return method(terms, term_vals, conditionals, cond_vals)
        
    def compute_approx_prob(self, terms, term_vals, conditionals, cond_vals):
        sims = [ self.sim_one() for _ in range(NUM_SIMS) ]
        csims = [ sim for sim in sims if cond_vals.issubset(sim) ]
        return sum([ term_vals.issubset(sim) for sim in csims ]) / len(csims)

    def sim_one(self):
        vals_set = set()
        rvs_left = list(self.rvs.values())
        while rvs_left:
            rv = random.choice(rvs_left)
            pv = rv.get_prob_vector_for(vals_set)
            if pv:
                val = self.choose_from_prob_vector(pv)
                vals_set |= {val}
                rvs_left.remove(rv)
        return vals_set

    def choose_from_prob_vector(self, pv):
        vals = []
        probs = []
        for val,prob in pv.items():
            vals += [val]
            probs += [prob]
        if sum(probs) != 1:
            probs = [ p/sum(probs) for p in probs ]
        return np.random.choice(vals,p=probs)
        
    def compute_exact_prob(self, terms, term_vals, conditionals, cond_vals):
        numerator = self.compute_with_some_vars_bound(term_vals | cond_vals)
        denominator = self.compute_with_some_vars_bound(cond_vals)
        return numerator / denominator

    def compute_with_some_vars_bound(self, term_vals):
        terms = { self.val_names_to_rvs[tv] for tv in term_vals }
        other_terms = set(self.rvs.values()) - set(terms)
        if len(other_terms) == 0:
            # Base case. No need to combinatorially explode.
            return self.compute_single_outcome(term_vals)
        other_terms = list(other_terms)
        return sum([self.compute_with_some_vars_bound(term_vals | {other_val})
            for other_val in other_terms[0].get_all_values() ])
            
    def compute_single_outcome(self, term_vals):
        prob = 1
        for rv in self.rvs.values():
            prob *= rv.get_prob_wrt_outcome(term_vals)
        return prob


def get_all_val_combos(vals):
    if len(vals) == 1:
        return tuple( (val,) for val in vals[0] )
    else:
        this = vals[0]
        rest = vals[1:]
        return tuple( (val,) + val2 for val in this
            for val2 in get_all_val_combos(rest))


my_bbn = BBN.from_filename(sys.argv[1])
if sys.argv[2] == 'exact':
    the_prob = my_bbn.compute_prob(sys.argv[3],True)
    print(the_prob)
elif sys.argv[2] == 'approx':
    the_prob = my_bbn.compute_prob(sys.argv[3],False)
    print(the_prob)
else:
    print('something went wrong')

