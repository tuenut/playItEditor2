import React, {Fragment} from "react";

import PrejectTreeElement from './PrejectTreeElement';


export default class ProjectTree extends React.Component {
  render() {
    if (this.props.project) {
      let sorted_tree = [];
      let tree_keys = Object.keys(this.props.project.project_tree).sort();

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
              <PrejectTreeElement
                name={name} key={name} content={this.props.project.project_tree[name]} path={this.props.path}
              />
            )
          )}
        </ul>
      )
    } else {
      return (<Fragment/>)
    }
  }
}
