import dataclasses
import time
import pytest

from Engine.World import World, BaseSystem


@pytest.fixture()
def new_world():
    return World()


def test_entities_creation(new_world):
    # Test entity creation
    entity1 = new_world.create_entity()
    entity2 = new_world.create_entity()
    assert len(new_world.entities) == 2
    # TODO: pointer type test and pointer link getting


def test_system_creation(new_world):
    # test step func in world for systems
    # Check is world same as given world
    system = SystemStepTest()
    system2 = TimedSystem()

    new_world.add_system(system)
    assert system.world is not None
    assert len(new_world.systems) == 1

    new_world.add_system(system2)
    assert len(new_world.systems) == 2

    get_system = new_world.get_system(SystemStepTest)
    assert get_system == system

    new_world.delete_system(SystemStepTest)
    assert system.world is None and get_system.world is None
    assert len(new_world.systems) == 1


def test_timed_systems(new_world):
    # Check for system step time
    system = TimedSystem()
    system2 = TimedSystem2()

    new_world.add_system(system)
    new_world.add_system(system2)

    new_world.step()

    get_time = new_world.get_time(TimedSystem)
    assert 0.8 < get_time < 1.2

    get_time2 = new_world.get_time(TimedSystem2)
    assert 1.8 < get_time2 < 2.2

    get_times = new_world.get_times()
    assert len(get_times) == 2
    assert get_times[0] == get_time and get_times[1] == get_time2

    get_times = new_world.get_times()
    assert len(get_times) == 2
    assert get_times[0] == get_time and get_times[1] == get_time2


def test_entity_components_system_combination(new_world):
    # Checks components getting, modification and removal trough pointer and World class
    system = ECSystem()
    new_world.add_system(system)

    component1 = ExampleComponent()
    component2 = ExampleComponent2()
    component3 = ExampleComponent()
    component3.z = 'sus'

    entity1 = new_world.create_entity()
    entity1.add_component(component1)
    entity2 = new_world.create_entity(component2)
    entity3 = new_world.create_entity()
    new_world.add_component(entity3, component3, component2)

    new_world.step()

    assert len(entity3.components) == 2
    entity3.remove_component(ExampleComponent2)
    assert len(entity3.components) == 1

    with pytest.raises(KeyError):
        entity3.remove_component(ExampleComponent2)


def test_system_step(new_world):
    # Uses some example system for check
    system = SystemStepTest()
    new_world.add_system(system)
    new_world.step()
    assert new_world.next_entity_id == 2281337


def test_entity_deletion(new_world):
    # pointer should self-delete if called
    # entities len in world should change, but next id should be same
    pointer = new_world.create_entity()
    pointer2 = new_world.create_entity()
    next_id = new_world.next_entity_id
    assert len(new_world.entities) == 2
    pointer.destroy()
    assert len(new_world.entities) == 1
    assert next_id == new_world.next_entity_id


def test_scene_manager(new_world):
    scene_manager = ExampleSceneManager()
    new_world.set_scene_manager(scene_manager)

    system = SceneSystem()
    new_world.add_system(system)

    scene = scene_manager.create_scene('no', True, True)
    scene2 = scene_manager.create_scene('no2')

    entity1 = new_world.create_entity()
    entity2 = new_world.create_entity()
    entity3 = new_world.create_entity()

    entity1.add_component(ExampleComponent())
    entity2.add_component(ExampleComponent())
    entity3.add_component(ExampleComponent())

    scene.append(entity1)
    scene.append(entity2)

    scene2.append(entity3)

    new_world.step()


class SystemStepTest(BaseSystem):
    def process(self):
        # systems fetch all data from world and components
        self.world.next_entity_id = 2281337


class ECSystem(BaseSystem):
    def process(self):
        len_comp2 = 0
        len_comp1 = 0

        for entity, component in self.world.get_entities_with_component(ExampleComponent):
            len_comp1 += 1
            if entity is None or component is None:
                raise Exception('Some part is None')

        for entity, component in self.world.get_entities_with_component(ExampleComponent2):
            len_comp2 += 1
            if entity is None or component is None:
                raise Exception('Some part is None')

        assert len_comp2 == 2
        assert len_comp1 == 2


class TimedSystem(BaseSystem):
    def process(self):
        time.sleep(1)


class TimedSystem2(BaseSystem):
    def process(self):
        time.sleep(2)


class SceneSystem(BaseSystem):
    def process(self):
        active_entities = 0
        all_entities = 0

        for entity, component in self.world.get_entities_with_component(ExampleComponent):
            active_entities += 1
        for entity, component in self.world.get_entities_with_component(ExampleComponent, all_entities=True):
            all_entities += 1

        assert active_entities == 2
        assert all_entities == 3


@dataclasses.dataclass
class ExampleComponent:
    x = 3
    y = 'sus'
    z = None


@dataclasses.dataclass
class ExampleComponent2:
    a = 0


class ExampleSceneManager:
    def __init__(self):
        self.scenes = {}
        self.active_scenes = []
        self.selected_scene = None

    def create_scene(self, name, activate=False, select=False):
        if name not in self.scenes:
            self.scenes[name] = []

            if activate:
                self.activate_scene(name)

            if select:
                self.select_scene(name)

            return self.scenes[name]

    def select_scene(self, name):
        if name in self.scenes:
            self.selected_scene = name

    def activate_scene(self, name):
        if name in self.scenes:
            self.active_scenes.append(name)

# TODO: implement test scenes for normal entity check


pytest.main()
