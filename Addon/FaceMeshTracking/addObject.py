import bpy
import bmesh
from bpy_extras.object_utils import object_data_add

def add_object(self, context, landmarks):
    scale_x = self.scale.x
    scale_y = self.scale.y
    scale_z = self.scale.z

    def scaling(x):
        return [x[0] * scale_x, x[1] * scale_y, x[2] * scale_z]

    verts = landmarks
    verts = list(map(scaling, verts))

    if 'FreeFaceMoCap_Obj' in bpy.data.objects:
        obj = bpy.data.objects['FreeFaceMoCap_Obj']
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        for obj_v, v in zip(bm.verts, verts):
            obj_v.co = tuple(v)
        bm.to_mesh(obj.data)
    else:    
        edges = []
        faces = []

        mesh = bpy.data.meshes.new(name="FreeFaceMoCap_Obj")
        mesh.from_pydata(verts, edges, faces)
        # useful for development when the mesh may be invalid.
        # mesh.validate(verbose=True)
        object_data_add(context, mesh, operator=self)