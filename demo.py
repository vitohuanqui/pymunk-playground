import pymunk
import pygame


class Physics:

    def __init__(self):
        # Initialize pymunk, set gravity
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

    def create_ball(self, center, mass=1.0, radius=10.0, elasticity=0.95):
        moment = pymunk.moment_for_circle(mass, radius, 0.0, pymunk.Vec2d(0, 0))
        body = pymunk.Body(mass, moment)
        body.position = pymunk.Vec2d(center)

        shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
        shape.friction = 1.5
        shape.collision_type = 0
        shape.elasticity = elasticity
        self.space.add(body, shape)
        return shape

    def create_wall(self, points, friction=1.0, elasticity=0.95):
        if len(points) != 2:
            return []

        points = list(map(pymunk.Vec2d, points))

        v1 = pymunk.Vec2d(points[0].x, points[0].y)
        v2 = pymunk.Vec2d(points[1].x, points[1].y)

        body = pymunk.Body()
        shape = pymunk.Segment(body, v1, v2, .0)

        shape.friction = friction
        shape.collision_type = 0
        shape.elasticity = elasticity

        self.space.add(shape)

        return shape

    def flipyv(self, v, window):
        return int(v.x), int(-v.y + window.height)

    def draw_ball(self, ball, window, color=(0, 0, 0)):
        body = ball.body
        v = body.position + ball.offset.cpvrotate(body.rotation_vector)
        p = self.flipyv(v, window)
        r = ball.radius
        pygame.draw.circle(window.screen, color, p, int(r), 1)

    def draw_wall(self, wall, window, color=(50, 50, 50)):
        body = wall.body
        pv1 = self.flipyv(
            body.position + wall.a.cpvrotate(body.rotation_vector), window)

        pv2 = self.flipyv(
            body.position + wall.b.cpvrotate(body.rotation_vector), window)

        pygame.draw.lines(window.screen, color, False,
            [pv1, pv2])


class Window:

    def __init__(self):
        self.width = 680
        self.height = 680
        self.screen = pygame.display.set_mode((self.width, self.height))


class Demo:

    def __init__(self):
        pygame.init()

    def play(self):
        window = Window()
        physics = Physics()
        fps = 60
        dt = 1.0 / fps

        ball = physics.create_ball((window.width // 2, window.height // 2))
        ball2 = physics.create_ball(
            (window.width // 2 + 3, window.height // 2 + 20))
        wall = physics.create_wall([(1, 200), (600, 200)])
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            window.screen.fill((255, 255, 255))

            physics.draw_ball(ball, window)
            physics.draw_ball(ball2, window)
            physics.draw_wall(wall, window)

            physics.space.step(dt)
            pygame.display.flip()

            clock.tick(fps)


if __name__ == "__main__":
    demo = Demo()
    demo.play()