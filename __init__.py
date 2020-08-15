bl_info = {
    "name": "Unitize Mesh",
    "author": "Dennis",
    "description": "Scales a mesh's geometry such that it fits in a unit cube around the origin.",
    "blender": (2, 81, 0),
    "category": "Object",
}

import bpy
import math


class Unitize(bpy.types.Operator):
    """Scales a mesh's geometry such that it fits in a unit cube around the origin."""
    bl_idname = 'object.unitize'
    bl_label = "Unitize Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if len( context.selected_objects ) != 1:
            self.report({'WARNING'}, "Select exactly one object")
            return {'CANCELLED'}
        else:
            obj = context.selected_objects[0]

            # Phase 1 #
            # Find the current bounds of the mesh

            minX = math.inf
            minY = math.inf
            minZ = math.inf
            maxX = -math.inf
            maxY = -math.inf
            maxZ = -math.inf

            for v in obj.data.vertices:
                minX = min( minX, v.co.x )
                minY = min( minY, v.co.y )
                minZ = min( minZ, v.co.z )
                maxX = max( maxX, v.co.x )
                maxY = max( maxY, v.co.y )
                maxZ = max( maxZ, v.co.z )

            offX = ( maxX + minX ) / 2
            offY = ( maxY + minY ) / 2
            offZ = ( maxZ + minZ ) / 2

            sizeX = maxX - minX
            sizeY = maxY - minY
            sizeZ = maxZ - minZ

            size = max( sizeX, sizeY, sizeZ )

            # Phase 2 #
            # Transform all vertices to make them fit in the unit cube around
            # the origin: [-.5,.5]x[-.5,.5]x[-.5,.5]

            for v in obj.data.vertices:
                v.co.x = ( v.co.x - offX ) / size
                v.co.y = ( v.co.y - offY ) / size
                v.co.z = ( v.co.z - offZ ) / size

            return {'FINISHED'}


def register():
    bpy.utils.register_class(Unitize)


def unregister():
    bpy.utils.unregister_class(Unitize)


if __name__ == '__main__':
    register()
