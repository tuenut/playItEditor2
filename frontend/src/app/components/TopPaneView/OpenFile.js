import React from "react";
import {Button, InputGroup, FormControl} from 'react-bootstrap';

import axios from "axios/index";
import {openProjectOnClick} from "../../store/App/actions";


export default class OpenFile extends React.Component {
  constructor(props) {
    super(props);

    this.handleOpenClick = this.handleOpenClick.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
    this.handleOnPressEnter = this.handleOnPressEnter.bind(this);
  }

  handleOnChange(event) {
    this.props.projectPathOnChange(event.target.value);
  }

  handleOpenClick(event) {
    axios.get('http://127.0.0.1:5000/open?file=' + this.props.project_path)
      .then(
        (response) => this.props.openProjectOnClick(response.data),
        (error) => this.context.appMethods.raiseErrorModal("Error", "Cant open file")
      );
  }

  handleOnPressEnter(event) {
    if (event.key === 'Enter') {
      this.handleOpenClick();
    }
  }

  render() {
    return (
      <InputGroup>
        <FormControl
          placeholder={"Enter project path"} aria-label={"Enter project path"} aria-describedby="openFile"
          style={{"width": "20rem"}} name={"openProject"} value={this.props.project_path}
          onChange={this.handleOnChange}
          onKeyDown={this.handleOnPressEnter}
        />
        <InputGroup.Append>
          <Button variant={"light"} className={"border-left"} onClick={this.handleOpenClick}>
            Open PLT project
          </Button>
        </InputGroup.Append>
      </InputGroup>
    )
  }
}


