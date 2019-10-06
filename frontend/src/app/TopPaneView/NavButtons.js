import React from "react";
import axios from "axios/index";

import ProjectContext from '../Context/ProjectContext';


class OpenFile extends React.Component {
  constructor(props) {
    super(props);

    this.state = {"file_path": null};

    this.handleOpenClick = this.handleOpenClick.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
  }

  handleOnChange(event) {
    this.setState({"file_path": event.target.value});
  }

  handleOpenClick() {
    axios.get('http://127.0.0.1:5000/open?file=' + this.state.file_path)
      .then((response) => {
        let data = response.data;
        this.props.openProjectCallback(data);
      });
  }

  render() {
    return (
      <div className={"form-inline"}>
        <div className="btn btn-light font-weight-bold mr-2" onClick={this.handleOpenClick}>
          Open
        </div>
        <input className={"form-control"} type={"text"} style={{"width": "20rem"}} name={"open_plt"}
               value={this.state.file_path} onChange={this.handleOnChange}/>
      </div>
    )
  }
}


export default class NavButtons extends React.Component {
  render() {
    return (
      <div className="navbar-nav-scroll">
        <ul className="navbar-nav flex-row">

          <li className="nav-item mx-1">
            <ProjectContext.Consumer>
              {(context) => (<OpenFile openProjectCallback={context.openProjectCallback}/>)}
            </ProjectContext.Consumer>
          </li>

        </ul>
      </div>
    )
  }
}