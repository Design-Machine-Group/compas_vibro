import rhinoscriptsyntax as rs
from compas.geometry import normal_polygon
from compas.geometry import add_vectors
from compas.geometry import normalize_vector
from compas.geometry import scale_vector


def plot_structure(structure):
    eks = []
    for ep in structure.element_properties:
        elements = structure.element_properties[ep].elements
        elset = structure.element_properties[ep].elset
        if elements:
            eks = elements
        elif elset:
            eks = structure.sets[elset].selection
        sec = structure.element_properties[ep].section
        t = structure.sections[sec].geometry['t']
        for ek in eks:
            nodes = structure.elements[ek].nodes
            vert = [structure.nodes[nk].xyz() for nk in nodes]
            n = scale_vector(normalize_vector(normal_polygon(vert)), t / 2.)
            n_ = scale_vector(n, -1)
            v_out = [add_vectors(v, n) for v in vert]
            v_in = [add_vectors(v, n_) for v in vert]
            s1 = rs.AddSrfPt(v_out)
            s2 = rs.AddSrfPt(v_in)
            srfs = [s1, s2]
            for i in range(len(v_in)):
                srf = rs.AddSrfPt([v_in[-i], v_in[-i - 1], v_out[-i - 1], v_out[-i]])
                if srf:
                    srfs.append(srf)
            rs.JoinSurfaces(srfs, delete_input=True)
        
        
if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure
    
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))
    fpath = os.path.join(compas_vibro.TEMP, 'clt_1_remeshed_field.obj')
    s = Structure.from_obj(fpath)
    plot_structure(s)