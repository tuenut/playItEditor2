import React, {Fragment} from "react";

import ProjectContext from '../Context/ProjectContext';


class PrejectTreeElement extends React.Component {
  constructor(props) {
    super(props);

    this.state = {"classes": "list-group-item py-0"}
  }

  render() {
    return (
      <Fragment>
        <li className={this.state.classes}>
          {this.props.name}
          {!this.props.name.toLowerCase().endsWith('.plt') && <ProjectTree tree={this.props.content}/>}
          </li>
      </Fragment>
    )
  }
}


class ProjectTree extends React.Component {
  render() {
    return (
      <ul className={"list-group list-group-flush"}>
        {
          this.props.tree &&
          Object.keys(this.props.tree).map((name) => (
            <PrejectTreeElement name={name} key={name} content={this.props.tree[name]}/>)
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

  render() {
    return (
      <nav className={this.state.classes} style={this.state.style}>
        <div className={"alert-danger w-100 m-0"}>Side Panel</div>
        <div className="d-flex flex-column my-3 d-xs-none">

          <ProjectContext.Consumer>
            {(context) => context.project && <ProjectTree tree={context.project.project_tree}/>}
          </ProjectContext.Consumer>
        </div>

      </nav>
    )
  }

}

export default SidePane;