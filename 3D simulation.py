from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class LightReflection3D(ShowBase):
    def __init__(self):
        super().__init__()
        self.setup_scene()
        self.setup_light()
        self.setup_mirrors()
        self.setup_rays()

    def setup_scene(self):
        self.disableMouse()  # Use default camera controls
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(0, 0, 0))

    def setup_light(self):
        # Light source at origin
        self.light = self.render.attachNewNode(PointLight("light"))
        self.light.setPos(0, 0, 0)

    def setup_mirrors(self):
        # Create a reflective plane (mirror)
        self.mirror = self.loader.loadModel("models/plane")
        self.mirror.setScale(5, 5, 5)
        self.mirror.setPos(0, 0, 0)
        self.mirror.reparentTo(self.render)

    def setup_rays(self):
        # Emit rays in multiple directions
        directions = [
            Vec3(1, 0, 0), Vec3(-1, 0, 0), 
            Vec3(0, 1, 0), Vec3(0, -1, 0),
            Vec3(0, 0, 1), Vec3(0, 0, -1)
        ]
        for dir in directions:
            ray = self.render.attachNewNode("ray")
            ray.setPos(0, 0, 0)
            ray.setPythonTag("direction", dir.normalized())
            ray.setPythonTag("bounces", 0)
            self.taskMgr.add(self.update_ray, f"update_ray_{dir}", extraArgs=[ray])

    def update_ray(self, ray, task):
        direction = ray.getPythonTag("direction")
        bounces = ray.getPythonTag("bounces")
        new_pos = ray.getPos() + direction * 0.1

        # Check collision with mirror
        collision = self.physicsWorld.rayTestClosest(ray.getPos(), new_pos)
        if collision.hasHit() and bounces < 5:
            # Calculate reflection direction
            normal = collision.getHitNormal()
            reflection = direction - 2 * direction.dot(normal) * normal
            ray.setPythonTag("direction", reflection.normalized())
            ray.setPythonTag("bounces", bounces + 1)
            new_pos = collision.getHitPos()

        # Update ray position and draw
        ray.setPos(new_pos)
        self.draw_line(ray.getPos(), direction)
        return task.cont

    def draw_line(self, pos, dir):
        line = LineSegs()
        line.setColor(1, 0, 0, 1)
        line.moveTo(pos)
        line.drawTo(pos + dir * 0.2)
        line_node = line.create()
        self.render.attachNewNode(line_node)

app = LightReflection3D()
app.run()
