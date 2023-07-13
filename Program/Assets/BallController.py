from TSGEngine.World import BaseSystem
from Program.Assets.BallComponent import BallComponent
from TSGEngine.Physics.Components.Colliders.RectangleCollider import RectangleCollider


class BallController(BaseSystem):
    def fixed_process(self, fixed_dt, *args, **kwargs):
        for entity, component in self.world.get_entities_with_component(BallComponent):
            vector = component.direction * fixed_dt * component.speed
            future_y_pos = entity.transform.position.y + vector.y
            if (future_y_pos < -0.969 and component.direction.y < 0) or \
                    (future_y_pos > 0.969 and component.direction.y > 0):
                component.direction.y *= -1
                vector = component.direction * fixed_dt * component.speed

            if entity.components[RectangleCollider].colliding:
                collision_point = entity.components[RectangleCollider].collision_point

                if (component.direction.x > 0 and collision_point[0] > 0) or \
                        (component.direction.x < 0 and collision_point[0] < 0):
                    component.direction.x *= -1

            if entity.transform.position.x >= 1:
                component.score[0] += 1
            if entity.transform.position.x <= -1:
                component.score[1] += 1

            if entity.transform.position.x <= -1 or entity.transform.position.x >= 1:
                entity.transform.position = [0, 0, 0]
                speed = component.speed
                score = component.score
                component.__init__()
                component.speed = speed
                component.score = score

            entity.transform.translate(vector.x, vector.y, 0)
