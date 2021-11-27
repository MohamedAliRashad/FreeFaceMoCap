import bpy
import bmesh
from ..config import Config

class FFMOCAP_OT_select_face_points(bpy.types.Operator):
    """Tooltip"""
    bl_idname = Config.operator_select_face_points_idname
    bl_label = "FFMoCap Select Face Points Operator"

    id: bpy.props.IntProperty(default=0)

    def execute(self, context):
        obj = context.scene.selected_char_prop.selected_char
        points_pos = context.scene.points_prop.points_pos
        points_selected = context.scene.points_prop.points_selected

        if obj is None:
            self.report({'ERROR'}, 'You have to select the character first!')
        
        else:
            me = obj.data
            
            # Get a BMesh representation
            bm = bmesh.from_edit_mesh(me)

            bm.faces.active = None

            # Modify the BMesh, can do anything here...
            for v in bm.verts:
                if v.select:
                    points_pos[self.id] = tuple(v.co)
                    points_selected[self.id] = True
                    break
        return {'FINISHED'}