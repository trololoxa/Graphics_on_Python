from TSGEngine.World import BaseSystem
from Program.Assets.PlatformComponent import PlatformComponent


class PlatformController(BaseSystem):
    def process(self, dt, *args, **kwargs):
        for entity, component in self.world.get_entities_with_component(PlatformComponent):
            if self.world.input_manager.key_states[component.up] and entity.transform.position.y < 0.85:
                entity.transform.translate(0, 1 * dt * component.speed)
            if self.world.input_manager.key_states[component.down] and entity.transform.position.y > -0.85:
                entity.transform.translate(0, -1 * dt * component.speed)
