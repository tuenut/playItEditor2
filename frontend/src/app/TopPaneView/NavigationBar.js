import React from 'react';
import axios from 'axios';

class NavigationBar extends React.Component {
  constructor(props) {
    super(props);

    this.handleOpenClick = this.handleOpenClick.bind(this);
  }

  handleOpenClick() {
    axios.get('http://127.0.0.1:5000/')
      .then((response) => {
        let data = response.data;
        this.props.openProjectCallback(data)
      });
  }

  render() {
    return (
      <header className="navbar navbar-expand navbar-dark bg-dark flex-column flex-md-row w-100"
              style={{"position": 'fixed', "top": 0, "zIndex": 1071}}>

        <div className="navbar-brand">
          <img className="d-block" width="36" height="36" src="edit.png"/>
        </div>

        <div className="navbar-nav-scroll">
          <ul className="navbar-nav flex-row">

            <li className="nav-item  mx-1">
              <div className="nav-link">Home</div>
            </li>

            <li className="nav-item mx-1">
              <div className="btn btn-light font-weight-bold" onClick={this.handleOpenClick}>
                Open
              </div>
            </li>

          </ul>
        </div>

        {
          this.props.projectName &&
          <h3 className={"mx-auto text-light font-weight-bold my-0"}>
            <span>{"Project: <"}</span>
            <span>{this.props.projectName}</span>
            <span>{"\>"}</span>
          </h3>
        }

      </header>
    )
  }
}

export default NavigationBar;