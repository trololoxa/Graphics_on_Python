import imgui
import pathlib

from TSGEngine import Main
from TSGEngine.Object.entity import Circle, Rectangle

# Systems
from Program.Assets.PlatformController import PlatformController
from Program.Assets.BallController import BallController

# Components for systems
from Program.Assets.BallComponent import BallComponent
from Program.Assets.PlatformComponent import PlatformComponent
from TSGEngine.Physics.Components.Colliders.RectangleCollider import RectangleCollider
from TSGEngine.World.Components.Mesh import Mesh

main = Main()

# Initialization, Insert Core assets folder here
# TODO: automatically get core assets from internet
main.initialize('G:/Programming/Python/TSGEngine/Program/Core_Assets')

main.window.create_window(800, 800, 'Example')

main.past_window_initialize()

frag_shader_path = str(pathlib.Path('Assets/Shaders/main.frag').absolute())
vert_shader_path = str(pathlib.Path('Assets/Shaders/main.vert').absolute())

main.world.shader_manager.add_shader('main', frag_shader_path, vert_shader_path)

# Creating and adding systems
Platform_system = PlatformController()
Ball_system = BallController()

main.world.add_system(Platform_system)
main.world.add_system(Ball_system)

# Creating and initializing entities
ball = main.world.create_entity(Circle(radius=0.03, subdivisions=2))
ball_component = BallComponent()
ball_component.speed = 0.4
ball_collider = RectangleCollider()
ball_collider.initialize_bounding_box(ball.components[Mesh].vertices)
ball.add_component(ball_component)
ball.add_component(ball_collider)

left_rectangle = main.world.create_entity(Rectangle(position=(-0.87, 0, 0), scale=(0.07, 0.3, 1)))
left_rectangle_component = PlatformComponent('w', 's')
left_rectangle_collider = RectangleCollider()
left_rectangle_collider.initialize_bounding_box(left_rectangle.components[Mesh].vertices)
left_rectangle.add_component(left_rectangle_component)
left_rectangle.add_component(left_rectangle_collider)

right_rectangle = main.world.create_entity(Rectangle(position=(0.87, 0, 0), scale=(0.07, 0.3, 1)))
right_rectangle_component = PlatformComponent('up_arrow', 'down_arrow')
right_rectangle_collider = RectangleCollider()
right_rectangle_collider.initialize_bounding_box(right_rectangle.components[Mesh].vertices)
right_rectangle.add_component(right_rectangle_component)
right_rectangle.add_component(right_rectangle_collider)


def gui_func():
    is_expand, _ = imgui.begin("Info", False)
    if is_expand:
        imgui.text(f'right rectangle y pos = {right_rectangle.transform.position[1]:.4f}')
        imgui.text(f'left rectangle y pos = {left_rectangle.transform.position[1]:.4f}')
        imgui.text(f'ball pos = vec2({ball.transform.position[0]:.4f}, {ball.transform.position[1]:.4f})')
        imgui.text(f'ball direction = vec2({ball_component.direction[0]:.4f}, {ball_component.direction[1]:.4f})')
        imgui.text(f'ball speed = {ball_component.speed}')
    imgui.end()

    is_expand, _ = imgui.begin("Control", False)
    if is_expand:
        if imgui.button('Reset ball position', 150, 20):
            ball.transform.position = [0, 0, 0]
            speed = ball_component.speed
            score = ball_component.score
            ball_component.__init__()
            ball_component.speed = speed
            ball_component.score = score
        if imgui.button('Reset score', 150, 20):
            ball_component.score = [0, 0]
        ball_component.speed = imgui.slider_float('Ball speed', ball_component.speed, 0, 1)[1]
        if imgui.button('Start', 150, 20):
            if left_rectangle_component.speed == 0:
                left_rectangle_component.speed, left_rectangle_component.speed_cache = \
                    left_rectangle_component.speed_cache, left_rectangle_component.speed
            if right_rectangle_component.speed == 0:
                right_rectangle_component.speed, right_rectangle_component.speed_cache = \
                    right_rectangle_component.speed_cache, right_rectangle_component.speed
            if ball_component.speed == 0:
                ball_component.speed, ball_component.speed_cache = ball_component.speed_cache, ball_component.speed
        if imgui.button('Pause', 150, 20):
            if left_rectangle_component.speed_cache == 0:
                left_rectangle_component.speed, left_rectangle_component.speed_cache = \
                    left_rectangle_component.speed_cache, left_rectangle_component.speed
            if right_rectangle_component.speed_cache == 0:
                right_rectangle_component.speed, right_rectangle_component.speed_cache = \
                    right_rectangle_component.speed_cache, right_rectangle_component.speed
            if ball_component.speed_cache == 0:
                ball_component.speed, ball_component.speed_cache = ball_component.speed_cache, ball_component.speed
        if imgui.button('Reset', 150, 20):
            ball.transform.position = [0, 0, 0]
            speed = ball_component.speed
            score = ball_component.score
            ball_component.__init__()
            ball_component.speed = speed
            ball_component.score = score

            right_rectangle.transform.position = [right_rectangle.transform.position[0], 0, 0]
            left_rectangle.transform.position = [left_rectangle.transform.position[0], 0, 0]

            ball_component.score = [0, 0]

    imgui.end()

    is_expand, _ = imgui.begin("Score", False)
    if is_expand:
        imgui.text('    SCORE \n'
                   'left : right \n'
                   f'{ball_component.score[0]}    :    {ball_component.score[1]}')
    imgui.end()


main.loop(gui_func)
