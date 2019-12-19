import {CHANGE_OPEN_FILE_PATH} from './actions';

const default_state = {open_project_path: '/home/tuenut/temp/mpy/_example.py'};

export const openFileReducer = (state = default_state, action) => {
  switch (action.type) {
    case CHANGE_OPEN_FILE_PATH:
      return {
        ...state,
        open_project_path: action.payload
      }

    default:
      return state
  }
}
