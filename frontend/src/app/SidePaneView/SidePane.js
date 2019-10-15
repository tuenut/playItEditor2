import React, {Fragment} from "react";
import {Button} from "react-bootstrap";

import ProjectContext from '../Context/ProjectContext';


class PrejectTreeElement extends React.Component {
  static contextType = ProjectContext;

  constructor(props) {
    super(props);

    this.state = {
      "classes": "py-0",
      "button_classes": "py-0 rounded-0 ",
      "path": this.props.path
    };

    this.handleOnClick = this.handleOnClick.bind(this);
  }

  handleOnClick() {
    this.context.switchMacros(this.state.path.concat([this.props.name]))
  }

  render() {
    return (
      <Fragment>
        <li className={this.state.classes}>

          {
            this.props.name.toLowerCase().endsWith('.plt') ? (
              <Button block variant={"light"} onClick={this.handleOnClick}
                      className={this.state.button_classes}>
                {this.props.name}
              </Button>
            ) : (
              <div>
                <Button  disabled variant={"light"} className={"font-weight-bold"}>{this.props.name}</Button>
                <ProjectTree tree={this.props.content} path={this.state.path.concat(this.props.name)}/>
              </div>
            )
          }
        </li>
      </Fragment>
    )
  }
}


class ProjectTree extends React.Component {
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


class SidePane extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "style": {
        "height": "100%",
        "marginTop": "4.2rem",
        "position": "fixed",
        "width": "16rem",
        "zIndex": 998,
      },
      "classes": "col border-right border-dark bg-light px-0 overflow-auto"
    }
  }

  static contextType = ProjectContext;

  render() {
    return (
      <nav className={this.state.classes} style={this.state.style}>
        <div className={"alert-danger w-100 m-0"}>Side Panel</div>
        <div className="d-flex flex-column my-3 d-xs-none">
          {this.context.project && <ProjectTree tree={this.context.project.project_tree} path={[]}/>}
        </div>
      </nav>
    )
  }

}

export default SidePane;