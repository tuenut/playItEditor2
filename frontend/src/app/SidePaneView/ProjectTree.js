import React, {Fragment} from "react";

import PrejectTreeElement from './PrejectTreeElement';

export default ProjectTree;

function ProjectTree({tree, path}) {
  if (tree) {
    let sorted_tree = [];
    let tree_keys = Object.keys(tree).sort();

    let i = 0;
    while (i < tree_keys.length) {
      let key = tree_keys[i];

      if (key.toLowerCase().endsWith('plt')) {
        sorted_tree.push(tree_keys.splice(i, 1)[0]);
      } else {
        i++;
      }
    }
    sorted_tree = sorted_tree.concat(tree_keys);

    return (
      <ul className={"list-group list-group-flush border"}>
        {sorted_tree.map((name) => (
          <PrejectTreeElement name={name} key={name} content={tree[name]} path={path}/>)
        )}
      </ul>
    )
  } else {
    return (<Fragment/>)
  }
}
