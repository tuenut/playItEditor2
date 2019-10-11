import React, {Fragment} from "react";
import {Modal, Button} from 'react-bootstrap';

import ProjectContext from '../Context/ProjectContext';


export default class ErrorModal extends React.Component {
  static contextType = ProjectContext;

  render() {
    return (
      <Fragment>

        <Modal show={this.props.error.show} onHide={this.context.closeError}>
          <Modal.Header closeButton>
            <Modal.Title>
              {this.props.error.title}
            </Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {this.props.error.body}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={this.context.closeError}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>

      </Fragment>
    )
  }
}

