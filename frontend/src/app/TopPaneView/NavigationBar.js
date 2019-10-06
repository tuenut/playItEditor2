import React from 'react';

import ProjectContext from '../Context/ProjectContext';
import NavButtons from './NavButtons';
import logo from './logo.png';


const ProjectTitle = () => (
  <ProjectContext.Consumer>
    {
      (context) => (
        context.project &&
        <h3 className={"mx-auto text-light font-weight-bold my-0"}>
          {"Project: "}{context.project.project_name}
        </h3>
      )
    }
  </ProjectContext.Consumer>
);

const NavLogo = () => (
  <div className={"navbar-brand"}>
    <img className={"d-block"} width={36} height={36} alt={"logo"} src={logo}/>
  </div>
);


class NavigationBar extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "classes": "navbar navbar-expand navbar-dark bg-dark flex-column flex-md-row w-100",
      "style": {"position": 'fixed', "top": 0, "zIndex": 1071}
    }
  }

  render() {
    return (
      <header className={this.state.classes} style={this.state.style}>

        <NavLogo/>

        <NavButtons/>

        <ProjectTitle/>

      </header>
    )
  }
}

export default NavigationBar;