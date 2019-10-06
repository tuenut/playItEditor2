import React from 'react';
import axios from 'axios';

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
    console.log(this.state.file_path);
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
        <input className={"form-control"} type={"text"} value={this.state.file_path} onChange={this.handleOnChange}
               style={{"width": "20rem"}} name={"open_plt"}/>
      </div>
    )
  }
}


class NavigationBar extends React.Component {
  render() {
    return (
      <header className="navbar navbar-expand navbar-dark bg-dark flex-column flex-md-row w-100"
              style={{"position": 'fixed', "top": 0, "zIndex": 1071}}>

        <div className="navbar-brand">
          <img className="d-block" width="36" height="36" src="edit.png"/>
        </div>

        <div className={"d-flex justify-content-between w-100"}>
          <div className="navbar-nav-scroll">
            <ul className="navbar-nav flex-row">

              <li className="nav-item  mx-1">
                <div className="nav-link">Home</div>
              </li>

              <li className="nav-item mx-1">
                <OpenFile openProjectCallback={this.props.openProjectCallback}/>
              </li>

            </ul>
          </div>

          <div className={""}>
            {
              this.props.projectName &&
              <h3 className={"mx-auto text-light font-weight-bold my-0"}>
                <span>{"Project: <"}</span>
                <span>{this.props.projectName}</span>
                <span>{"\>"}</span>
              </h3>
            }
          </div>
        </div>

      </header>
    )
  }
}

export default NavigationBar;