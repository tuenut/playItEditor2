import React, {Fragment} from "react";
import {Button} from "react-bootstrap";

import ProjectContext from '../Context/ProjectContext';


class PrejectTreeElement extends React.Component {
  static contextType = ProjectContext;

  constructor(props) {
    super(props);

    this.state = {
      "classes": "py-0 m-0",
      "button_classes": "py-0 rounded-0 ",
      "macros_path": [this.props.path]
    }
  }

  render() {
    return (
      <Fragment>
        <li className={this.state.classes}>

          {
            this.props.name.toLowerCase().endsWith('.plt') ? (
              <Button block variant={"light"} onClick={() => this.context.switchMacros(this.props.name)}
                      className={this.state.button_classes}>
                {this.props.name}
              </Button>
            ) : (
              <div>
                <Button block variant={"light"} disabled>{this.props.name}</Button>
                <ProjectTree tree={this.props.content}/>
              </div>
            )
          }
        </li>
      </Fragment>
    )
  }
}


class ProjectTree extends React.Component {
  render() {
    let element_path = this.props.parent ? (["/"].concat(this,props.parent)) : ["/"];
    return (
      <ul className={"list-group list-group-flush"}>
        {
          this.props.tree &&
          Object.keys(this.props.tree).map((name) => (
            <PrejectTreeElement name={name} key={name} content={this.props.tree[name]} path={element_path}/>)
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
        "zIndex": 998
      },
      "classes": "col border-right border-dark bg-light px-0"
    }
  }

  static contextType = ProjectContext;

  render() {
    return (
      <nav className={this.state.classes} style={this.state.style}>
        <div className={"alert-danger w-100 m-0"}>Side Panel</div>
        <div className="d-flex flex-column my-3 d-xs-none">
          {this.context.project && <ProjectTree tree={this.context.project.project_tree}/>}
        </div>
      </nav>
    )
  }

}

export default SidePane;