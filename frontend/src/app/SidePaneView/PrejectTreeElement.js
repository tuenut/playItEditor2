import React, {Fragment} from "react";
import {Button} from "react-bootstrap";

import {ProjectContext, AppMethodsContext} from "../Context/ProjectContext";
import ProjectTree from './ProjectTree';


export default class PrejectTreeElement extends React.Component {
  static contextType = AppMethodsContext;

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
    this.context.appMethods.switchMacros(this.state.path.concat([this.props.name]))
  }

  render() {
    return (
      <Fragment>
        <li className={this.state.classes}>

          {
            this.props.name.toLowerCase().endsWith('.plt') ? (
              <Button
                block variant={"light"} onClick={this.handleOnClick} className={this.state.button_classes}
              >
                {this.props.name}
              </Button>
            ) : (
              <div>
                <Button disabled variant={"light"} className={"font-weight-bold"}>{this.props.name}</Button>
                <ProjectTree tree={this.props.content} path={this.state.path.concat(this.props.name)}/>
              </div>
            )
          }

        </li>
      </Fragment>
    )
  }
}

