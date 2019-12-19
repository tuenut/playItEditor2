import {OPEN_PROJECT, CHANGE_PROJECT_DATA} from "./actions";

function getMacros(macros, project_tree) {
  let tree_object = project_tree;

  for (let i in macros) {
    tree_object = tree_object[macros[i]];
  }

  return tree_object
}

function update_project(tree, macros_path, new_data) {
  let sub_tree = {...tree};
  let data_key = macros_path[0];

  if (macros_path.length > 1) {
    let tree_part = getMacros(macros_path.slice(0, 1), tree);
    let rest_path = macros_path.slice(1);
    sub_tree = {
      ...sub_tree,
      [data_key]: update_project(tree_part, rest_path, new_data)
    }
  } else {
    sub_tree = {...sub_tree, [data_key]: new_data}
  }
  return sub_tree
}

export const projectReducer = (state = {}, action) => {
  switch (action.type) {
    case OPEN_PROJECT:
      let a = {
        ...state,
        project: action.payload
      }

      console.log(a)

      return a

    case CHANGE_PROJECT_DATA:
      return {
        ...state,
        ...update_project(state, action.data_path, action.new_data)
      }

    default:
      return state
  }
}







