import React from "react";

import PrejectTreeElement from './PrejectTreeElement';


export default class ProjectTree extends React.Component {
  sort_directories_after(tree) {
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

    return sorted_tree
  }

  render() {
    return (
      <ul className={"list-group list-group-flush border"}>
        {
          this.props.tree &&
          this.sort_directories_after(this.props.tree).map((name) => (
            <PrejectTreeElement name={name} key={name} content={this.props.tree[name]} path={this.props.path}/>)
          )
        }
      </ul>
    )
  }
}