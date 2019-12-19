export const OPEN_PROJECT = "OPEN_PROJECT";
export const CHANGE_PROJECT_DATA = "CHANGE_PROJECT_DATA";

export const openProject = project => ({
  type: OPEN_PROJECT,
  payload: project
})

export const changeProjectData = (data_path, new_data) => ({
  type: CHANGE_PROJECT_DATA,
  data_path,
  new_data
})