# To enable, go to the panel at:
#   View3D > Navigation > ViewCube
# Then, click "View Widget"
# 
# Notes:
#  - If the Properties panel is open, the widget may be hidden
#  - Currently the widget zoom doesn't work in Orthographic

import bpy
import bgl
import blf
import mathutils
import math

bl_info = {
    "name": "ViewCube",
    "author": "Tony Coculuzzi",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "View3D > ViewCube",
    "description": "An on-scree 3D widget used to navigate the 3D View",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/",
    "category": "3D View",
}

def draw_callback_px(self, context):
    
    #get RegionView3D
    r3d = 0
    for space in context.area.spaces:
        if space.type == 'VIEW_3D':
            r3d = space.region_3d
    
    if r3d == 0:
        print("region_3D NOT FOUND")
        pass
    
    screenWidth = context.area.width
    screenHeight = context.area.height
    
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glEnable(bgl.GL_DEPTH_TEST)
    
    # get old viewport properties
    oldViewport = bgl.Buffer(bgl.GL_INT, 4)
    bgl.glGetIntegerv(bgl.GL_VIEWPORT, oldViewport) 
    
    #oldViewDistance = r3d.view_distance
    
    oldMatrix = bgl.Buffer(bgl.GL_DOUBLE, [4,4])
    bgl.glGetDoublev(bgl.GL_PROJECTION_MATRIX, oldMatrix)
    
    viewportWidth = int(oldViewport[2]/4)
    viewportHeight = int(oldViewport[3]/4)
    
    #bgl.glViewport(screenWidth - viewportWidth, screenHeight - viewportHeight, viewportWidth, viewportHeight)
    bgl.glViewport(screenWidth - viewportWidth, (screenHeight - viewportHeight) + int((viewportHeight-viewportWidth)/2), viewportWidth, viewportHeight)
    
    draw_cube(context, r3d)

    # restore opengl defaults
    #r3d.view_distance = oldViewDistance
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glDisable(bgl.GL_DEPTH_TEST)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    bgl.glViewport(oldViewport[0],oldViewport[1],oldViewport[2],oldViewport[3])
    
    bgl.glPushMatrix()
    bgl.glLoadMatrixf(oldMatrix)
    bgl.glPopMatrix()

def draw_cube(context, r3d):
    
    #direction = r3d.view_rotation * mathutils.Vector((0.0, 0.0, -1.0))
    #position = r3d.view_matrix.inverted().translation
    
    #r3d.view_distance = 1;
    #r3d.view_camera_zoom = 1
    
    rad2deg = 360.0 / (math.pi * 2.0)
    rotation = r3d.view_rotation.to_euler()
    rotation.x = (rotation.x * rad2deg) + 180
    rotation.y = (rotation.y * rad2deg)
    rotation.z = (rotation.z * rad2deg)
    
    #r3d.view_rotation = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ').to_quaternion()
    
    size = 1
    
    centerX = 0
    centerY = 0
    centerZ = 0
    
    #colors
    cTop = mathutils.Color((130.0/255.0, 130.0/255.0, 130.0/255.0))
    cBot = mathutils.Color((100.0/255.0, 100.0/255.0, 100.0/255.0))
    cLine = mathutils.Color((0.0/255.0, 0.0/255.0, 0.0/255.0))
    
    # BEGIN MATRIX
    bgl.glPushMatrix()
    bgl.glLoadIdentity()
    #bgl.glTranslated(0.0, 0.0, 0.0)
    bgl.glOrtho(-5, 5, -5, 5, 0.01, 100)
    
    bgl.glRotatef(rotation.x, 1.0, 0.0, 0.0)
    bgl.glRotatef(rotation.y, 0.0, 1.0, 0.0)
    bgl.glRotatef(rotation.z, 0.0, 0.0, 1.0)
    
    # FACES TEXT
    #font_id = 0
    #blf.position(font_id, 0, 0, 1)
    #blf.size(font_id, 10, 72)
    #blf.draw(font_id, "top")
    
    # QUADS
    bgl.glBegin(bgl.GL_QUADS)
    
    # top
    bgl.glColor3f(cTop.r, cTop.g, cTop.b)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ + size)
    
    # bottom
    bgl.glColor3f(cBot.r, cBot.g, cBot.b)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ - size)
    
    # left
    bgl.glColor3f(cBot.r, cBot.g, cBot.b)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ - size)
    bgl.glColor3f(cTop.r, cTop.g, cTop.b)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ + size)
    
    # right
    bgl.glColor3f(cBot.r, cBot.g, cBot.b)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ - size)
    bgl.glColor3f(cTop.r, cTop.g, cTop.b)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ + size)
    
    # front
    bgl.glColor3f(cBot.r, cBot.g, cBot.b)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ - size)
    bgl.glColor3f(cTop.r, cTop.g, cTop.b)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ + size)
    
    # back
    bgl.glColor3f(cBot.r, cBot.g, cBot.b)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ - size)
    bgl.glColor3f(cTop.r, cTop.g, cTop.b)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ + size)
    
    bgl.glEnd()
    
    # LINES
    bgl.glColor3f(cLine.r, cLine.g, cLine.b)
    bgl.glLineWidth(1)
    size = size * 1.01
    
    # top
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ + size)
    bgl.glEnd()
    
    # bottom
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ - size)
    bgl.glEnd()
    
    # left
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ - size)
    bgl.glEnd()
    
    # right
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ - size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ - size)
    bgl.glEnd()
    
    # front
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY + size, centerZ - size)
    bgl.glEnd()
    
    # back
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ - size)
    bgl.glVertex3f(centerX - size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ + size)
    bgl.glVertex3f(centerX + size, centerY - size, centerZ - size)
    bgl.glEnd()
    
    # END MATRIX
    bgl.glPopMatrix()

class ViewCubeWidgetOperator(bpy.types.Operator):
    bl_idname = "viewcube.widget"
    bl_label = "ViewCube Widget"

    def modal(self, context, event):
        context.area.tag_redraw()
        
        #if event.type == 'MOUSEMOVE':
            #self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

        if event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            print("ViewCube Exited")
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # Add the region OpenGL drawing callback, draw in view space with 'POST_VIEW' and 'PRE_VIEW', or 2D space with 'POST_PIXEL'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_VIEW')

            context.window_manager.modal_handler_add(self)
            print()
            print("ViewCube Started")
            print(" - To exit ViewCube, press ESC")
            print()
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

#begin Panel
class ViewCubePanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'ViewCube'
    bl_context = 'objectmode'
    bl_category = 'Navigation'
    
    # Drawing UI elements
    def draw(self, context):
        layout = self.layout
        layout.operator("viewcube.widget", text ="View Widget", icon="MESH_CUBE")
#end Panel

#Operators
class ViewCube_ViewLeft(bpy.types.Operator):
    bl_idname = 'viewcube.view_left'
    bl_label = 'Left Viewpoint'
    bl_description = 'View from the Left'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='LEFT')
        return {'FINISHED'}


class ViewCube_ViewRight(bpy.types.Operator):
    bl_idname = 'viewcube.view_right'
    bl_label = 'Right Viewpoint'
    bl_description = 'View from the Right'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='RIGHT')
        return {'FINISHED'}


class ViewCube_ViewFront(bpy.types.Operator):
    bl_idname = 'viewcube.view_front'
    bl_label = 'Front Viewpoint'
    bl_description = 'View from the Front'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='FRONT')
        return {'FINISHED'}

class ViewCube_ViewBack(bpy.types.Operator):
    bl_idname = 'viewcube.view_back'
    bl_label = 'Back Viewpoint'
    bl_description = 'View from the Back'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='BACK')
        return {'FINISHED'}


class ViewCube_ViewTop(bpy.types.Operator):
    bl_idname = 'viewcube.view_top'
    bl_label = 'Top Viewpoint'
    bl_description = 'View from the Top'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='TOP')
        return {'FINISHED'}


class ViewCube_ViewBottom(bpy.types.Operator):
    bl_idname = 'viewcube.view_bottom'
    bl_label = 'Bottom Viewpoint'
    bl_description = 'View from the Bottom'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='BOTTOM')
        return {'FINISHED'}
#end Operators

#Registration
classes = [
    ViewCubePanel,
    ViewCubeWidgetOperator,
    ViewCube_ViewLeft,
    ViewCube_ViewRight,
    ViewCube_ViewFront,
    ViewCube_ViewBack,
    ViewCube_ViewTop,
    ViewCube_ViewBottom
]

def register():
    print("ViewCube registered")
    for c in classes:
        bpy.utils.register_class(c)
    
def unregister():
    print("ViewCube unregistered")
    for c in classes:
        bpy.utils.unregister_class(c)
    
#Registration from blender Text Editor
if __name__ == '__main__':
    register()