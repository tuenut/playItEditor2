export const LOAD_PROJECT = "LOAD_PROJECT";
export const SET_PROJECT_NAME = "SET_PROJECT_NAME";
// export const CHANGE_PROJECT_DATA = "CHANGE_PROJECT_DATA";

export const openProjectOnClick = project => ({
  type: LOAD_PROJECT,
  payload: project
})

export const setProjectName = name => ({
  type: SET_PROJECT_NAME,
  payload: name
})

// export const changeProjectData = (data_path, new_data) => ({
//   type: CHANGE_PROJECT_DATA,
//   data_path,
//   new_data
// })