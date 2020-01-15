import {PROJECT_PATH_INPUT_ON_CHANGE} from './actions';

const default_state = {project_path: '/home/tuenut/temp/mpy/_example.py'};

export const navbarLevelReducer = (state = default_state, action) => {
  switch (action.type) {
    case PROJECT_PATH_INPUT_ON_CHANGE:
      return {
        ...state,
        project_path: action.payload
      }

    default:
      return state
  }
}
