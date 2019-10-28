import React from "react";
import {Button, InputGroup, FormControl} from 'react-bootstrap';

import axios from "axios/index";

import {AppMethodsContext} from '../Context/ProjectContext';


export default class OpenFile extends React.Component {
  static contextType = AppMethodsContext;

  constructor(props) {
    super(props);

    this.state = {
      "file_path": '/home/tuenut/temp/mpy/_example.py',
      "placeholderText": "Enter init file path..."
    };

    this.handleOpenClick = this.handleOpenClick.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
  }

  handleOnChange(event) {
    this.setState({"file_path": event.target.value});
  }

  handleOpenClick(event) {
    axios.get('http://127.0.0.1:5000/open?file=' + this.state.file_path)
      .then(
        (response) => this.context.appMethods.openProject(response.data),
        (error) => this.context.appMethods.raiseErrorModal("Error", "Cant open file")
      );
  }

  render() {
    return (
      <InputGroup>
        <FormControl
          placeholder={this.state.placeholderText} aria-label={this.state.placeholderText} aria-describedby="openFile"
          style={{"width": "20rem"}} name={"openProject"} value={this.state.file_path} onChange={this.handleOnChange}
          onKeyDown={
            (event) => {
              if (event.key === 'Enter') {
                this.handleOpenClick();
              }
            }
          }
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


