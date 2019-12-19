export const CHANGE_OPEN_FILE_PATH = 'CHANGE_FILE_PATH';

export const changeFilePath = open_project_path => ({
  type: CHANGE_OPEN_FILE_PATH,
  payload: open_project_path
})