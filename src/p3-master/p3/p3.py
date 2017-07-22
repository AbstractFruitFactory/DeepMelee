import os.path
import time

import fox
import memory_watcher
import menu_manager
import pad
import state
import state_manager
import stats


def find_dolphin_dir():
    """Attempts to find the dolphin user directory. None on failure."""
    candidates = ['~/.dolphin-emu', '~/.local/share/.dolphin-emu']
    for candidate in candidates:
        path = os.path.expanduser(candidate)
        if os.path.isdir(path):
            return path
    return None

def write_locations(dolphin_dir, locations):
    """Writes out the locations list to the appropriate place under dolphin_dir."""
    path = dolphin_dir + '/MemoryWatcher/Locations.txt'
    with open(path, 'w') as f:
        f.write('\n'.join(locations))

        dolphin_dir = find_dolphin_dir()
        if dolphin_dir is None:
            print('Could not detect dolphin directory.')
            return

def run(fox, this_state, sm, mw, this_pad, this_stats):
    mm = menu_manager.MenuManager()
    while True:
        last_frame = this_state.frame
        res = next(mw)
        if res is not None:
            sm.handle(*res)
        if this_state.frame > last_frame:
            this_stats.add_frames(this_state.frame - last_frame)
            start = time.time()
            make_action(this_state, this_pad, mm, fox)
            this_stats.add_thinking_time(time.time() - start)

def make_action(this_state, this_pad, mm, this_fox):
    if this_state.menu == state.Menu.Game:
        this_fox.advance(this_state, this_pad)
    elif this_state.menu == state.Menu.Characters:
        mm.pick_fox(this_state, this_pad)
    elif this_state.menu == state.Menu.Stages:
        # Handle this once we know where the cursor position is in memory.
        this_pad.tilt_stick(pad.Stick.C, 0.5, 0.5)
    elif this_state.menu == state.Menu.PostGame:
        mm.press_start_lots(this_state, this_pad)

def main():
    dolphin_dir = find_dolphin_dir()
    if dolphin_dir is None:
        print('Could not find dolphin config dir.')
        return

    this_state = state.State()
    sm = state_manager.StateManager(this_state)
    write_locations(dolphin_dir, sm.locations())

    this_stats = stats.Stats()

    this_fox = fox.Fox()

    try:
        print('Start dolphin now. Press ^C to stop p3.')
        pad_path = dolphin_dir + '/Pipes/p3'
        mw_path = dolphin_dir + '/MemoryWatcher/MemoryWatcher'
    
        with pad.Pad(pad_path) as this_pad, memory_watcher.MemoryWatcher(mw_path) as mw:
            
            run(this_fox, this_state, sm, mw, this_pad, this_stats)
    except KeyboardInterrupt:
        print('Stopped')
        print(this_stats)

if __name__ == '__main__':
    main()
