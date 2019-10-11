import React from "react";
import {Button, InputGroup, FormControl} from 'react-bootstrap';

import axios from "axios/index";

import ProjectContext from '../Context/ProjectContext';


export default class OpenFile extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "file_path": '/home/tuenut/temp/mpy/49.py',
      "placeholderText": "Enter init file path..."
    };

    this.handleOpenClick = this.handleOpenClick.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
  }

  handleOnChange(event) {
    this.setState({"file_path": event.target.value});
  }

  handleOpenClick() {
    axios.get('http://127.0.0.1:5000/open?file=' + this.state.file_path)
      .then(
        (response) => this.context.openProject(response.data),
        (error) => this.context.raiseError("Error", "Cant open file")
      );
  }

  static contextType = ProjectContext;

  render() {
    return (
      <InputGroup >
        <FormControl
          placeholder={this.state.placeholderText} aria-label={this.state.placeholderText} aria-describedby="openFile"
          style={{"width": "20rem"}} name={"openProject"}
          value={this.state.file_path} onChange={this.handleOnChange}
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


