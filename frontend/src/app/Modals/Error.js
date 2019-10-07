import React, {Fragment} from "react";
import {Modal, Button} from 'react-bootstrap';


export default class ErrorModal extends React.Component {
  render() {
    return (
      <Fragment>

        <Modal show={this.props.error.show} onHide={this.props.closeCallback}>
          <Modal.Header closeButton>
            <Modal.Title>
              {this.props.error.title}
            </Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {this.props.error.body}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={this.props.closeCallback}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>

      </Fragment>
    )
  }
}

