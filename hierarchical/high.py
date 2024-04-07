import pm4py
from typing import Collection, Dict, Any
from copy import deepcopy


class HighHierarchicalNet(pm4py.PetriNet):
    class Subprocess(pm4py.PetriNet.Transition):
        def __init__(self, name, label=None, in_arcs=None, out_arcs=None, properties=None, subprocess=None):
            super().__init__(name, label, in_arcs, out_arcs, properties)
            self.__subprocess = pm4py.PetriNet() if subprocess is None else subprocess

        def __get_subprocess(self):
            return self.__subprocess

        def __set_subprocess(self, subprocess):
            self.__subprocess = subprocess

        # TODO: enhance repr! That's a Petri Net in one transition, after all...
        def __repr__(self):
            if self.label is None:
                return "(" + str(self.name) + ", None)"
            else:
                return "(" + str(self.name) + ", '" + str(self.label) + "')"

        def __deepcopy__(self, memodict={}):
            if id(self) in memodict:
                return memodict[id(self)]
            new_trans = HighHierarchicalNet.Subprocess(self.name, self.label, properties=self.properties)
            memodict[id(self)] = new_trans
            for arc in self.in_arcs:
                new_arc = deepcopy(arc, memo=memodict)
                new_trans.in_arcs.add(new_arc)
            for arc in self.out_arcs:
                new_arc = deepcopy(arc, memo=memodict)
                new_trans.out_arcs.add(new_arc)
            return new_trans

        subprocess = property(__get_subprocess, __set_subprocess)

    def __init__(self, name: str = None, places: Collection[pm4py.PetriNet.Place] = None,
                 transitions: Collection[pm4py.PetriNet.Transition] = None, arcs: Collection[pm4py.PetriNet.Arc] = None,
                 properties: Dict[str, Any] = None):
        super().__init__(name, places, transitions, arcs, properties)

    def __hash__(self):
        ret = 0
        for p in self.places:
            ret += hash(p)
            ret = ret % 479001599
        for t in self.transitions:
            ret += hash(t)
            ret = ret % 479001599
        return ret

    def __deepcopy__(self, memodict={}):
        from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to
        this_copy = HighHierarchicalNet(self.name)
        memodict[id(self)] = this_copy
        for place in self.places:
            place_copy = pm4py.PetriNet.Place(place.name, properties=place.properties)
            this_copy.places.add(place_copy)
            memodict[id(place)] = place_copy
        for trans in self.transitions:
            if trans is HighHierarchicalNet.Subprocess:
                trans_copy = HighHierarchicalNet.Subprocess(trans.name, trans.label, properties=trans.properties)
            else:
                trans_copy = pm4py.PetriNet.Transition(trans.name, trans.label, properties=trans.properties)
            this_copy.transitions.add(trans_copy)
            memodict[id(trans)] = trans_copy
        for arc in self.arcs:
            add_arc_from_to(memodict[id(arc.source)], memodict[id(arc.target)], this_copy, weight=arc.weight)
        return this_copy
