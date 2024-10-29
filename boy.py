from pico2d import load_image, get_time
from state_machine import StateMachine, time_out, right_down, left_up, left_down, right_up, start_event, key_a_down


class Idle:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.action = 3
            boy.face_dir = 0
        elif right_down(e) or left_up(e):
            boy.action = 2
            boy.face_dir = -1
        elif left_down(e) or right_up(e):
            boy.action = 3
            boy.face_dir = 1

        boy.frame = 0
        boy.wait_time = get_time()
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.start_time > 3.00:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Sleep:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.face_dir = 1
            boy.action = 3
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
            3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          3 * 3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, -1, 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

        if boy.x < 1:
            boy.x = 1
        elif boy.x > 800:
            boy.x = 800
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)



class AutoRun:

    @staticmethod
    def enter(boy, e):

        if boy.action == 2:
            boy.dir = -1
            boy.action = 0

        elif boy.action == 3:
            boy.dir = 1
            boy.action = 1

        boy.speed = 10
        boy.scale = 5
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.wait_time >= 5:
            boy.state_machine.handle_event(('TIME_OUT', 0))

        boy.x += boy.dir * boy.speed

        if boy.x > 800:
            boy.action = 0
            boy.dir = -1

        elif boy.x < 0:
            boy.action = 1
            boy.dir = 1

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + 120, 100 * boy.scale,
                            100 * boy.scale)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.face_dir = 1  # face_dir 초기값 설정
        self.start_time = get_time()
        self.wait_time = get_time()
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Sleep, key_a_down: AutoRun},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, start_event: Idle, key_a_down: AutoRun},
                AutoRun: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
