from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_a


def start_event(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def time_out(e):
    return e[0] == 'TIME_OUT'

def key_a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.event_q = []
        self.cur_state = None
        self.transitions = {}

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.boy, ('START', None))

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return

    def update(self):
        if len(self.event_q) > 0:  # 이벤트 큐 처리 추가
            event = self.event_q.pop()
            self.handle_event(event)
        if self.cur_state:
            self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)

    def add_event(self, e):
        print(f'DEBUG: add event {e}')
        self.event_q.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions