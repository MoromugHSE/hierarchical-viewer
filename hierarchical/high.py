import pm4py
from typing import Collection, Dict, Any
from copy import deepcopy


class HighHierarchicalNet(pm4py.PetriNet):
    class Subprocess(pm4py.PetriNet.Transition):
        def __init__(self, name, label=None, in_arcs=None, out_arcs=None, properties=None, subprocess=None):
            super().__init__(name, label, in_arcs, out_arcs, properties)
            self.__subprocess = pm4py.PetriNet() if subprocess is None else subprocess

        def __get_subprocess(self):

        def __repr__(self):
            if self.label is None:
                return "("+str(self.name)+", None)"
            else:
                return "("+str(self.name)+", '"+str(self.label)+"')"

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

    def __init__(self, name: str=None, places: Collection[pm4py.PetriNet.Place]=None, transitions: Collection[pm4py.PetriNet.Transition]=None, arcs: Collection[pm4py.PetriNet.Arc]=None, properties:Dict[str, Any]=None):
        super().__init__(name, places, transitions, arcs, properties)

    def __get_name(self) -> str:
        return self.__name

    def __set_name(self, name):
        self.__name = name

    def __get_places(self) -> Collection[Place]:
        return self.__places

    def __get_transitions(self) -> Collection[Transition]:
        return self.__transitions

    def __get_arcs(self) -> Collection[Arc]:
        return self.__arcs

    def __get_properties(self) -> Dict[str, Any]:
        return self.__properties

    def __hash__(self):
        ret = 0
        for p in self.places:
            ret += hash(p)
            ret = ret % 479001599
        for t in self.transitions:
            ret += hash(t)
            ret = ret % 479001599
        return ret

    def __eq__(self, other):
        # for the Petri net equality keep the ID for now
        return id(self) == id(other)

    def __deepcopy__(self, memodict={}):
        from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to
        this_copy = PetriNet(self.name)
        memodict[id(self)] = this_copy
        for place in self.places:
            place_copy = PetriNet.Place(place.name, properties=place.properties)
            this_copy.places.add(place_copy)
            memodict[id(place)] = place_copy
        for trans in self.transitions:
            trans_copy = PetriNet.Transition(trans.name, trans.label, properties=trans.properties)
            this_copy.transitions.add(trans_copy)
            memodict[id(trans)] = trans_copy
        for arc in self.arcs:
            add_arc_from_to(memodict[id(arc.source)], memodict[id(arc.target)], this_copy, weight=arc.weight)
        return this_copy

    def __repr__(self):
        ret = ["places: ["]
        places_rep = []
        for place in self.places:
            places_rep.append(repr(place))
        places_rep.sort()
        ret.append(" " + ", ".join(places_rep) + " ")
        ret.append("]\ntransitions: [")
        trans_rep = []
        for trans in self.transitions:
            trans_rep.append(repr(trans))
        trans_rep.sort()
        ret.append(" " + ", ".join(trans_rep) + " ")
        ret.append("]\narcs: [")
        arcs_rep = []
        for arc in self.arcs:
            arcs_rep.append(repr(arc))
        arcs_rep.sort()
        ret.append(" " + ", ".join(arcs_rep) + " ")
        ret.append("]")
        return "".join(ret)

    def __str__(self):
        return self.__repr__()

    name = property(__get_name, __set_name)
    places = property(__get_places)
    transitions = property(__get_transitions)
    arcs = property(__get_arcs)
    properties = property(__get_properties)